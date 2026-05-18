from dataclasses import dataclass
from pathlib import Path
import re


WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z\-]{2,}")


@dataclass
class Chunk:
    title: str
    location: str
    text: str
    score: int = 0


def tokenize(text: str) -> set[str]:
    return {word.lower() for word in WORD_RE.findall(text)}


def load_text_documents(data_dir: Path) -> list[tuple[str, str]]:
    documents: list[tuple[str, str]] = []
    for path in sorted(data_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        title = path.stem.replace("_", " ").title()
        for line in text.splitlines():
            if line.startswith("Title:"):
                title = line.replace("Title:", "", 1).strip()
                break
        documents.append((title, text))
    return documents


def chunk_document(title: str, text: str, chunk_size: int = 520) -> list[Chunk]:
    paragraphs = [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]
    chunks: list[Chunk] = []

    for index, paragraph in enumerate(paragraphs, start=1):
        if len(paragraph) <= chunk_size:
            chunk_text = paragraph
        else:
            chunk_text = paragraph[:chunk_size].rsplit(" ", 1)[0]

        chunks.append(Chunk(title=title, location=f"section {index}", text=chunk_text))

    return chunks


def retrieve(question: str, data_dir: Path, limit: int = 3) -> list[Chunk]:
    question_terms = tokenize(question)
    all_chunks: list[Chunk] = []

    for title, text in load_text_documents(data_dir):
        all_chunks.extend(chunk_document(title, text))

    scored_chunks: list[Chunk] = []
    for chunk in all_chunks:
        chunk_terms = tokenize(chunk.text)
        score = len(question_terms.intersection(chunk_terms))
        if score > 0:
            scored_chunks.append(Chunk(chunk.title, chunk.location, chunk.text, score))

    return sorted(scored_chunks, key=lambda chunk: chunk.score, reverse=True)[:limit]

