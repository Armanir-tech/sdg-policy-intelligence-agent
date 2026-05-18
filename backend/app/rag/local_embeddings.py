from __future__ import annotations

import hashlib
import math
import re


WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z\-]{2,}")


class LocalHashEmbedding:
    """Small deterministic embedding function for the MVP.

    It is intentionally dependency-light so the project runs on a small server.
    Later we can replace this with OpenAI embeddings without changing the API
    shape of the retriever.
    """

    def __init__(self, dimensions: int = 384):
        self.dimensions = dimensions

    def __call__(self, input: list[str]) -> list[list[float]]:
        return [self.embed(text) for text in input]

    def name(self) -> str:
        return "local-hash-embedding"

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions

        for word in WORD_RE.findall(text.lower()):
            digest = hashlib.sha256(word.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign

        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector

        return [value / norm for value in vector]

