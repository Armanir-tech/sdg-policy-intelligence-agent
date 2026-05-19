from pathlib import Path
import re
from uuid import uuid4

from fastapi import APIRouter, File, Header, HTTPException, UploadFile

from app.agents.policy_workflow import run_policy_workflow
from app.core.config import settings
from app.rag.ingest import (
    UPLOAD_DIR,
    ingest_sample_documents,
    ingest_uploaded_file,
    list_indexed_documents,
    reset_collection,
)
from app.schemas.research import ResearchRequest, ResearchResponse

router = APIRouter()
CLIENT_ID_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{1,120}$")
SAFE_STEM_PATTERN = re.compile(r"[^A-Za-z0-9._-]+")


def normalize_client_id(client_id: str | None) -> str | None:
    if not client_id:
        return None
    trimmed = client_id.strip()
    if not CLIENT_ID_PATTERN.fullmatch(trimmed):
        raise HTTPException(status_code=400, detail="Invalid client id.")
    return trimmed


def safe_upload_stem(file_name: str | None) -> str:
    stem = Path(file_name or "document").stem
    cleaned = SAFE_STEM_PATTERN.sub("-", stem).strip(".-_")
    return cleaned[:48] or "document"


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
async def upload_document(
    file: UploadFile = File(...),
    x_client_id: str | None = Header(default=None),
) -> dict[str, int | str]:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".pdf", ".txt"}:
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")
    client_id = normalize_client_id(x_client_id)

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = f"{safe_upload_stem(file.filename)}-{uuid4().hex[:8]}{suffix}"
    destination = UPLOAD_DIR / safe_name

    content = await file.read()
    if len(content) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail="File is too large.")
    destination.write_bytes(content)
    chunks = ingest_uploaded_file(destination, client_id)

    return {"status": "ok", "file_name": safe_name, "chunks": chunks}


@router.get("/documents")
def documents(x_client_id: str | None = Header(default=None)) -> dict[str, list[dict[str, str | int]]]:
    return {"documents": list_indexed_documents(normalize_client_id(x_client_id))}


@router.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest) -> ResearchResponse:
    return run_policy_workflow(request.question, request.language, request.provider, request.client_id)
