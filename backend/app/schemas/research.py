from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    question: str = Field(..., min_length=5)


class Source(BaseModel):
    title: str
    location: str
    excerpt: str


class ResearchResponse(BaseModel):
    question: str
    answer: str
    policy_brief: str
    sources: list[Source]
    validation_notes: list[str]
    workflow_steps: list[str] = []
