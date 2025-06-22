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

---

## 🔑 Setup

1. **Set your Groq API key** in a `.env` file:
    - GROQ_API_KEY=your_groq_api_key_here


2. **Run the app:**
    - streamlit run app.py


3. **Open your browser** to the provided local URL.

---

## 📝 How It Works

1. **Upload a file** (PDF, DOCX, or TXT).
2. **Text and inline images** are extracted.
3. **OCR** is performed on each image to extract any text (if present).
4. **LLM** generates structured metadata and detailed summaries.
5. **Results** (metadata and image summaries) are shown in a modern UI, with download options.

---

## 🎨 UI & Custom Styling

- The app uses a `style.css` file for custom UI enhancements.
- Image summaries are displayed in visually distinct boxes beside each image for clarity and appeal.

---

## 💡 Notes

- Only images with non-empty OCR text are displayed and summarized.
- Summaries for each image start with “The following image ...” for clarity.
- The app is designed for easy extension and customization.

---

## 📂 Example `.env`

- GROQ_API_KEY=your_groq_api_key_here


---

## 📜 License

MIT License (or your preferred license)

---

## 👤 Author

Your Name – [samyak_m@ece.iitr.ac.in](mailto:your.email@example.com)

---

**Enjoy smarter document review and metadata extraction!**


