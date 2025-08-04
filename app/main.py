# app/main.py
from fastapi import FastAPI
from app.api.routes import router as api_router
import uvicorn

app = FastAPI(
    title="HackRx LLM Query System",
    description="LLM-powered intelligent clause retrieval system",
    version="1.0"
)

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
