# 📄 AI Metadata & Image Summarizer

A modern Streamlit web app for uploading PDF, DOCX, or TXT files, extracting text and inline images, performing OCR on images, and generating rich metadata and smart, visually appealing summaries for each image using Groq's LLM.

---

## 🚀 Features

- **Upload PDF, DOCX, or TXT files**
- **Extracts all text and inline (embedded) images**
- **Performs OCR on images** to extract any text present
- **LLM-powered metadata extraction** (title, summary, keywords, topics, author, type)
- **Smart, markdown-formatted summaries for each image**
- **Download metadata as JSON**
- **Modern, user-friendly Streamlit interface**

---

## 🛠️ Requirements

- Python 3.8+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (must be installed and the path set)
- [Poppler](http://blog.alivate.com.au/poppler-windows/) (for PDF image extraction, if running on Windows)
- Groq API key

---

## 📦 Important Python Packages Used

- `streamlit` – Web app framework
- `os`, `tempfile`, `io`, `json`, `pathlib` – File handling
- `PyPDF2` – PDF text extraction
- `python-docx` – DOCX text/image extraction
- `pytesseract` – OCR on images
- `langchain_groq` – LLM API integration (LLama3 via Groq)
- `langchain.schema` – LLM message formatting
- `dotenv` – Loads API keys from `.env`
- `Pillow (PIL)` – Image processing
- `fitz` (PyMuPDF) – Extracts inline images from PDF
- `docx.opc.constants` – DOCX image relationship constants

---

## ⚡ Installation

# Clone the repository
    - git clone https://github.com/yourusername/ai-metadata-summarizer.git
    - cd ai-metadata-summarizer

# Install Python dependencies
    - pip install -r requirements.txt


**Install Tesseract:**
- [Tesseract Download](https://github.com/tesseract-ocr/tesseract)
- Set the path in your script if needed.

**Install Poppler (for Windows):**
- [Poppler Download](http://blog.alivate.com.au/poppler-windows/)
- Add Poppler's `bin` folder to your PATH.

---

## 🔑 Setup

1. **Set your Groq API key** in a `.env` file:
    - GROQ_API_KEY=your_groq_api_key_here


2. **Run the app:**
    - streamlit run app.py
