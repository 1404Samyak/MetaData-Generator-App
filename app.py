# import streamlit as st
# import os
# import tempfile
# import json
# from pathlib import Path
# from PyPDF2 import PdfReader
# from docx import Document as DocxDocument
# import pytesseract
# from pdf2image import convert_from_path
# from langchain_groq import ChatGroq
# from langchain.schema import HumanMessage, SystemMessage
# from dotenv import load_dotenv
# from PIL import Image
# import io
# from docx.opc.constants import RELATIONSHIP_TYPE as RT
# # import pdfplumber

# load_dotenv()
# os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
# llm = ChatGroq(
#     model="llama3-8b-8192",
#     api_key=os.getenv("GROQ_API_KEY")
# )
# pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# def extract_text_and_images(uploaded_file):
#     suffix = Path(uploaded_file.name).suffix.lower()
#     text = ""
#     ocr_text = ""
#     image_list = []
#     ocr_texts_per_image = []

#     with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
#         tmp_file.write(uploaded_file.read())
#         tmp_file_path = tmp_file.name

#     poppler_path = r"C:\poppler-24.08.0\Library\bin"

#     try:
#         if suffix == ".pdf":
#             try:
#                 reader = PdfReader(tmp_file_path)
#                 text = "\n".join([page.extract_text() or "" for page in reader.pages])
#             except Exception:
#                 text = ""
#             images = convert_from_path(tmp_file_path, poppler_path=poppler_path)
#             for img in images:
#                 image_list.append(img)
#                 ocr_img_text = pytesseract.image_to_string(img)
#                 ocr_texts_per_image.append(ocr_img_text)
#             ocr_text = " ".join(ocr_texts_per_image)

#         elif suffix == ".docx":
#             doc = DocxDocument(tmp_file_path)
#             text = "\n".join([para.text for para in doc.paragraphs])
#             rels = doc.part._rels
#             for rel in rels:
#                 rel = rels[rel]
#                 if rel.reltype == RT.IMAGE:
#                     image_data = rel.target_part.blob
#                     image = Image.open(io.BytesIO(image_data))
#                     image_list.append(image)
#                     ocr_img_text = pytesseract.image_to_string(image)
#                     ocr_texts_per_image.append(ocr_img_text)
#             ocr_text = "\n".join(ocr_texts_per_image)

#         elif suffix == ".txt":
#             with open(tmp_file_path, "r", encoding="utf-8") as f:
#                 text = f.read()

#         else:
#             text = f"Unsupported file type: {suffix}"

#     finally:
#         os.remove(tmp_file_path)

#     return {
#         "text": text.strip(),
#         "ocr_text": ocr_text.strip(),
#         "images": image_list,
#         "ocr_texts_per_image": ocr_texts_per_image
#     }


# def generate_metadata(text):
#     prompt = f"""
# You are a professional metadata assistant.

# Analyze the following document and return structured metadata in JSON format with fields:
# - title
# - summary (at least 9–10 lines in detail)
# - keywords (comma-separated)
# - topics (broad subject categories)
# - author (if mentioned)
# - document_type (e.g., research paper, report, article, etc.)

# Document Content:
# {text.strip()}
# """
#     response = llm([
#         SystemMessage(content="You are a metadata extraction assistant."),
#         HumanMessage(content=prompt)
#     ])
#     return response.content.strip()

# def summarize_ocr_text(ocr_text):
#     if not ocr_text.strip():
#         return "No OCR content found to summarize."

#     prompt = f"""
# You are a helpful assistant.

# Summarize the following OCR-extracted text in a clear and meaningful paragraph. 
# If it's a graph or chart, explain what the axes represent and describe key trends or patterns. 
# If it's a table, highlight the main comparisons or figures. 
# If it's a scanned paragraph, summarize the main idea, important names, numbers, or keywords. 
# Avoid assumptions and mention if any content is unclear.

# OCR Text:
# {ocr_text}
# """
#     response = llm([
#         SystemMessage(content="You summarize OCR-extracted content."),
#         HumanMessage(content=prompt)
#     ])
#     return response.content.strip()

# st.set_page_config(page_title="📄 AI Metadata Generator", layout="wide")
# st.title("📄 AI Metadata Generator")

# with open("style.css") as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# uploaded_file = st.file_uploader("📤 Upload a document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

# if uploaded_file:
#     with st.spinner("🧐 Extracting text from the document..."):
#         raw = extract_text_and_images(uploaded_file)
#         extracted_text = raw["text"]
#         ocr_text = raw["ocr_text"]
#         images = raw["images"]
#         ocr_texts_per_image = raw.get("ocr_texts_per_image", [])

#     with st.spinner("🤖 Generating metadata using Groq via LangChain..."):
#         metadata_output = generate_metadata(extracted_text)

#     st.success("✅ Metadata generated successfully!")
#     st.subheader("📌 Extracted Metadata")

#     try:
#         metadata_dict = json.loads(metadata_output)
#         formatted_json = json.dumps(metadata_dict, indent=2)
#     except Exception:
#         formatted_json = metadata_output

#     st.markdown(f"""<div class='scrollable-json'>{formatted_json}</div>""", unsafe_allow_html=True)

#     st.download_button(
#         label="⬇️ Download Metadata as JSON",
#         data=formatted_json,
#         file_name="metadata_output.json",
#         mime="application/json"
#     )

#     if images:
#         st.subheader("🖼️ Extracted Images from Document")
#         for idx, img in enumerate(images):
#             st.image(img, caption=f"Image {idx+1}", use_column_width=True)
#             # Download button for each image
#             img_bytes = io.BytesIO()
#             img.save(img_bytes, format="PNG")
#             st.download_button(
#                 label=f"⬇️ Download Image {idx+1}",
#                 data=img_bytes.getvalue(),
#                 file_name=f"extracted_image_{idx+1}.png",
#                 mime="image/png",
#                 key=f"download_img_{idx}"
#             )
#             ocr_img_text = ocr_texts_per_image[idx] if idx < len(ocr_texts_per_image) else ""
#             if ocr_img_text.strip():
#                 with st.expander(f"OCR Text for Image {idx+1}"):
#                     st.text_area("OCR Text", value=ocr_img_text.strip(), height=150, key=f"ocr_text_{idx}")
#                     if st.button(f"Summarize OCR for Image {idx+1}", key=f"summarize_ocr_{idx}"):
#                         with st.spinner("Summarizing OCR text..."):
#                             ocr_summary = summarize_ocr_text(ocr_img_text)
#                         st.markdown(f"**Summary:** {ocr_summary}")

#     if ocr_text.strip():
#         with st.spinner("📝 Summarizing all OCR text..."):
#             ocr_summary = summarize_ocr_text(ocr_text)

#         st.subheader("📝 OCR Text Summary (All Images)")
#         st.markdown(f"<div class='scrollable-json'>{ocr_summary}</div>", unsafe_allow_html=True)

# else:
#     st.info("📂 Please upload a file to get started.") 