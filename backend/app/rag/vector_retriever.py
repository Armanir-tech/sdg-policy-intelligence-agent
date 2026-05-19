from __future__ import annotations

from dataclasses import dataclass

from app.rag.ingest import SAMPLE_FILES, get_collection, ingest_sample_documents


@dataclass
class RetrievedChunk:
    title: str
    location: str
    text: str
    distance: float
    source_type: str


def retrieve_from_vector_store(question: str, limit: int = 4, client_id: str | None = None) -> list[RetrievedChunk]:
    ingest_sample_documents()
    collection = get_collection()
    result = collection.query(query_texts=[question], n_results=limit * 6)

    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    chunks: list[RetrievedChunk] = []
    for document, metadata, distance in zip(documents, metadatas, distances):
        file_name = str(metadata.get("file_name", ""))
        source_type = str(metadata.get("source_type", "sample" if file_name in SAMPLE_FILES else "uploaded"))
        document_client_id = str(metadata.get("client_id", ""))
        if source_type == "uploaded" and (not client_id or document_client_id != client_id):
            continue
        chunks.append(
            RetrievedChunk(
                title=str(metadata.get("title", "Unknown source")),
                location=str(metadata.get("location", "Unknown location")),
                text=document,
                distance=float(distance),
                source_type=source_type,
            )
        )
        if len(chunks) >= limit:
            break

    return chunks
