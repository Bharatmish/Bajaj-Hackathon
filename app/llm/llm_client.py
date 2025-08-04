# app/llm/llm_client.py
"""
Thin wrapper around the Gemini 1.5 Flash REST API.
Returns raw text (no markdown / code fences).
"""

import os
import requests
from dotenv import load_dotenv

# ── Load .env ─────────────────────────────────────────────────────────────
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")        # put your key in .env

# ── Main call helper ─────────────────────────────────────────────────────
def call_google_gemini(prompt: str) -> str:
    if not API_KEY:
        raise ValueError("GOOGLE_API_KEY not set in environment (.env)")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-1.5-flash:generateContent"
    )

    body = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,       # lower → more deterministic JSON
            "topK":        1,
            "topP":        1,
            "maxOutputTokens": 512
        }
    }

    resp = requests.post(url, params={"key": API_KEY},
                         headers={"Content-Type": "application/json"},
                         json=body, timeout=60)

    if resp.status_code != 200:
        raise RuntimeError(
            f"Gemini API error {resp.status_code}: {resp.text[:200]}"
        )

    try:
        return (
            resp.json()
            ["candidates"][0]
            ["content"]["parts"][0]
            ["text"]
            .strip()
        )
    except (KeyError, IndexError) as exc:
        raise RuntimeError(
            f"Unexpected Gemini response structure → {exc}\n{resp.text[:400]}"
        )
