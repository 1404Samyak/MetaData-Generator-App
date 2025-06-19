import streamlit as st
import os
import tempfile
from pathlib import Path
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
import pytesseract
from pdf2image import convert_from_path
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

def extract_text_from_file(uploaded_file):
    suffix = Path(uploaded_file.name).suffix.lower()
    text = ""

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    if suffix == ".pdf":
        try:
            reader = PdfReader(tmp_file_path)
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
        except:
            images = convert_from_path(tmp_file_path)
            text = " ".join([pytesseract.image_to_string(image) for image in images])

    elif suffix == ".docx":
        doc = DocxDocument(tmp_file_path)
        text = "\n".join([para.text for para in doc.paragraphs])

    elif suffix == ".txt":
        with open(tmp_file_path, "r", encoding="utf-8") as f:
            text = f.read()

    os.remove(tmp_file_path)
    return text

# ========== METADATA GENERATION via OLLAMA ==========

llm = Ollama(model="mistral")

def generate_metadata(text):
    prompt_template = PromptTemplate.from_template("""
You are a metadata assistant.
Analyze the following document and return structured metadata in JSON format with fields:
- title
- summary
- keywords
- topics
- author (if mentioned)
- document_type (e.g., invoice, paper, legal, resume)
Try to explain the summary in detail please
Document:
{text}
""")
    prompt = prompt_template.format(text=text[:3000])
    return llm.invoke(prompt)

# ========== STREAMLIT UI ========== 

st.set_page_config(page_title="📄 AI Metadata Generator", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f7f9fc;
    }
    .stApp {
        background-image: linear-gradient(to right, #e0f7fa, #f8f9fa);
    }
    .stTitle > h1 {
        font-size: 2.5rem;
        font-weight: 700;
        color: #003366;
    }
    .css-1aumxhk {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
    }
    .scrollable-json {
        overflow-x: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📄 AI Metadata Generator")

uploaded_file = st.file_uploader("📤 Upload a document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    with st.spinner("🧐 Extracting text from the document..."):
        raw_text = extract_text_from_file(uploaded_file)

    with st.spinner("🤖 Generating metadata using Mistral via Ollama..."):
        metadata_output = generate_metadata(raw_text)

    st.success("✅ Metadata generated successfully!")
    st.subheader("📌 Extracted Metadata")
    st.markdown(f"""<div class='scrollable-json'>{metadata_output}</div>""", unsafe_allow_html=True)
else:
    st.info("📂 Please upload a file to get started.")
