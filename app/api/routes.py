# app/api/routes.py


from fastapi import APIRouter, Header, HTTPException
from app.api.schemas import RunRequest

from app.documents.doc_ingestor    import ingest_document
from app.embeddings.chunker         import chunk_text
from app.embeddings.embedder        import embed_text
from app.embeddings.vector_store    import VectorStore
from app.embeddings.metadata_store  import build_metadata
from app.search.retrieval_pipeline  import get_top_chunks_for_query
from app.llm.llm_reasoner           import run_reasoning_llm

import os
from dotenv import load_dotenv
load_dotenv()

SECRET_TOKEN = os.getenv("HACKRX_API_TOKEN")

router = APIRouter()

# ─────────────────────────────────────────────────────────────────────────
@router.post("/hackrx/run")
def run_pipeline(
    request: RunRequest,
    authorization: str = Header(
        ...,
        alias="Authorization",
        description="Bearer token required (format: Bearer <token>)"
    )
):
    # 1. Validate Bearer token
    if not authorization.startswith("Bearer ") or not authorization.endswith(SECRET_TOKEN):
        raise HTTPException(status_code=401, detail="Invalid or missing authorization token")

    # 2. Ingest document
    try:
        raw_pages = ingest_document(request.documents)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Document ingestion failed: {exc}")

    # 3. Chunk & embed
    chunks     = chunk_text(raw_pages)
    metadata   = build_metadata(chunks)
    embeddings = [embed_text(c["text"]) for c in chunks]

    store = VectorStore()
    store.add(embeddings, metadata)

    # 4. Answer each question
    answers: list[str] = []

    for question in request.questions:
        try:
            top_chunks = get_top_chunks_for_query(question, store, top_k=5)
            sentence   = run_reasoning_llm(question, top_chunks)  # one fluent sentence
            answers.append(sentence)
        except Exception as exc:
            answers.append(f"Error answering: {question} – {exc}")

    return {"answers": answers}
