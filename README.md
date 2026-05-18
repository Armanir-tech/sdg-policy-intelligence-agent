# SDG Policy Intelligence Agent

An agentic AI research assistant for development policy documents.

The project retrieves evidence from policy reports, validates source coverage, and drafts short policy briefs through an explicit agent workflow. It was built as a portfolio project for roles involving LLMs, RAG, agentic AI systems, and development policy research.

## Live Demo

Demo URL:

```text
http://213.142.148.196
```

The demo runs on a small Ubuntu server with a FastAPI backend and a React frontend served by nginx.

## What It Does

- Upload PDF or TXT policy documents.
- Extract and chunk document text.
- Store chunks in ChromaDB.
- Retrieve relevant evidence for a policy question.
- Run a LangGraph workflow:

```text
research -> analysis -> validation -> brief
```

- Show:
  - evidence-backed answer,
  - policy brief,
  - source passages,
  - validation notes,
  - workflow status.

## Why I Built It

The goal was to build a practical project aligned with agentic AI research work in the development policy space.

The project demonstrates:

- Python backend development with FastAPI.
- React frontend development.
- Retrieval-Augmented Generation (RAG) concepts.
- Vector database usage with ChromaDB.
- PDF/TXT document ingestion.
- LangGraph-based agent workflow design.
- Deployment on an Ubuntu server with systemd and nginx.

## Architecture

```text
Browser
  -> React frontend
  -> FastAPI backend
  -> LangGraph workflow
  -> ChromaDB vector store
  -> retrieved policy evidence
  -> answer + policy brief + validation notes
```

## Tech Stack

Backend:

- Python
- FastAPI
- ChromaDB
- pypdf
- LangGraph
- systemd

Frontend:

- React
- TypeScript
- Vite
- custom CSS
- lucide-react

Deployment:

- Ubuntu 22.04
- nginx
- systemd

## Repository Structure

```text
sdg-policy-intelligence-agent/
  backend/
    app/
      agents/
      api/
      core/
      rag/
      schemas/
    data/
      sample_reports/
    requirements.txt
  frontend/
    src/
      styles/
    package.json
  docs/
    learning-notes.md
    project-plan.md
    production-deploy.md
```

## Main API Endpoints

Health check:

```http
GET /health
```

Upload document:

```http
POST /documents/upload
```

Run research:

```http
POST /research
```

Reset and re-ingest sample documents:

```http
POST /ingest/reset
```

## Example Question

```text
How can private sector finance support SDG implementation?
```

Example workflow result:

- retrieves relevant SDG financing passages,
- identifies supporting evidence,
- writes a concise answer,
- drafts a policy brief,
- returns validation notes.

## Current Status

Implemented:

- FastAPI backend
- React/Vite frontend
- ChromaDB vector retrieval
- PDF/TXT upload
- LangGraph workflow
- nginx deployment
- systemd backend service

Planned improvements:

- OpenAI embeddings
- stronger policy brief generation
- evaluation metrics for citation coverage
- better document management
- user authentication for private deployments

## Learning Notes

This repository is intentionally documented as a learning project. See:

- `docs/learning-notes.md`
- `docs/project-plan.md`
- `docs/production-deploy.md`

## Portfolio Summary

Built an SDG Policy Intelligence Agent using Python, FastAPI, React, ChromaDB, and LangGraph to analyze development policy documents, retrieve evidence-backed answers, and generate structured policy briefs with citations and validation notes.

