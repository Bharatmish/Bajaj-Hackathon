# app/embeddings/embedder.py
from sentence_transformers import SentenceTransformer
from functools import lru_cache

@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str):
    model = get_model()
    return model.encode(text)

