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
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
load_dotenv()  


# Use Groq via LangChain
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    model="llama3-8b-8192",
    api_key=os.getenv("GROQ_API_KEY")
)

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

def generate_metadata(text):
    prompt = f"""
You are a wonderful and best metadata assistant.
Analyze the following document and return structured metadata in JSON format with fields:
- title
- summary
- keywords
- topics
- author (if mentioned)
- document_type 
Try to explain the summary in detail please,and atleast 9-10 lines in a paragraph.Kindly dont miss any important points in summary
Document:
{text}
"""
    response = llm([
        SystemMessage(content="You are a metadata extraction assistant."),
        HumanMessage(content=prompt)
    ])
    return response.content.strip()

st.set_page_config(page_title="📄 AI Metadata Generator", layout="wide")

st.markdown("""
    <style>

    </style>
""", unsafe_allow_html=True)

st.title("📄 AI Metadata Generator")

uploaded_file = st.file_uploader("📤 Upload a document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    with st.spinner("🧐 Extracting text from the document..."):
        raw_text = extract_text_from_file(uploaded_file)

    with st.spinner("🤖 Generating metadata using Groq via LangChain..."):
        metadata_output = generate_metadata(raw_text)

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