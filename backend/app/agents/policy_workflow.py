from __future__ import annotations

from typing import TypedDict

import httpx
from langgraph.graph import END, StateGraph

from app.agents.llm_client import LLMUnavailable, generate_with_groq, has_llm
from app.rag.vector_retriever import RetrievedChunk, retrieve_from_vector_store
from app.schemas.research import ResearchResponse, Source


class PolicyState(TypedDict, total=False):
    question: str
    chunks: list[RetrievedChunk]
    answer: str
    policy_brief: str
    validation_notes: list[str]


def research_node(state: PolicyState) -> PolicyState:
    return {"chunks": retrieve_from_vector_store(state["question"])}


def analysis_node(state: PolicyState) -> PolicyState:
    chunks = state.get("chunks", [])
    if not chunks:
        return {
            "answer": (
                "I could not find strong supporting evidence in the current document "
                "collection. Add more reports or ask a question closer to the indexed "
                "policy material."
            )
        }

    evidence = "\n\n".join(
        f"Source: {chunk.title} ({chunk.location})\n{chunk.text}" for chunk in chunks[:3]
    )

    if has_llm():
        try:
            answer = generate_with_groq(
                system_prompt=(
                    "You are a development policy research assistant. Answer only "
                    "from the provided evidence. Be concise, analytical, and avoid "
                    "unsupported claims."
                ),
                user_prompt=(
                    f"Question:\n{state['question']}\n\n"
                    f"Evidence:\n{evidence}\n\n"
                    "Write an evidence-backed answer in 1-2 paragraphs."
                ),
                max_tokens=420,
            )
            return {"answer": answer}
        except (LLMUnavailable, httpx.HTTPError, KeyError):
            pass

    joined_evidence = " ".join(chunk.text for chunk in chunks[:2])
    return {
        "answer": (
            "Based on the retrieved policy evidence, development impact depends on "
            "aligning interventions with measurable public outcomes, safeguards, and "
            "monitoring. "
            + joined_evidence[:520]
        )
    }


def validation_node(state: PolicyState) -> PolicyState:
    chunks = state.get("chunks", [])
    if not chunks:
        return {
            "validation_notes": [
                "No supporting sources found.",
                "The answer should not be treated as evidence-backed yet.",
            ]
        }

    return {
        "validation_notes": [
            f"{len(chunks)} supporting source sections found.",
            "ChromaDB vector retrieval is active.",
            "LangGraph workflow executed: research -> analysis -> validation -> brief.",
        ]
    }


def brief_node(state: PolicyState) -> PolicyState:
    chunks = state.get("chunks", [])
    if not chunks:
        return {
            "policy_brief": (
                "Problem: The current document collection does not contain enough "
                "evidence for this question.\n\n"
                "Evidence: No relevant chunks were retrieved.\n\n"
                "Recommendation: Ingest additional policy reports before generating "
                "a final brief."
            )
        }

    strongest = chunks[0]

    evidence = "\n\n".join(
        f"Source: {chunk.title} ({chunk.location})\n{chunk.text}" for chunk in chunks[:3]
    )

    if has_llm():
        try:
            policy_brief = generate_with_groq(
                system_prompt=(
                    "You write short policy briefs for development policy audiences. "
                    "Use only the supplied evidence and keep the structure clear."
                ),
                user_prompt=(
                    f"Question:\n{state['question']}\n\n"
                    f"Evidence:\n{evidence}\n\n"
                    "Draft a brief with exactly these sections: Problem, Evidence, "
                    "Recommendation. Keep it under 180 words."
                ),
                max_tokens=360,
            )
            return {"policy_brief": policy_brief}
        except (LLMUnavailable, httpx.HTTPError, KeyError):
            pass

    return {
        "policy_brief": (
            "Problem: Development policy goals often require financing, institutional "
            "capacity, and inclusion safeguards.\n\n"
            f"Evidence: The workflow retrieved {len(chunks)} source sections. The "
            f"strongest match is from \"{strongest.title}\" ({strongest.location}).\n\n"
            "Recommendation: Use private sector participation or AI-enabled services "
            "only when measurable impact indicators, transparency, and public-interest "
            "safeguards are defined before implementation."
        )
    }


def build_policy_graph():
    graph = StateGraph(PolicyState)
    graph.add_node("research", research_node)
    graph.add_node("analysis", analysis_node)
    graph.add_node("validation", validation_node)
    graph.add_node("brief", brief_node)
    graph.set_entry_point("research")
    graph.add_edge("research", "analysis")
    graph.add_edge("analysis", "validation")
    graph.add_edge("validation", "brief")
    graph.add_edge("brief", END)
    return graph.compile()


policy_graph = build_policy_graph()


def run_policy_workflow(question: str) -> ResearchResponse:
    state = policy_graph.invoke({"question": question})
    chunks = state.get("chunks", [])

    return ResearchResponse(
        question=question,
        answer=state.get("answer", ""),
        policy_brief=state.get("policy_brief", ""),
        sources=[
            Source(title=chunk.title, location=chunk.location, excerpt=chunk.text)
            for chunk in chunks
        ],
        validation_notes=state.get("validation_notes", []),
        workflow_steps=["research", "analysis", "validation", "brief"],
    )
