# app/documents/email_parser.py
import extract_msg

def extract_email_text(filepath: str) -> list[dict]:
    msg = extract_msg.Message(filepath)
    body = msg.body or msg.htmlBody or ""
    return [{
        "page": 1,
        "text": body.strip()
    }]
