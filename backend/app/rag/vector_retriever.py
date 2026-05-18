from __future__ import annotations

from dataclasses import dataclass

from app.rag.ingest import get_collection, ingest_sample_documents


@dataclass
class RetrievedChunk:
    title: str
    location: str
    text: str
    distance: float


def retrieve_from_vector_store(question: str, limit: int = 4) -> list[RetrievedChunk]:
    ingest_sample_documents()
    collection = get_collection()
    result = collection.query(query_texts=[question], n_results=limit)

    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    chunks: list[RetrievedChunk] = []
    for document, metadata, distance in zip(documents, metadatas, distances):
        chunks.append(
            RetrievedChunk(
                title=str(metadata.get("title", "Unknown source")),
                location=str(metadata.get("location", "Unknown location")),
                text=document,
                distance=float(distance),
            )
        )

    return chunks

