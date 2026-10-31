from functools import lru_cache
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.core import Support
from pathlib import Path as StaticPath
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Support RAG Desk")


@lru_cache
def service():
    return Support()


class Question(BaseModel):
    tenant: str = Field(pattern="^(acme|beacon)$")
    question: str = Field(min_length=1, max_length=2000)
    mode: str = Field(default="fixture", pattern="^(fixture|local)$")


@app.post("/api/ask")
def ask(q: Question):
    try:
        return service().ask(q.tenant, q.question, q.mode)
    except ValueError as e:
        raise HTTPException(422, str(e)) from e


@app.get("/api/documents/{tenant}")
def docs(tenant: str):
    try:
        return service().docs(tenant)
    except ValueError as e:
        raise HTTPException(404, str(e)) from e


@app.get("/api/tickets/{tenant}")
def tickets(tenant: str):
    try:
        return service().tickets(tenant)
    except ValueError as e:
        raise HTTPException(404, str(e)) from e


# Serve the compiled React client after all API routes.

if StaticPath("web/dist").is_dir():
    app.mount("/", StaticFiles(directory="web/dist", html=True), name="web")
