# 📄 AI Metadata & Image Summarizer

A modern Streamlit web app that lets you upload PDF, DOCX, or TXT files, automatically extracts text and inline images, performs OCR on images, and uses Groq's LLM (LLama3) to generate rich metadata and visually appealing, smart summaries for each image.

---

## 🚀 Features

- **Upload** PDF, DOCX, or TXT files
- **Extracts** all text and inline (embedded) images
- **Performs OCR** on images to extract any text present
- **LLM-powered metadata extraction** (title, summary, keywords, topics, author, type)
- **Smart, markdown-formatted summaries** for each image
- **Download metadata as JSON**
- **Modern, user-friendly Streamlit interface**

---

## 🛠️ Requirements

- **Python** 3.8+
- **Tesseract OCR** (must be installed and the path set)
    - [Tesseract Download](https://github.com/tesseract-ocr/tesseract)
- **Groq API key** for LLM access

---

## 📦 Key Python Packages

| Package                | Purpose                                      |
|------------------------|----------------------------------------------|
| streamlit              | Web app framework                            |
| os, tempfile, io, json, pathlib | File handling                     |
| PyPDF2                 | PDF text extraction                          |
| python-docx            | DOCX text/image extraction                   |
| pytesseract            | OCR on images                                |
| langchain_groq         | LLM API integration (LLama3 via Groq)        |
| langchain.schema       | LLM message formatting                       |
| dotenv                 | Loads API keys from `.env`                   |
| Pillow (PIL)           | Image processing                             |
| fitz (PyMuPDF)         | Extracts inline images from PDF              |
| docx.opc.constants     | DOCX image relationship constants            |

---

## ⚡ Installation

# Clone the repository
    - git clone https://github.com/yourusername/ai-metadata-summarizer.git
    - cd ai-metadata-summarizer

# Install Python dependencies
    - pip install -r requirements.txt


**Install Tesseract:**
- Download and install from [here](https://github.com/tesseract-ocr/tesseract)
- Set the path in your script if needed (see code).

---

## 🔑 Setup

1. **Create a `.env` file** in the project root with your Groq API key:
    ```
    GROQ_API_KEY=your_groq_api_key_here
    ```

2. **Run the app:**
    ```
    streamlit run app.py
    ```

3. **Open your browser** to the local URL provided by Streamlit.

---

## 📝 How It Works

1. **Upload a file** (PDF, DOCX, or TXT).
2. **Text and inline images** are extracted from the document.
3. **OCR** is performed on each image to extract any text present.
4. **LLM** generates structured metadata and detailed, markdown-formatted summaries.
5. **Results** (metadata and image summaries) are displayed in a modern UI, with download options.

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

Samyak Mahapatra – [samyak_m@ece.iitr.ac.in](mailto:samyak_m@ece.iitr.ac.in)

---

**Enjoy smarter document review and metadata extraction!**
