# import streamlit as st
# import os
# import tempfile
# import json
# from pathlib import Path
# from PyPDF2 import PdfReader
# from docx import Document as DocxDocument
# import pytesseract
# from dotenv import load_dotenv
# from PIL import Image
# import io
# import fitz
# from docx.opc.constants import RELATIONSHIP_TYPE as RT

# from langchain_groq import ChatGroq
# from langchain.schema import HumanMessage, SystemMessage

# import nltk
# nltk.download('punkt')
# from sumy.parsers.plaintext import PlaintextParser
# from sumy.nlp.tokenizers import Tokenizer
# from sumy.summarizers.lex_rank import LexRankSummarizer

# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# def extract_text_and_inline_images(uploaded_file):
#     suffix = Path(uploaded_file.name).suffix.lower()
#     text = ""
#     ocr_text = ""
#     image_list = []
#     ocr_texts_per_image = []

#     with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
#         tmp_file.write(uploaded_file.read())
#         tmp_file_path = tmp_file.name

#     try:
#         if suffix == ".pdf":
#             try:
#                 reader = PdfReader(tmp_file_path)
#                 text = "\n".join([page.extract_text() or "" for page in reader.pages])
#             except Exception:
#                 text = ""
#             pdf_doc = fitz.open(tmp_file_path)
#             for page in pdf_doc:
#                 images = page.get_images(full=False)
#                 for img in images:
#                     xref = img[0] if isinstance(img, tuple) else img
#                     base_image = pdf_doc.extract_image(xref)
#                     image_data = base_image["image"]
#                     image = Image.open(io.BytesIO(image_data)).convert("RGB")
#                     image_list.append(image)
#                     ocr_img_text = pytesseract.image_to_string(image)
#                     ocr_texts_per_image.append(ocr_img_text)
#             ocr_text = "\n".join(ocr_texts_per_image)
#         elif suffix == ".docx":
#             doc = DocxDocument(tmp_file_path)
#             text = "\n".join([para.text for para in doc.paragraphs])
#             rels = doc.part._rels
#             for rel in rels:
#                 rel = rels[rel]
#                 if rel.reltype == RT.IMAGE:
#                     image_data = rel.target_part.blob
#                     image = Image.open(io.BytesIO(image_data)).convert("RGB")
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
#         try:
#             os.remove(tmp_file_path)
#         except PermissionError:
#             pass

#     return {
#         "text": text.strip(),
#         "ocr_text": ocr_text.strip(),
#         "images": image_list,
#         "ocr_texts_per_image": ocr_texts_per_image
#     }

# # --- Free extractive summarization using Sumy ---
# def extractive_summary(text, num_sentences=20):
#     parser = PlaintextParser.from_string(text, Tokenizer("english"))
#     summarizer = LexRankSummarizer()
#     summary_sentences = summarizer(parser.document, num_sentences)
#     summary = " ".join(str(sentence) for sentence in summary_sentences)
#     return summary

# def generate_metadata(summarized_text):
#     llm = ChatGroq(
#         model="llama3-8b-8192",
#         api_key=GROQ_API_KEY
#     )
#     prompt = f"""
# You are a professional and wonderful metadata assistant.

# Analyze the following document summary and return structured metadata in JSON format with fields:
# - title
# - summary (at least 10-15 lines in detail covering all important points)
# - keywords (comma-separated)
# - topics (broad subject categories)
# - author (if mentioned)
# - document_type

# Document Summary:
# {summarized_text}
# """
#     try:
#         response = llm([
#             SystemMessage(content="You are a metadata extraction assistant."),
#             HumanMessage(content=prompt)
#         ])
#         return response.content.strip()
#     except Exception as e:
#         st.error(f"Metadata extraction failed: {e}")
#         return '{"error": "Metadata extraction failed."}'

# def summarize_ocr_text(ocr_text):
#     if not ocr_text.strip():
#         return "No OCR content found to summarize."
#     llm = ChatGroq(
#         model="llama3-8b-8192",
#         api_key=GROQ_API_KEY
#     )
#     prompt = (
#         "You are a professional assistant. "
#         "Start your response with 'The following image ...'. "
#         "Summarize the following OCR-extracted content in a clear, well-organized, and visually appealing markdown format. "
#         "Your summary should include:\n"
#         "- A short title or heading for the content\n"
#         "- Key points or highlights as a bullet list\n"
#         "- Detected names, dates, numbers, or keywords (if any)\n"
#         "- A concise paragraph summarizing the main idea or purpose\n"
#         "If the content is a graph or chart, explain axes and key trends. "
#         "If it's a table, highlight main comparisons or figures. "
#         "If it's a scanned paragraph, summarize the main idea. "
#         "Avoid assumptions. If content is unclear, mention it.\n\n"
#         "If it's none of the above, just describe the content of picture, background, etc.\n"
#         f"OCR Text:\n{ocr_text}"
#     )
#     try:
#         response = llm([
#             SystemMessage(content="You summarize OCR-extracted content in structured markdown."),
#             HumanMessage(content=prompt)
#         ])
#         return response.content.strip()
#     except Exception as e:
#         return f"OCR summarization failed: {e}"

# # --- Streamlit UI ---
# st.set_page_config(page_title="📄 AI Metadata Generator (RAG)", layout="wide")
# st.title("📄 AI Metadata Generator with Extractive & LLM Summarization")

# st.markdown("""
# <div style='background-color:#f0f2f6; padding: 1em; border-radius: 10px; margin-bottom:1em;'>
#     <h3>Upload a document (PDF, DOCX, or TXT) and generate structured metadata using free extractive summarization (Sumy) and Groq LLM! Inline images are also OCR'd and summarized.</h3>
# </div>
# """, unsafe_allow_html=True)

# uploaded_file = st.file_uploader("📤 Upload a document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

# if uploaded_file:
#     with st.spinner("Extracting text and images..."):
#         raw = extract_text_and_inline_images(uploaded_file)
#         extracted_text = raw["text"]
#         images = raw["images"]
#         ocr_texts_per_image = raw.get("ocr_texts_per_image", [])

#     st.info("Generating extractive summary (free, local)...")
#     with st.spinner("Summarizing document with Sumy..."):
#         extractive_sum = extractive_summary(extracted_text, num_sentences=30)
#     st.markdown(f"<div class='summary-box'>{extractive_sum}</div>", unsafe_allow_html=True)

#     st.info("Generating metadata from summary using Groq Llama...")
#     with st.spinner("Generating metadata..."):
#         metadata_output = generate_metadata(extractive_sum)

#     st.success("✅ Metadata generated successfully!")
#     st.subheader("📌 Extracted Metadata")

#     try:
#         metadata_dict = json.loads(metadata_output)
#         formatted_json = json.dumps(metadata_dict, indent=2)
#     except Exception:
#         formatted_json = metadata_output

#     st.markdown(f"""<div class='scrollable-json'><pre>{formatted_json}</pre></div>""", unsafe_allow_html=True)
#     st.download_button(
#         label="⬇️ Download Metadata as JSON",
#         data=formatted_json,
#         file_name="metadata_output.json",
#         mime="application/json"
#     )

#     if images:
#         st.subheader("🖼️ Inline Image Summaries")
#         for idx, img in enumerate(images):
#             ocr_img_text = ocr_texts_per_image[idx] if idx < len(ocr_texts_per_image) else ""
#             if ocr_img_text.strip():
#                 st.markdown(f"---\n### 🖼️ Image {idx+1}")
#                 col1, col2 = st.columns([1, 2])
#                 with col1:
#                     st.image(img, caption=f"Image {idx+1}", use_container_width=True)
#                 with col2:
#                     with st.spinner(f"Summarizing OCR text for Image {idx+1}..."):
#                         summary = summarize_ocr_text(ocr_img_text)
#                     st.markdown(f"<div class='summary-box'>{summary}</div>", unsafe_allow_html=True)
#                     with st.expander("Show Raw OCR Text"):
#                         st.code(ocr_img_text)
# else:
#     st.info("📂 Please upload a file to get started.")

# # --- Optional: Add CSS for summary boxes ---
# st.markdown("""
# <style>
# .summary-box {
#     background: linear-gradient(90deg, #f7fafc 0%, #e3e9f7 100%);
#     border-left: 8px solid #4F8BF9;
#     border-radius: 12px;
#     padding: 1.5em 1.5em 1.5em 2em;
#     margin: 1.5em 0;
#     box-shadow: 0 2px 8px rgba(79,139,249,0.07);
#     font-size: 1.13em;
#     color: #22223b;
#     font-family: 'Segoe UI', 'Roboto', sans-serif;
#     transition: box-shadow 0.2s;
# }
# .summary-box:hover {
#     box-shadow: 0 6px 24px rgba(79,139,249,0.12);
# }
# .scrollable-json {
#     max-height: 300px;
#     overflow-y: auto;
#     background: #f4f6fb;
#     border-radius: 8px;
#     padding: 1em;
#     margin-bottom: 1em;
# }
# </style>
# """, unsafe_allow_html=True)
