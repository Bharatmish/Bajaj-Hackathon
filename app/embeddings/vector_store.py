# app/embeddings/vector_store.py

import faiss
import numpy as np
import json
import os

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

    def save(self, index_path: str, metadata_path: str):
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        faiss.write_index(self.index, index_path)
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.chunk_metadata, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, index_path: str, metadata_path: str):
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"Index file not found: {index_path}")
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")

        store = cls()
        store.index = faiss.read_index(index_path)
        with open(metadata_path, 'r', encoding='utf-8') as f:
            store.chunk_metadata = json.load(f)
        return store
