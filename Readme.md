# 📄 AI Metadata Generator with Groq Llama 3.3 70B Versatile model

A Streamlit app to **extract, summarize, and generate structured metadata from PDF, DOCX, and TXT documents** using the Groq Llama-3.3-70B-Versatile model. The app also extracts and summarizes text from inline images using OCR. Note that OCR image extraction is only possible for DOCX and PDF files, as it is not possible to have images in TXT files.

---

## 🚀 Features

- **Document Upload:** Supports PDF, DOCX, and TXT files.
- **Text Extraction:** Extracts all text from uploaded documents.
- **Image Extraction & OCR:** Extracts inline images and runs OCR (Optical Character Recognition) to get text from images.
- **Hierarchical Summarization:** Summarizes large documents chunk-by-chunk, then combines and further summarizes to fit within model token limits.
- **Metadata Generation:** Produces detailed, structured metadata (title, summary, keywords, topics, author, document type) using the document summary.
- **Image OCR Summarization:** Each extracted image's OCR text is summarized in a clear, markdown-formatted style.
- **Downloadable Metadata:** Download the generated metadata as a JSON file.
- **Modern UI:** Clean, wide-layout Streamlit interface with custom CSS support.

---

## 🛠️ Required Packages

Install all dependencies with:

   - pip install streamlit python-dotenv PyPDF2 python-docx pytesseract pillow pymupdf langchain langchain-groq


**Additional requirements:**
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) must be installed and available on your system path.
- A valid Groq API key (set as `GROQ_API_KEY` in your `.env` file).

---

## 📂 How It Works

1. **Upload a file** (PDF, DOCX, or TXT).
2. **Extract text and images:** The app parses the document, extracting all text and any inline images.
3. **OCR on images:** Each image is processed with Tesseract OCR to extract text.
4. **Hierarchical Summarization:**  
   - The document text is split into manageable chunks (approx. 700 tokens each).
   - Each chunk is summarized using Groq Llama-3.3-70b-versatile.
   - All summaries are combined; if the combined summary is too long, it is summarized again to ensure it fits within the token limit.
5. **Metadata Generation:**  
   - The final summary is passed to the Groq model to generate rich metadata in JSON format.
6. **Image Summaries:**  
   - Each image's OCR text is summarized separately and displayed alongside the image.
7. **Download & View:**  
   - View the metadata and summary in the streamlit app, and download the metadata as JSON.

---

## 🧠 Hierarchical Summarization

**Hierarchical summarization** is a technique for summarizing large documents that exceed the token limits of language models. It works as follows:

- The document is divided into smaller chunks, each within the model's token limit.
- Each chunk is summarized individually, extracting key points, keywords, names, terminologies, dates, and numbers.
- All chunk summaries are combined. If the combined summary still exceeds the token limit, it is summarized again.
- This process ensures complete coverage of the document and produces a concise, information-rich summary suitable for further processing, such as metadata extraction.

**Advantages:**
- Handles documents of any size.
- Preserves important details from all sections.
- Produces high-quality, concise summaries for downstream tasks.

---

## 📝 Example Metadata Output

{
"title": "Sample Document Title",
"summary": "This document covers ... (detailed summary, 15-20 lines)",
"keywords": "AI, metadata, summarization, OCR, PDF",
"topics": "Artificial Intelligence, Document Processing",
"author": "John Doe",
"document_type": "Research Paper"
}


---

## 🖼️ Image Summaries

Each extracted image is displayed with:
- The summarized OCR content (as markdown)
- The raw OCR text (expandable)
- The original image

---

## 💻 Usage

1. **Set up your environment:**
   - Install dependencies (see above).
   - Install Tesseract OCR and ensure it is on your system path.
   - Create a `.env` file with your Groq API key:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```

2. **Run the app:**
   - streamlit run your_app_file.py


3. **Upload a document(PDF,TXT OR DOCX FORMAT) and explore the results.**

---

## 📦 File Structure

- `your_app_file.py` — Main Streamlit app.
- `style.css` — (Optional) Custom CSS for app styling.
- `.env` — Your Groq API key.

---

## ✨ Customization

- **Model selection:** The app uses `llama-3.3-70b-versatile` by default for all summarization and metadata tasks. You can change the model string in the code if needed.
- **Chunk size:** Adjust the `chunk_size` in `chunk_text_by_tokens` for different token limits.
- **Prompt engineering:** Modify the prompts in `summarize_with_groq` or `generate_metadata` for different summary or metadata styles.

---

## ☁️ Deployment Notes (Streamlit Cloud & Tesseract)

deployment_notes:
  - **Tesseract OCR is not available on Streamlit Community Cloud.**  
     This means OCR features (image text extraction and summarization) will **not work** on Streamlit Cloud deployments.  
     The rest of the app (text extraction, summarization, metadata generation) will continue to work as expected."

  - **Workaround:** For full OCR functionality, run the app locally on your machine with Tesseract installed,  
     or deploy to a cloud VM (like Render, Railway, or EC2) where you can install system-level packages."

  - **Tesseract path setting limitation:**  
     The Tesseract path (`tesseract_cmd`) must be manually set in the code, and it varies by platform (Windows vs. Linux).  
     On platforms like Streamlit Cloud, you cannot control the Tesseract installation path — this results in `TesseractNotFoundError`  
     even if the Python package is available."

  - **Unsupported image formats:**  
     On Linux (including Streamlit Cloud), WMF/EMF image formats cannot be processed by Pillow.  
     These are silently skipped to prevent application crashes."


---

## 🎥 Demo Video

A short demonstration video (2 minutes) showing how to use the app is available here:

**[Watch the demo video](https://drive.google.com/file/d/1IofNyNkADOQaViUs2y65HxwWS_m4t6hm/view?usp=sharing)**

---

## 📝 License

This project is open-source and free to use for non-commercial and research purposes.

---

## 🙏 Acknowledgements

- Meta for Llama 3 models
- Groq for providing fast, scalable LLM inference
- Open-source Python community for PDF, DOCX, and OCR tools

---
