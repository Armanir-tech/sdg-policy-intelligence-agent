from __future__ import annotations

import httpx

from app.core.config import settings


class LLMUnavailable(Exception):
    pass


class LLMResponse(dict):
    text: str
    provider: str


def available_providers() -> list[str]:
    providers: list[str] = []
    if settings.groq_api_key.strip():
        providers.append("groq")
    if settings.gemini_api_key.strip():
        providers.append("gemini")
    if settings.openrouter_api_key.strip():
        providers.append("openrouter")
    return providers


def choose_providers(requested_provider: str) -> list[str]:
    requested = requested_provider.lower().strip()
    configured = available_providers()

    if requested in {"groq", "gemini", "openrouter"}:
        return [requested] if requested in configured else []

    preferred_order = ["groq", "gemini", "openrouter"]
    return [provider for provider in preferred_order if provider in configured]


def generate_text(
    system_prompt: str,
    user_prompt: str,
    requested_provider: str = "auto",
    max_tokens: int = 520,
) -> tuple[str, str]:
    errors: list[str] = []
    for provider in choose_providers(requested_provider):
        try:
            if provider == "groq":
                return generate_with_groq(system_prompt, user_prompt, max_tokens), "groq"
            if provider == "gemini":
                return generate_with_gemini(system_prompt, user_prompt, max_tokens), "gemini"
            if provider == "openrouter":
                return generate_with_openrouter(system_prompt, user_prompt, max_tokens), "openrouter"
        except (httpx.HTTPError, KeyError, IndexError, TypeError, LLMUnavailable) as error:
            errors.append(f"{provider}: {error}")

    raise LLMUnavailable("; ".join(errors) or "No configured provider is available.")


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


def generate_with_openrouter(system_prompt: str, user_prompt: str, max_tokens: int = 520) -> str:
    api_key = settings.openrouter_api_key.strip()
    if not api_key:
        raise LLMUnavailable("OPENROUTER_API_KEY is not configured.")

    payload = {
        "model": settings.openrouter_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.25,
        "max_tokens": max_tokens,
    }

    with httpx.Client(timeout=45) as client:
        response = client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://213.142.148.196",
                "X-Title": "SDG Policy Intelligence Agent",
            },
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    return data["choices"][0]["message"]["content"].strip()


def generate_with_gemini(system_prompt: str, user_prompt: str, max_tokens: int = 520) -> str:
    api_key = settings.gemini_api_key.strip()
    if not api_key:
        raise LLMUnavailable("GEMINI_API_KEY is not configured.")

    prompt = f"{system_prompt}\n\n{user_prompt}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.25,
            "maxOutputTokens": max_tokens,
        },
    }

    with httpx.Client(timeout=45) as client:
        response = client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_model}:generateContent",
            headers={
                "x-goog-api-key": api_key,
                "Content-Type": "application/json",
            },
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    return data["candidates"][0]["content"]["parts"][0]["text"].strip()
