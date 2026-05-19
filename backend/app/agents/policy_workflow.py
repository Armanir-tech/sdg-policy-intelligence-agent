from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.agents.llm_client import LLMUnavailable, generate_text
from app.rag.vector_retriever import RetrievedChunk, retrieve_from_vector_store
from app.schemas.research import ResearchResponse, Source


class PolicyState(TypedDict, total=False):
    question: str
    language: str
    provider: str
    client_id: str | None
    provider_used: str
    chunks: list[RetrievedChunk]
    answer: str
    policy_brief: str
    validation_notes: list[str]


def research_node(state: PolicyState) -> PolicyState:
    return {"chunks": retrieve_from_vector_store(state["question"], client_id=state.get("client_id"))}


def analysis_node(state: PolicyState) -> PolicyState:
    chunks = state.get("chunks", [])
    language = state.get("language", "en")
    if not chunks:
        if language == "tr":
            return {
                "answer": (
                    "Mevcut belge koleksiyonunda bu soru için güçlü destekleyici kanıt "
                    "bulamadım. Daha fazla rapor yükleyebilir veya indekslenmiş politika "
                    "materyaline daha yakın bir soru sorabilirsin."
                )
            }
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

    try:
        answer, provider_used = generate_text(
                system_prompt=(
                    "You are a development policy research assistant. Answer only "
                    "from the provided evidence. Be concise, analytical, and avoid "
                    "unsupported claims. Write in Turkish if the requested language is Turkish."
                ),
                user_prompt=(
                    f"Requested language: {'Turkish' if language == 'tr' else 'English'}\n\n"
                    f"Question:\n{state['question']}\n\n"
                    f"Evidence:\n{evidence}\n\n"
                    "Write an evidence-backed answer in 1-2 paragraphs."
                ),
                requested_provider=state.get("provider", "auto"),
                max_tokens=420,
            )
        return {"answer": answer, "provider_used": provider_used}
    except LLMUnavailable:
        pass

    joined_evidence = " ".join(chunk.text for chunk in chunks[:2])
    if language == "tr":
        return {
            "answer": (
                "Bulunan politika kanıtlarına göre etki yaratmak için finansman ve teknoloji "
                "müdahalelerinin ölçülebilir kamu yararı hedefleri, güvence mekanizmaları ve "
                "izleme süreçleriyle uyumlu olması gerekir. "
                + joined_evidence[:520]
            )
        }

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
    language = state.get("language", "en")
    if not chunks:
        if language == "tr":
            return {
                "validation_notes": [
                    "Destekleyici kaynak bulunamadı.",
                    "Bu cevap henüz kanıta dayalı kabul edilmemeli.",
                ]
            }
        return {
            "validation_notes": [
                "No supporting sources found.",
                "The answer should not be treated as evidence-backed yet.",
            ]
        }

    if language == "tr":
        return {
            "validation_notes": [
                f"{len(chunks)} destekleyici kaynak bölümü bulundu.",
                "ChromaDB vektör araması aktif.",
                "LangGraph akışı çalıştı: araştırma -> analiz -> doğrulama -> brief.",
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
    language = state.get("language", "en")
    if not chunks:
        if language == "tr":
            return {
                "policy_brief": (
                    "Problem: Mevcut belge koleksiyonu bu soru için yeterli kanıt içermiyor.\n\n"
                    "Kanıt: İlgili belge parçası bulunamadı.\n\n"
                    "Öneri: Nihai brief üretmeden önce ek politika raporları yüklenmeli."
                )
            }
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

    try:
        policy_brief, provider_used = generate_text(
                system_prompt=(
                    "You write short policy briefs for development policy audiences. "
                    "Use only the supplied evidence and keep the structure clear."
                ),
                user_prompt=(
                    f"Requested language: {'Turkish' if language == 'tr' else 'English'}\n\n"
                    f"Question:\n{state['question']}\n\n"
                    f"Evidence:\n{evidence}\n\n"
                    "Draft a brief with exactly these sections in the requested language: "
                    "Problem/Problem, Evidence/Kanıt, Recommendation/Öneri. Keep it under 180 words."
                ),
                requested_provider=state.get("provider", "auto"),
                max_tokens=360,
            )
        return {"policy_brief": policy_brief, "provider_used": provider_used}
    except LLMUnavailable:
        pass

    if language == "tr":
        return {
            "policy_brief": (
                "Problem: Kalkınma politikası hedefleri çoğu zaman finansman, kurumsal "
                "kapasite ve kapsayıcılık güvenceleri gerektirir.\n\n"
                f"Kanıt: İş akışı {len(chunks)} kaynak bölümü buldu. En güçlü eşleşme "
                f"\"{strongest.title}\" ({strongest.location}) kaynağından geldi.\n\n"
                "Öneri: Özel sektör katılımı veya yapay zeka destekli kamu hizmetleri "
                "ancak ölçülebilir etki göstergeleri, şeffaflık ve kamu yararı güvenceleri "
                "uygulama öncesinde tanımlandığında kullanılmalıdır."
            )
        }

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


def run_policy_workflow(
    question: str,
    language: str = "en",
    provider: str = "auto",
    client_id: str | None = None,
) -> ResearchResponse:
    normalized_language = "tr" if language == "tr" else "en"
    normalized_provider = provider if provider in {"auto", "groq", "gemini", "openrouter"} else "auto"
    state = policy_graph.invoke(
        {
            "question": question,
            "language": normalized_language,
            "provider": normalized_provider,
            "client_id": client_id,
        }
    )
    chunks = state.get("chunks", [])

    return ResearchResponse(
        question=question,
        answer=state.get("answer", ""),
        policy_brief=state.get("policy_brief", ""),
        sources=[
            Source(
                title=chunk.title if chunk.source_type == "sample" else "Uploaded policy report",
                location=chunk.location if chunk.source_type == "sample" else "private uploaded source",
                excerpt=(
                    chunk.text
                    if chunk.source_type == "sample"
                    else "A matching passage was found in an uploaded document. The full excerpt is hidden in the public demo."
                ),
                source_type=chunk.source_type,
                page_number=chunk.page_number,
                confidence="high" if chunk.distance < 0.85 else "medium",
            )
            for chunk in chunks
        ],
        validation_notes=state.get("validation_notes", []),
        workflow_steps=["research", "analysis", "validation", "brief"],
        provider_used=state.get("provider_used", "local"),
    )
