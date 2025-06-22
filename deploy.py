import streamlit as st
import os
import tempfile
import json
from pathlib import Path
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
import pytesseract
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
from PIL import Image
import io
import fitz  
from docx.opc.constants import RELATIONSHIP_TYPE as RT

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama3-8b-8192",
    api_key=os.getenv("GROQ_API_KEY")
)

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def extract_text_and_inline_images(uploaded_file):
    suffix = Path(uploaded_file.name).suffix.lower()
    text = ""
    ocr_text = ""
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
                    xref = img[0]
                    base_image = pdf_doc.extract_image(xref)
                    image_data = base_image["image"]
                    image = Image.open(io.BytesIO(image_data)).convert("RGB")
                    image_list.append(image)
                    ocr_img_text = pytesseract.image_to_string(image)
                    ocr_texts_per_image.append(ocr_img_text)
            ocr_text = "\n".join(ocr_texts_per_image)

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
            ocr_text = "\n".join(ocr_texts_per_image)

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
        "ocr_text": ocr_text.strip(),
        "images": image_list,
        "ocr_texts_per_image": ocr_texts_per_image
    }

def generate_metadata(text):
    prompt = f"""
You are a professional and wonderful metadata assistant.
Analyze the following document,idenitfy and leverage most meaningful sections of document and return structured metadata in JSON format with fields:
- title
- summary (at least 15-20 lines in detail covering all meaningful sections of document)
- Meaningful and important keywords (comma-separated)
- Meaningful and important topics (broad subject categories)
- author (if mentioned)
- document_type
-At end only rewrite the detailed summary(20-30 lines) without missing ay important sections of document so that user can see the summary alone.But dont write in the structured metadata write separately please
Document Content:
{text.strip()}
"""
    response = llm([
        SystemMessage(content="You are a metadata extraction assistant."),
        HumanMessage(content=prompt)
    ])
    return response.content.strip()

def summarize_ocr_text(ocr_text):
    if not ocr_text.strip():
        return "No OCR content found to summarize."

    prompt = (
        "You are a professional assistant. "
        "Start your response with 'The following image ...'. "
        "Summarize the following OCR-extracted content in a clear, well-organized, and visually appealing markdown format in about 5-10 lines "
        "Your summary should include:\n"
        "- A short title or heading for the content\n"
        "- Key points or highlights as a bullet list\n"
        "- Detected names, dates, numbers, or keywords (if any)\n"
        "- A concise paragraph summarizing the main idea or purpose\n"
        "If the content is a graph or chart, explain axes and key trends. "
        "If it's a table, highlight main comparisons or figures. "
        "If it's a scanned paragraph, summarize the main idea. "
        "Avoid assumptions. If content is unclear, mention it.\n\n"
        "If it's none of the above, just describe the content of picture, background, etc.\n"
        f"OCR Text:\n{ocr_text}"
    )

    response = llm([
        SystemMessage(content="You summarize OCR-extracted content in structured markdown."),
        HumanMessage(content=prompt)
    ])
    return response.content.strip()

st.set_page_config(page_title="📄 AI Metadata Generator", layout="wide")
st.title("📄 AI Metadata Generator")

st.markdown("""
<div style='background-color:#f0f2f6; padding: 1em; border-radius: 10px; margin-bottom:1em;'>
    <h3>👋 Welcome to the AI Metadata & Image Summarizer!</h3>
    <ul>
        <li>Upload a <b>PDF, DOCX, or TXT</b> file.</li>
        <li>See extracted text, metadata, and smart summaries of all images.</li>
        <li>Download your results instantly.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📤 Upload a document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    with st.spinner("🧐 Extracting text and inline images..."):
        raw = extract_text_and_inline_images(uploaded_file)
        extracted_text = raw["text"]
        ocr_text = raw["ocr_text"]
        images = raw["images"]
        ocr_texts_per_image = raw.get("ocr_texts_per_image", [])

    with st.spinner("🤖 Generating metadata using Groq via LangChain..."):
        metadata_output = generate_metadata(extracted_text)

    st.success("✅ Metadata generated successfully!")
    st.subheader("📌 Extracted Metadata")

    try:
        metadata_dict = json.loads(metadata_output)
        formatted_json = json.dumps(metadata_dict, indent=2)
    except Exception:
        formatted_json = metadata_output

    st.markdown(f"""<div class='scrollable-json'><pre>{formatted_json}</pre></div>""", unsafe_allow_html=True)
    st.download_button(
        label="⬇️ Download Metadata as JSON",
        data=formatted_json,
        file_name="metadata_output.json",
        mime="application/json"
    )

    if images:
        st.subheader("🖼️ Inline Image Summaries")
        for idx, img in enumerate(images):
            ocr_img_text = ocr_texts_per_image[idx] if idx < len(ocr_texts_per_image) else ""
            if ocr_img_text.strip():
                st.markdown(f"---\n### 🖼️ Image {idx+1}")
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(img, caption=f"Image {idx+1}", use_container_width=True)
                with col2:
                    with st.spinner(f"Summarizing OCR text for Image {idx+1}..."):
                        summary = summarize_ocr_text(ocr_img_text)
                    st.markdown(f"<div class='summary-box'>{summary}</div>", unsafe_allow_html=True)
                    with st.expander("Show Raw OCR Text"):
                        st.code(ocr_img_text)

else:
    st.info("📂 Please upload a file to get started.")
