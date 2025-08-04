# app/embeddings/vector_store.py
import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim: int = 384):
        self.index = faiss.IndexFlatL2(dim)
        self.chunk_metadata = []

    def add(self, embeddings: list, metadata: list):
        self.index.add(np.array(embeddings).astype('float32'))
        self.chunk_metadata.extend(metadata)

    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        D, I = self.index.search(np.array([query_embedding]).astype('float32'), top_k)
        return [self.chunk_metadata[i] for i in I[0] if i < len(self.chunk_metadata)]
