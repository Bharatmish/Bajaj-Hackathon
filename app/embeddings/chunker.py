# app/embeddings/chunker.py
def chunk_text(document: list[dict], max_words=100, overlap=20) -> list[dict]:
    chunks = []
    chunk_id = 0

    for page in document:
        words = page["text"].split()
        for i in range(0, len(words), max_words - overlap):
            chunk_words = words[i:i + max_words]
            chunk_text = " ".join(chunk_words).strip()

            if chunk_text:
                chunks.append({
                    "chunk_id": f"chunk_{chunk_id}",
                    "text": chunk_text,
                    "page": page["page"]
                })
                chunk_id += 1
    return chunks
