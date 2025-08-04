# app/search/retrieval_pipeline.py
from app.search.semantic_search import retrieve_relevant_chunks
from app.embeddings.vector_store import VectorStore

def get_top_chunks_for_query(query: str, vector_store: VectorStore, top_k: int = 5) -> list[dict]:
    return retrieve_relevant_chunks(vector_store, query, top_k=top_k)

def get_context_string(chunks: list[dict]) -> str:
    # Combine retrieved chunks into a single context string
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"Clause {i+1} (Page {chunk['page']}):\n{chunk['text']}\n\n"
    return context.strip()
