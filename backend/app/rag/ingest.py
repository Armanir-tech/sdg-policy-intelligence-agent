from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import chromadb
from pypdf import PdfReader

from app.core.config import settings
from app.rag.local_embeddings import LocalHashEmbedding


DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "sample_reports"
UPLOAD_DIR = Path(__file__).resolve().parents[3] / "data" / "uploads"
SAMPLE_FILES = {"sdg_financing.txt", "digital_inclusion.txt"}


def public_document_label(file_name: str, source_type: str, index: int | None = None) -> str:
    if source_type == "sample":
        return file_name
    suffix = f" {index}" if index is not None else ""
    return f"Uploaded document{suffix}"


def read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append(f"Page {index}\n{text.strip()}")
    return "\n\n".join(pages)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def chunk_text(text: str, max_chars: int = 760, overlap: int = 120) -> list[str]:
    clean = " ".join(text.split())
    if not clean:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(clean):
        end = min(start + max_chars, len(clean))
        chunk = clean[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(clean):
            break
        start = max(0, end - overlap)
    return chunks


def get_collection():
    client = chromadb.PersistentClient(path=settings.chroma_dir)
    return client.get_or_create_collection(
        name="policy_reports",
        embedding_function=LocalHashEmbedding(),
        metadata={"description": "Development policy report chunks"},
    )


def ingest_sample_documents() -> int:
    collection = get_collection()
    existing = collection.count()
    if existing > 0:
        return existing

    documents: list[str] = []
    ids: list[str] = []
    metadatas: list[dict[str, str | int]] = []

    for path in sorted(DATA_DIR.glob("*")):
        if path.suffix.lower() == ".pdf":
            text = read_pdf(path)
        elif path.suffix.lower() == ".txt":
            text = read_text(path)
        else:
            continue

        title = path.stem.replace("_", " ").title()
        for line in text.splitlines():
            if line.startswith("Title:"):
                title = line.replace("Title:", "", 1).strip()
                break

        for index, chunk in enumerate(chunk_text(text), start=1):
            ids.append(f"{path.stem}-{index}-{uuid4().hex[:8]}")
            documents.append(chunk)
            metadatas.append(
                {
                    "title": title,
                    "location": f"{path.name} chunk {index}",
                    "file_name": path.name,
                    "source_type": "sample",
                }
            )

    if documents:
        collection.add(ids=ids, documents=documents, metadatas=metadatas)

    return collection.count()


def ingest_uploaded_file(path: Path, client_id: str | None = None) -> int:
    collection = get_collection()

    if path.suffix.lower() == ".pdf":
        text = read_pdf(path)
    elif path.suffix.lower() == ".txt":
        text = read_text(path)
    else:
        raise ValueError("Only PDF and TXT files are supported.")

    title = path.stem.replace("_", " ").title()
    documents: list[str] = []
    ids: list[str] = []
    metadatas: list[dict[str, str | int]] = []

    for index, chunk in enumerate(chunk_text(text), start=1):
        ids.append(f"upload-{path.stem}-{index}-{uuid4().hex[:8]}")
        documents.append(chunk)
        metadatas.append(
            {
                "title": "Uploaded document",
                "location": f"uploaded source chunk {index}",
                "file_name": path.name,
                "source_type": "uploaded",
                "client_id": client_id or "",
            }
        )

    if documents:
        collection.add(ids=ids, documents=documents, metadatas=metadatas)

    return len(documents)


def list_indexed_documents(client_id: str | None = None) -> list[dict[str, str | int]]:
    collection = get_collection()
    count = collection.count()
    if count == 0:
        return []

    result = collection.get(include=["metadatas"], limit=count)
    metadatas = result.get("metadatas", [])
    grouped: dict[str, dict[str, str | int]] = {}

    for metadata in metadatas:
        file_name = str(metadata.get("file_name", "unknown"))
        title = str(metadata.get("title", file_name))
        source_type = str(metadata.get("source_type", "uploaded" if file_name not in SAMPLE_FILES else "sample"))
        document_client_id = str(metadata.get("client_id", ""))
        if source_type == "uploaded" and (not client_id or document_client_id != client_id):
            continue
        current = grouped.setdefault(
            file_name,
            {
                "file_name": public_document_label(file_name, source_type),
                "title": title if source_type == "sample" else "Uploaded policy report",
                "chunks": 0,
                "source_type": source_type,
            },
        )
        current["chunks"] = int(current["chunks"]) + 1

    public_items = sorted(grouped.values(), key=lambda item: str(item["file_name"]))
    upload_index = 0
    for item in public_items:
        if item["source_type"] == "uploaded":
            upload_index += 1
            item["file_name"] = public_document_label("", "uploaded", upload_index)

    return public_items


def reset_collection() -> int:
    client = chromadb.PersistentClient(path=settings.chroma_dir)
    try:
        client.delete_collection("policy_reports")
    except Exception:
        pass
    return ingest_sample_documents()
