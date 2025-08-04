# app/embeddings/metadata_store.py
def build_metadata(chunks: list[dict]) -> list[dict]:
    return [
        {
            "chunk_id": chunk["chunk_id"],
            "page": chunk["page"],
            "text": chunk["text"]
        }
        for chunk in chunks
    ]
