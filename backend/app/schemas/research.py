from pydantic import BaseModel, Field, field_validator


class ResearchRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=1200)
    language: str = "en"
    provider: str = "auto"
    client_id: str | None = None

    @field_validator("client_id")
    @classmethod
    def validate_client_id(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        if not stripped or len(stripped) > 120:
            return None
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._:-")
        if any(character not in allowed for character in stripped):
            return None
        return stripped


class Source(BaseModel):
    title: str
    location: str
    excerpt: str
    source_type: str = "sample"
    page_number: int | None = None
    confidence: str = "retrieved"


class ResearchResponse(BaseModel):
    question: str
    answer: str
    policy_brief: str
    sources: list[Source]
    validation_notes: list[str]
    workflow_steps: list[str] = []
    provider_used: str = "local"
