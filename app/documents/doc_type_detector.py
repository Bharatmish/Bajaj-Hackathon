# app/documents/doc_type_detector.py
import mimetypes

def detect_file_type(filepath: str) -> str:
    mimetype, _ = mimetypes.guess_type(filepath)
    if mimetype:
        if 'pdf' in mimetype:
            return 'pdf'
        elif 'msword' in mimetype or 'wordprocessingml' in mimetype:
            return 'docx'
        elif 'message' in mimetype or filepath.endswith('.eml') or filepath.endswith('.msg'):
            return 'email'
    raise ValueError("Unsupported file type")
