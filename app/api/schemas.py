# app/api/schemas.py

from pydantic import BaseModel
from typing import List

class RunRequest(BaseModel):
    documents: str
    questions: List[str]
