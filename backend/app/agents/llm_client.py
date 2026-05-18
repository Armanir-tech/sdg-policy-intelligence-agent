from __future__ import annotations

import httpx

from app.core.config import settings


class LLMUnavailable(Exception):
    pass


def has_llm() -> bool:
    return bool(settings.groq_api_key.strip())


def generate_with_groq(system_prompt: str, user_prompt: str, max_tokens: int = 520) -> str:
    api_key = settings.groq_api_key.strip()
    if not api_key:
        raise LLMUnavailable("GROQ_API_KEY is not configured.")

    payload = {
        "model": settings.groq_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.25,
        "max_tokens": max_tokens,
    }

    with httpx.Client(timeout=35) as client:
        response = client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    return data["choices"][0]["message"]["content"].strip()
