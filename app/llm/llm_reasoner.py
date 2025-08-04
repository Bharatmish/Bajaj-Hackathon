# app/llm/llm_reasoner.py
"""
Build prompt → call Gemini → return ONE fluent sentence that answers the query.
No JSON parsing is required from the model; we only need the sentence.
"""

from typing import List, Dict
from app.llm.llm_client import call_google_gemini


# ── Prompt builder ───────────────────────────────────────────────────────
def build_prompt(query: str, chunks: List[Dict]) -> str:
    """
    Assemble a prompt with retrieved document chunks and the question.
    """
    context = "".join(
        f"[{c['chunk_id']} | Page {c['page']}]\n{c['text']}\n\n"
        for c in chunks
    )
    with open("app/llm/prompt_template.txt", encoding="utf-8") as f:
        template = f.read()

    return template.format(query=query.strip(), retrieved_docs=context.strip())


# ── Main helper used by the pipeline ─────────────────────────────────────
def run_reasoning_llm(query: str, retrieved_chunks: List[Dict]) -> str:
    """
    Calls Gemini and returns a single, fluent answer sentence.

    Strips ```json … ``` or ```text … ``` code-fences if Gemini adds them.
    """
    prompt = build_prompt(query, retrieved_chunks)
    answer = call_google_gemini(prompt).strip()

    # Remove leading code-fence if present
    if answer.startswith("```"):
        answer = answer.strip("`").lstrip("json").lstrip("text").strip()

    return answer
