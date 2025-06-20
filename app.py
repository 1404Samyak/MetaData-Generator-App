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
body, .main {
    background: linear-gradient(120deg, #e0f7fa 0%, #f8f9fa 100%);
    min-height: 100vh;
    font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
    color: #222d3d;
    margin: 0;
    padding: 0;
}

/* ====== App Container ====== */
.stApp {
    background: transparent;
    min-height: 100vh;
    padding: 2rem 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    animation: fadeIn 1.2s cubic-bezier(.4,0,.2,1);
}

/* ====== Title ====== */
.stTitle > h1 {
    font-size: 2.8rem;
    font-weight: 800;
    color: #006494;
    text-align: center;
    letter-spacing: 1px;
    margin-bottom: 0.5em;
    background: linear-gradient(90deg, #00b4d8 30%, #48cae4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: slideDown 0.8s cubic-bezier(.4,0,.2,1);
}

/* ====== Card Style ====== */
.css-1aumxhk {
    background: #ffffffcc;
    border-radius: 18px;
    padding: 2rem 2.5rem;
    box-shadow: 0 8px 32px 0 rgba(0, 49, 90, 0.08), 0 1.5px 4px rgba(0,0,0,0.04);
    margin: 1.5rem 0;
    transition: box-shadow 0.3s, transform 0.3s;
    animation: cardPop 0.7s cubic-bezier(.4,0,.2,1);
}
.css-1aumxhk:hover {
    box-shadow: 0 12px 40px 0 rgba(0, 49, 90, 0.13), 0 2px 8px rgba(0,0,0,0.07);
    transform: translateY(-6px) scale(1.02);
}

/* ====== Scrollable JSON Box ====== */
.scrollable-json {
    overflow-x: auto;
    background: #f1f8fb;
    border-radius: 8px;
    padding: 1.2rem;
    margin: 1rem 0;
    font-family: 'Fira Mono', 'Consolas', monospace;
    font-size: 1.05rem;
    color: #003366;
    box-shadow: 0 1px 4px rgba(0, 180, 216, 0.07);
    transition: background 0.3s;
}
.scrollable-json:hover {
    background: #e0f7fa;
}

/* ====== File Upload Button ====== */
input[type="file"]::-webkit-file-upload-button {
    background: linear-gradient(90deg, #00b4d8, #48cae4);
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 0.7em 1.4em;
    font-size: 1.08rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.3s, transform 0.2s;
    box-shadow: 0 2px 8px rgba(0, 180, 216, 0.13);
}
input[type="file"]::-webkit-file-upload-button:hover {
    background: linear-gradient(90deg, #0096c7, #00b4d8);
    transform: scale(1.05);
}

/* ====== Animated Submit Button ====== */
button, .stButton > button {
    background: linear-gradient(90deg, #00b4d8, #48cae4);
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 0.9em 2.2em;
    font-size: 1.15rem;
    font-weight: 700;
    cursor: pointer;
    margin-top: 1.2rem;
    box-shadow: 0 2px 8px rgba(0, 180, 216, 0.13);
    transition: background 0.3s, transform 0.2s, box-shadow 0.3s;
    animation: pulse 2.5s infinite;
}
button:hover, .stButton > button:hover {
    background: linear-gradient(90deg, #0096c7, #00b4d8);
    transform: scale(1.07);
    box-shadow: 0 4px 16px rgba(0, 180, 216, 0.18);
}

/* ====== Animations ====== */
@keyframes fadeIn {
    0% { opacity: 0; }
    100% { opacity: 1; }
}
@keyframes slideDown {
    0% { opacity: 0; transform: translateY(-40px);}
    100% { opacity: 1; transform: translateY(0);}
}
@keyframes cardPop {
    0% { opacity: 0; transform: scale(0.96);}
    100% { opacity: 1; transform: scale(1);}
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 2px 8px rgba(0, 180, 216, 0.13);}
    50% { box-shadow: 0 6px 24px rgba(0, 180, 216, 0.22);}
}

/* ====== Responsive Design ====== */
@media (max-width: 700px) {
    .css-1aumxhk {
        padding: 1.2rem 0.7rem;
    }
    .stTitle > h1 {
        font-size: 2rem;
    }
}
/* ====== Bottom Bar / Footer ====== */
.bottom-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100vw;
    background: linear-gradient(90deg, #00b4d8 0%, #48cae4 100%);
    color: #fff;
    font-size: 1.08rem;
    font-weight: 500;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.8rem 2.5vw;
    box-shadow: 0 -2px 16px rgba(0, 180, 216, 0.05);
    z-index: 9999;
    animation: slideUp 0.7s cubic-bezier(.4,0,.2,1);
}

.bottom-bar a {
    color: #fff;
    text-decoration: underline;
    margin-left: 1.2em;
    transition: color 0.2s;
}
.bottom-bar a:hover {
    color: #caf0f8;
}

@media (max-width: 700px) {
    .bottom-bar {
        flex-direction: column;
        font-size: 0.98rem;
        padding: 1rem 0.5rem;
        text-align: center;
        gap: 0.5em;
    }
}

@keyframes slideUp {
    0% { transform: translateY(60px); opacity: 0; }
    100% { transform: translateY(0); opacity: 1; }
}


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