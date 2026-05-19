from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    question: str = Field(..., min_length=5)
    language: str = "en"
    provider: str = "auto"
    client_id: str | None = None


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
