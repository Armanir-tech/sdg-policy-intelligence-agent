from pathlib import Path
import re
from uuid import uuid4

from fastapi import APIRouter, File, Header, HTTPException, Request, UploadFile

from app.agents.policy_workflow import run_policy_workflow
from app.core.config import settings
from app.core.rate_limit import check_rate_limit
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


def request_key(request: Request, client_id: str | None, action: str) -> str:
    host = request.client.host if request.client else "unknown"
    return f"{action}:{client_id or host}"


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
    request: Request,
    file: UploadFile = File(...),
    x_client_id: str | None = Header(default=None),
) -> dict[str, int | str]:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".pdf", ".txt"}:
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")
    client_id = normalize_client_id(x_client_id)
    check_rate_limit(
        request_key(request, client_id, "upload"),
        settings.upload_rate_limit,
        settings.upload_rate_window_seconds,
    )

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
def research(payload: ResearchRequest, request: Request) -> ResearchResponse:
    check_rate_limit(
        request_key(request, payload.client_id, "research"),
        settings.research_rate_limit,
        settings.research_rate_window_seconds,
    )
    return run_policy_workflow(payload.question, payload.language, payload.provider, payload.client_id)
