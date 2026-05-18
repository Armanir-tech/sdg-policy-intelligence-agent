# Portfolio Notes

## Short GitHub Description

Agentic AI research assistant for SDG policy documents using FastAPI, React, ChromaDB, and LangGraph.

## CV Bullet

Built an SDG Policy Intelligence Agent using Python, FastAPI, React, ChromaDB, and LangGraph to analyze development policy documents, retrieve evidence-backed answers, and generate structured policy briefs with citations and validation notes.

## LinkedIn / Portfolio Description

I built an SDG Policy Intelligence Agent as a portfolio project focused on agentic AI for development policy research. The application allows users to upload PDF/TXT policy documents, retrieve relevant evidence from a vector database, and generate structured answers and policy briefs through a LangGraph workflow.

The project helped me practice backend development, frontend development, RAG concepts, vector databases, deployment, and agent workflow design.

## Interview Explanation

The project started as a simple FastAPI and React application. First, I built a mock research endpoint to make sure the frontend and backend could communicate. Then I added a basic retrieval layer, upgraded it to ChromaDB vector retrieval, added document upload, and finally organized the research process as a LangGraph workflow.

The workflow has four steps:

```text
research -> analysis -> validation -> brief
```

This structure makes it easier to explain what the agent is doing and where each result comes from.

## Honest Current Limitations

- The current MVP uses local deterministic embeddings instead of OpenAI embeddings.
- The policy brief generation is template-based, not fully LLM-generated yet.
- There is no authentication, so it should be treated as a demo deployment.
- Uploaded document management is basic.

These limitations are intentional for the first deployable version and can be improved in later versions.

