# 📄 AI Metadata & Image Summarizer

A cutting-edge Streamlit web application that enables users to effortlessly upload PDF, DOCX, or TXT documents, automatically extracting both textual content and embedded inline images. The app performs OCR on extracted images to uncover any text they contain and leverages Groq’s powerful LLM (LLama3) to generate comprehensive, structured metadata along with visually rich, context-aware summaries for each image. This seamless integration of document processing, OCR, and generative AI delivers an intuitive and efficient experience for detailed document analysis and review.

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

- The app incorporates a custom style.css file to enhance the overall look and feel, ensuring a modern and cohesive user experience.

- Each image summary is presented in a visually distinct, styled box positioned beside its corresponding image, making it easy to compare visuals and insights at a glance.

- Clean layouts, intuitive navigation, and subtle visual accents help users focus on the content and results, providing both clarity and aesthetic appeal throughout the application.

---

## 💡 Notes

- Only images containing meaningful OCR-extracted text are displayed and summarized, ensuring that users see relevant insights without unnecessary clutter.

- Each image summary begins with the phrase “The following image ...” to provide clear context and improve readability.

- The app’s modular design and clean codebase make it straightforward to extend or customize features, allowing for easy adaptation to evolving user needs or integration with additional AI services.

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
