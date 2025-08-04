# app/documents/pdf_parser.py
from PyPDF2 import PdfReader

def extract_pdf_text(filepath: str) -> list[dict]:
    reader = PdfReader(filepath)
    results = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            results.append({
                "page": i + 1,
                "text": text.strip()
            })
    return results
