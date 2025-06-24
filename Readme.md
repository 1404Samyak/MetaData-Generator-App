# 📄 AI Metadata Generator with Groq Llama 3.3 70B Versatile

A Streamlit app to **extract, summarize, and generate structured metadata** from PDF, DOCX, and TXT documents using the Groq Llama-3.3-70B-Versatile model. The app also extracts and summarizes text from inline images using OCR.

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

    - pip install streamlit python-dotenv PyPDF2 python-docx pytesseract pillow pymupdf langchain-groq


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
   - View the metadata and summary in the app, and download the metadata as JSON.

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

*Reference: [Hierarchical Summarization, ACL Anthology][4]*

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


3. **Upload a document and explore the results.**

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

## 📚 References

- [Hierarchical Summarization: Scaling Up Multi-Document Summarization](https://aclanthology.org/anthology-files/anthology-files/pdf/P/P14/P14-1085.xhtml)[4]
- [PyPDF2 Documentation](https://pypdf2.readthedocs.io/)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [Pytesseract Documentation](https://pypi.org/project/pytesseract/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

## 📝 License

This project is open-source and free to use for non-commercial and research purposes.

---

## Acknowledgements

- Meta for Llama 3 models
- Groq for providing fast, scalable LLM inference
- Open-source Python community for PDF, DOCX, and OCR tools

---

