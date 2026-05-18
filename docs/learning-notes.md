# Learning Notes

This file explains the project step by step while we build it.

## What Are We Building?

We are building an AI research assistant for development policy documents.

The assistant should be able to:

- read policy reports,
- find relevant evidence,
- answer questions with sources,
- turn the answer into a short policy brief,
- check whether the answer is supported by retrieved evidence.

## What Is RAG?

RAG means Retrieval-Augmented Generation.

Instead of asking the AI model to answer from memory only, we first retrieve relevant text from our own documents. Then the model answers using that retrieved evidence.

Simple version:

```text
Question -> Search documents -> Find relevant chunks -> Ask model with context -> Answer with citations
```

## What Is a Vector Database?

A vector database stores chunks of text as numeric vectors. Similar text should
have similar vectors. When a user asks a question, we convert the question into a
vector and search for nearby document chunks.

In this project, ChromaDB stores the report chunks.

Current MVP:

```text
sample reports -> chunks -> local embeddings -> ChromaDB -> retrieved sources
```

Later upgrade:

```text
PDF reports -> chunks -> OpenAI embeddings -> ChromaDB -> LangGraph workflow
```

## What Is an Agentic AI Workflow?

An agentic workflow breaks a task into controlled steps.

For this project:

```text
Research -> Analyze -> Validate -> Write brief
```

Each step has a clear responsibility:

- Research: find relevant source material.
- Analyze: explain the evidence.
- Validate: check if the answer has enough support.
- Write brief: produce a structured policy note.

In the backend, this is implemented as a LangGraph workflow. LangGraph lets us
define named steps and connect them in order:

```text
research -> analysis -> validation -> brief
```

This is more portfolio-friendly than a single large prompt because the process is
visible, testable, and easy to explain.

## What Happens When A PDF Is Uploaded?

The upload flow is:

```text
PDF/TXT upload -> save file -> extract text -> chunk text -> embed chunks -> store in ChromaDB
```

After that, new questions can retrieve evidence from the uploaded document.

## Why This Fits The UNDP Internship

The internship asks for Python, prompt engineering, agentic AI systems, RAG, vector databases, API work, and analytical writing.

This project touches all of those areas in one focused portfolio piece.
