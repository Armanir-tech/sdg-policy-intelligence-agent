from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.agents.policy_workflow import run_policy_workflow
from app.rag.ingest import (
    UPLOAD_DIR,
    ingest_sample_documents,
    ingest_uploaded_file,
    list_indexed_documents,
    reset_collection,
)
from app.schemas.research import ResearchRequest, ResearchResponse

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/ingest")
def ingest_documents() -> dict[str, int | str]:
    count = ingest_sample_documents()
    return {"status": "ok", "chunks": count}


@router.post("/ingest/reset")
def reset_documents() -> dict[str, int | str]:
    count = reset_collection()
    return {"status": "ok", "chunks": count}


@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)) -> dict[str, int | str]:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".pdf", ".txt"}:
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = f"{Path(file.filename or 'document').stem}-{uuid4().hex[:8]}{suffix}"
    destination = UPLOAD_DIR / safe_name

    content = await file.read()
    destination.write_bytes(content)
    chunks = ingest_uploaded_file(destination)

    return {"status": "ok", "file_name": safe_name, "chunks": chunks}


@router.get("/documents")
def documents() -> dict[str, list[dict[str, str | int]]]:
    return {"documents": list_indexed_documents()}


@router.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest) -> ResearchResponse:
    return run_policy_workflow(request.question, request.language)
