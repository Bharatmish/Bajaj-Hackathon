from app.llm.llm_reasoner import run_reasoning_llm
from app.documents.doc_ingestor import ingest_document
from app.embeddings.chunker import chunk_text
from app.embeddings.embedder import embed_text
from app.embeddings.vector_store import VectorStore
from app.embeddings.metadata_store import build_metadata
from app.search.retrieval_pipeline import get_top_chunks_for_query

DOC = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09:11:24Z&se=2027-07-05T09:11:00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT/jUHNO7HzQ="
QUESTION = "What is the grace period for premium payment?"

pages  = ingest_document(DOC)
chunks = chunk_text(pages)
meta   = build_metadata(chunks)
vecs   = [embed_text(c["text"]) for c in chunks]

store = VectorStore()
store.add(vecs, meta)

top_chunks = get_top_chunks_for_query(QUESTION, store, top_k=5)
resp = run_reasoning_llm(QUESTION, top_chunks)

print("\n🟢 PARSED RESPONSE:\n", resp)
