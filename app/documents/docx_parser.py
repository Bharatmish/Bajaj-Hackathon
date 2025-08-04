# app/documents/docx_parser.py
from docx import Document

def extract_docx_text(filepath: str) -> list[dict]:
    doc = Document(filepath)
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return [{
        "page": 1,
        "text": text
    }]
