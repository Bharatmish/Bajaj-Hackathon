# app/search/semantic_search.py
from app.embeddings.embedder import embed_text
from app.embeddings.vector_store import VectorStore

def retrieve_relevant_chunks(vector_store: VectorStore, query: str, top_k: int = 5) -> list[dict]:
    query_embedding = embed_text(query)
    results = vector_store.search(query_embedding, top_k=top_k)
    return results
