import streamlit as st
import os
import tempfile
import json
from pathlib import Path
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
import pytesseract
from dotenv import load_dotenv
from PIL import Image
import io
import fitz
from docx.opc.constants import RELATIONSHIP_TYPE as RT

from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_and_inline_images(uploaded_file):
    suffix = Path(uploaded_file.name).suffix.lower()
    text = ""
    image_list = []
    ocr_texts_per_image = []

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    try:
        if suffix == ".pdf":
            try:
                reader = PdfReader(tmp_file_path)
                text = "\n".join([page.extract_text() or "" for page in reader.pages])
            except Exception:
                text = ""
            pdf_doc = fitz.open(tmp_file_path)
            for page in pdf_doc:
                images = page.get_images(full=False)
                for img in images:
                    xref = img[0] if isinstance(img, tuple) else img
                    base_image = pdf_doc.extract_image(xref)
                    image_data = base_image["image"]
                    image = Image.open(io.BytesIO(image_data)).convert("RGB")
                    image_list.append(image)
                    ocr_img_text = pytesseract.image_to_string(image)
                    ocr_texts_per_image.append(ocr_img_text)
        elif suffix == ".docx":
            doc = DocxDocument(tmp_file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            rels = doc.part._rels
            for rel in rels:
                rel = rels[rel]
                if rel.reltype == RT.IMAGE:
                    image_data = rel.target_part.blob
                    image = Image.open(io.BytesIO(image_data)).convert("RGB")
                    image_list.append(image)
                    ocr_img_text = pytesseract.image_to_string(image)
                    ocr_texts_per_image.append(ocr_img_text)
        elif suffix == ".txt":
            with open(tmp_file_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            text = f"Unsupported file type: {suffix}"
    finally:
        try:
            os.remove(tmp_file_path)
        except PermissionError:
            pass

    return {
        "text": text.strip(),
        "images": image_list,
        "ocr_texts_per_image": ocr_texts_per_image
    }

def chunk_text_by_tokens(text, max_tokens=700):
    chunk_size = 2800
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1
        if current_length >= chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_length = 0
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

def summarize_with_groq(text, api_key, model="llama-3.3-70b-versatile", max_tokens=700):
    llm = ChatGroq(model=model, api_key=api_key, max_tokens=max_tokens)
    prompt = (
    f"Summarize the following text in detail, extracting the most meaningful sections of the document. "
    f"Your summary should include: important information, key points, keywords, author names, any mentioned names, "
    f"specialized terminologies, dates, and numbers if present. "
    f"Present the summary clearly and keep it under {max_tokens} tokens.\n\n"
    f"Text:\n{text}"
    )
    response = llm([
        SystemMessage(content="You are a professional summarization assistant."),
        HumanMessage(content=prompt)
    ])
    return response.content.strip()

def summarize_pdf_text(full_text):
    chunks = chunk_text_by_tokens(full_text, max_tokens=700)
    summaries = []
    for chunk in chunks:
        summary = summarize_with_groq(chunk, api_key=GROQ_API_KEY, model="llama-3.3-70b-versatile", max_tokens=700)
        summaries.append(summary)
    combined_summary = "\n".join(summaries)
    if len(summaries) > 1 or len(combined_summary.split()) > 700:
        combined_summary = summarize_with_groq(combined_summary, api_key=GROQ_API_KEY, model="llama-3.3-70b-versatile", max_tokens=700)
    return combined_summary.strip()

def generate_metadata(summarized_text):
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY, max_tokens=700)
    prompt = f"""
You are a professional and wonderful metadata assistant.

Analyze the following document summary and return structured metadata in JSON format with fields:
- title
- summary (at least 15-20 lines in detail covering all important points)
- keywords (comma-separated)
- topics (broad subject categories)
- author (if mentioned)
- document_type
Document Summary:
{summarized_text}
"""
    try:
        response = llm([
            SystemMessage(content="You are a metadata extraction assistant."),
            HumanMessage(content=prompt)
        ])
        return response.content.strip()
    except Exception as e:
        st.error(f"Metadata extraction failed: {e}")
        return '{"error": "Metadata extraction failed."}'

def summarize_ocr_text(ocr_text):
    if not ocr_text.strip():
        return "No OCR content found to summarize."
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)
    prompt = (
        "You are a professional assistant. "
        "Start your response with 'The following image ...'. "
        "Summarize the following OCR-extracted content in a clear, well-organized, and visually appealing markdown format. "
        "Your summary should include:\n"
        "- A short title or heading for the content\n"
        "- Key points or highlights as a bullet list\n"
        "- Detected names, dates, numbers, or keywords (if any)\n"
        "- A concise paragraph summarizing the main idea or purpose\n"
        "If the content is a graph or chart, explain axes and key trends. "
        "If it's a table, highlight main comparisons or figures. "
        "If it's a scanned paragraph, summarize the main idea. "
        "Avoid assumptions. If content is unclear, mention it.\n\n"
        f"OCR Text:\n{ocr_text}"
    )
    try:
        response = llm([
            SystemMessage(content="You summarize OCR-extracted content in structured markdown."),
            HumanMessage(content=prompt)
        ])
        return response.content.strip()
    except Exception as e:
        return f"OCR summarization failed: {e}"

st.set_page_config(page_title="📄 AI Metadata Generator", layout="wide")
st.title("📄 AI Metadata Generator with Groq")

st.markdown("""
<div style='background-color:#f0f2f6; padding: 1em; border-radius: 10px; margin-bottom:1em;'>
    <h3>Upload a document (PDF, DOCX, or TXT) and generate structured metadata using Groq model. OCR images are summarized separately.</h3>
</div>
""", unsafe_allow_html=True)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📤 Upload a document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    with st.spinner("Extracting text and images..."):
        raw = extract_text_and_inline_images(uploaded_file)
        extracted_text = raw["text"]
        images = raw["images"]
        ocr_texts_per_image = raw.get("ocr_texts_per_image", [])

    st.info("Summarizing the entire document for metadata extraction...")
    with st.spinner("Summarizing document with Groq Llama 3.3 70B Versatile..."):
        summarized_text = summarize_pdf_text(extracted_text)

    with st.spinner("Generating metadata using Groq..."):
        metadata_output = generate_metadata(summarized_text)

    st.success("✅ Metadata generated successfully!")
    st.subheader("📌 Extracted Metadata")

    try:
        metadata_dict = json.loads(metadata_output)
        formatted_json = json.dumps(metadata_dict, indent=2)
    except Exception:
        formatted_json = metadata_output

    st.markdown(f"""<div class='scrollable-json'><pre>{formatted_json}</pre></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class='scrollable-json-2'><pre>{summarized_text}</pre></div>""", unsafe_allow_html=True)
    st.download_button(
        label="⬇️ Download Metadata as JSON",
        data=formatted_json,
        file_name="metadata_output.json",
        mime="application/json"
    )

    if images:
        st.subheader("🖼️ Inline Image Summaries")
        ocr_summary_cache = {}

        for idx, img in enumerate(images):
            ocr_img_text = ocr_texts_per_image[idx] if idx < len(ocr_texts_per_image) else ""
            clean_ocr = ocr_img_text.strip()

            if clean_ocr:
                if clean_ocr not in ocr_summary_cache:
                    with st.spinner(f"Summarizing OCR text for Image {idx+1}..."):
                        summary = summarize_ocr_text(clean_ocr)
                        ocr_summary_cache[clean_ocr] = summary
                else:
                    summary = ocr_summary_cache[clean_ocr]
                st.markdown(f"---\n### 🖼️ Image {idx+1}")
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(img, caption=f"Image {idx+1}", use_container_width=True)
                with col2:
                    st.markdown(f"<div class='summary-box'>{summary}</div>", unsafe_allow_html=True)
                    with st.expander("Show Raw OCR Text"):
                        st.code(clean_ocr)

else:
    st.info("📂 Please upload a file to get started.")
