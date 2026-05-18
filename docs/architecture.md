# Architecture

## High-Level Flow

```text
User
  -> asks a policy question in the web UI
  -> React sends request to FastAPI
  -> LangGraph starts the workflow
  -> research node retrieves source chunks from ChromaDB
  -> analysis node drafts an evidence-backed answer
  -> validation node checks source coverage
  -> brief node writes a short policy brief
  -> API returns answer, brief, sources, and validation notes
```

## Components

### Frontend

The frontend is a React/Vite app. It provides:

- research question input,
- PDF/TXT upload,
- workflow status,
- answer tab,
- policy brief tab,
- sources tab,
- validation tab.

### Backend

The backend is a FastAPI app. It provides:

- document upload,
- document ingestion,
- vector retrieval,
- LangGraph workflow execution,
- structured API responses.

### RAG Layer

The RAG layer:

1. reads policy documents,
2. chunks text,
3. embeds chunks,
4. stores chunks in ChromaDB,
5. retrieves relevant chunks for a question.

The current MVP uses local deterministic embeddings to keep the app lightweight on a small server. This can be replaced by OpenAI embeddings later.

### Agent Workflow

The workflow is implemented with LangGraph:

```text
research -> analysis -> validation -> brief
```

This makes the system easier to explain than a single hidden prompt.

