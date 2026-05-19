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

I built this project to turn the AI, API, backend, frontend, and deployment topics I have been learning into a real working product. Instead of only using AI tools from the outside, I wanted to understand how an AI-powered application is actually designed, connected, deployed, and presented as a portfolio project.

The project is also aligned with agentic AI research work in the development policy space. It gave me a practical way to apply concepts such as API integration, document upload, retrieval, vector search, prompt design, agent workflows, and policy brief generation in one end-to-end system.

In short, I built it to practice:

- using real AI APIs in an application,
- connecting a frontend to a backend,
- building a RAG pipeline over PDF/TXT documents,
- designing an agent workflow with clear steps,
- deploying a project on my own Ubuntu server,
- improving the UI/UX until it feels usable,
- documenting the work clearly on GitHub as a portfolio project.

The project demonstrates:

- Python backend development with FastAPI.
- React frontend development.
- Retrieval-Augmented Generation (RAG) concepts.
- Vector database usage with ChromaDB.
- PDF/TXT document ingestion.
- LangGraph-based agent workflow design.
- Optional Groq, Gemini, or OpenRouter LLM API support for generated answers and briefs.
- Deployment on an Ubuntu server with systemd and nginx.
- Basic public demo privacy controls, including masked uploaded document names and scoped browser sessions.

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
- Groq API optional
- Gemini API optional
- OpenRouter API optional
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
- upload size limit and sanitized uploaded file names
- browser-scoped uploaded document access for the public demo
- LangGraph workflow
- optional multi-provider LLM generation
- nginx deployment
- systemd backend service
- bilingual English/Turkish interface
- copy/download policy brief actions

Planned improvements:

- OpenAI embeddings
- evaluation metrics for citation coverage
- user authentication for private deployments
- stronger production document management with accounts and audit logs

## Optional Free LLM APIs

The app can run without any LLM API key by using template-based answer and brief
generation. If API keys are configured, the LangGraph workflow can use Groq,
Gemini, or OpenRouter for the analysis and policy brief steps.

Environment variables:

```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.1-8b-instant
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
```

The UI lets the user choose `Auto`, `Groq`, `Gemini`, or `OpenRouter`.
`Auto` tries configured providers in order and falls back to the local template
mode if no API provider is available.

## Security And Privacy Notes

This is a public portfolio demo, so it includes basic safeguards:

- real API keys are kept in server-side `.env` files and are not committed,
- uploaded document file names are masked in the UI,
- uploaded documents are scoped to a browser session with an anonymous client id,
- upload file names are sanitized before storage,
- upload size is limited,
- only PDF/TXT uploads are accepted,
- the backend sends basic security headers,
- CORS is restricted to the expected frontend origins by default.

For a production deployment, the next step would be real user authentication,
database-backed document ownership, audit logs, and stricter rate limiting.

## Learning Notes

This repository is intentionally documented as a learning project. See:

- `docs/learning-notes.md`
- `docs/project-plan.md`
- `docs/production-deploy.md`

## Portfolio Summary

Built an SDG Policy Intelligence Agent using Python, FastAPI, React, ChromaDB, and LangGraph to analyze development policy documents, retrieve evidence-backed answers, and generate structured policy briefs with citations and validation notes.
