# app/documents/doc_ingestor.py
from app.documents.downloader import download_document
from app.documents.doc_type_detector import detect_file_type
from app.documents.pdf_parser import extract_pdf_text
from app.documents.docx_parser import extract_docx_text
from app.documents.email_parser import extract_email_text

def ingest_document(url: str) -> list[dict]:
    filepath = download_document(url)
    doc_type = detect_file_type(filepath)

    if doc_type == 'pdf':
        return extract_pdf_text(filepath)
    elif doc_type == 'docx':
        return extract_docx_text(filepath)
    elif doc_type == 'email':
        return extract_email_text(filepath)
    else:
        raise Exception("Unsupported document type")
