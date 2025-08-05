# app/api/routes.py

from fastapi import APIRouter, Header, HTTPException
from app.api.schemas import RunRequest

from app.documents.doc_ingestor import ingest_document
from app.embeddings.chunker import chunk_text
from app.embeddings.embedder import embed_text
from app.embeddings.vector_store import VectorStore
from app.embeddings.metadata_store import build_metadata
from app.search.retrieval_pipeline import get_top_chunks_for_query
from app.llm.llm_reasoner import run_reasoning_llm

import os
from dotenv import load_dotenv

load_dotenv()
SECRET_TOKEN = os.getenv("HACKRX_API_TOKEN")

router = APIRouter()

# File paths for saved index
INDEX_PATH = "index/policy_faiss.index"
META_PATH = "index/policy_chunks.json"

# Cache in memory after first load
vector_store: VectorStore = None

@router.post("/hackrx/run")
def run_pipeline(
    request: RunRequest,
    authorization: str = Header(..., alias="Authorization")
):
    # 1. Validate Bearer token
    if not authorization.startswith("Bearer ") or not authorization.endswith(SECRET_TOKEN):
        raise HTTPException(status_code=401, detail="Invalid or missing authorization token")

    global vector_store

    # 2. Try loading saved index + metadata (already processed?)
    if vector_store is None and os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
        try:
            vector_store = VectorStore.load(INDEX_PATH, META_PATH)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to load index: {e}")

    # 3. If not already loaded, do full processing (first time only)
    if vector_store is None:
        try:
            raw_pages = ingest_document(request.documents)
            chunks = chunk_text(raw_pages)
            metadata = build_metadata(chunks)
            embeddings = [embed_text(c["text"]) for c in chunks]

            vector_store = VectorStore()
            vector_store.add(embeddings, metadata)

            # Ensure 'index' folder exists
            os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
            vector_store.save(INDEX_PATH, META_PATH)

        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Document processing failed: {exc}")

    # 4. Answer the questions using saved/loaded index
    answers = []
    for question in request.questions:
        try:
            top_chunks = get_top_chunks_for_query(question, vector_store, top_k=5)
            response = run_reasoning_llm(question, top_chunks)
            answers.append(response)
        except Exception as exc:
            answers.append(f"Error answering: {question} – {exc}")

    return {"answers": answers}
