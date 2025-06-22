import streamlit as st
import os
import tempfile
import json
from pathlib import Path
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
import pytesseract
from pdf2image import convert_from_path
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from PIL import Image
import io

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    model="llama3-8b-8192",
    api_key=os.getenv("GROQ_API_KEY")
)

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def extract_text_and_images(uploaded_file):
    suffix = Path(uploaded_file.name).suffix.lower()
    text = ""
    ocr_text = ""
    image_list = []

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    try:
        if suffix == ".pdf":
            try:
                reader = PdfReader(tmp_file_path)
                text = "\n".join([page.extract_text() or "" for page in reader.pages])
            except:
                text = ""
            images = convert_from_path(tmp_file_path)
            image_list.extend(images)
            ocr_text = " ".join([pytesseract.image_to_string(img) for img in images])

        elif suffix == ".docx":
            doc = DocxDocument(tmp_file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            rels = doc.part._rels
            for rel in rels:
                rel = rels[rel]
                if rel.reltype == RT.IMAGE:
                    image_data = rel.target_part.blob
                    image = Image.open(io.BytesIO(image_data))
                    image_list.append(image)
                    ocr_text += pytesseract.image_to_string(image) + "\n"

        elif suffix == ".txt":
            with open(tmp_file_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            text = f"Unsupported file type: {suffix}"

    finally:
        os.remove(tmp_file_path)

    return {
        "text": text.strip(),
        "ocr_text": ocr_text.strip(),
        "images": image_list
    }

def generate_metadata(text, ocr_text=""):
    combined_text = f"""
The following document contains both extracted text and OCR text from images.

--- Extracted Text ---
{text.strip()}

--- OCR Extracted Text from Images ---
{ocr_text.strip()}
"""
    prompt = f"""
You are a professional metadata assistant.

Analyze the following combined document content and return structured metadata in JSON format with fields:
- title
- summary (at least 9–10 lines in detail)
- keywords (comma-separated)
- topics (broad subject categories)
- author (if mentioned)
- document_type (e.g., research paper, report, article, etc.)

Do not miss any important information from the document or image text.

Combined Content:
{combined_text}
"""
    response = llm([
        SystemMessage(content="You are a metadata extraction assistant."),
        HumanMessage(content=prompt)
    ])
    return response.content.strip()

# Streamlit UI setup
st.set_page_config(page_title="📄 AI Metadata Generator", layout="wide")

# Retain original CSS styles
st.markdown(open("style.css").read(), unsafe_allow_html=True)

st.title("📄 AI Metadata Generator")

uploaded_file = st.file_uploader("📄 Upload a document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    with st.spinner("😮 Extracting text from the document..."):
        raw = extract_text_and_images(uploaded_file)

    with st.spinner("🤖 Generating metadata using Groq via LangChain..."):
        metadata_output = generate_metadata(raw["text"], raw["ocr_text"])

    st.success("✅ Metadata generated successfully!")
    st.subheader("📌 Extracted Metadata")

    try:
        metadata_dict = json.loads(metadata_output)
        formatted_json = json.dumps(metadata_dict, indent=2)
    except:
        formatted_json = metadata_output

    st.markdown(f"""<div class='scrollable-json'>{formatted_json}</div>""", unsafe_allow_html=True)

    st.download_button(
        label="⬇️ Download Metadata as JSON",
        data=formatted_json,
        file_name="metadata_output.json",
        mime="application/json"
    )
else:
    st.info("📂 Please upload a file to get started.")
