# Retirement CoPilot

AI-powered Retirement Planning CoPilot for HDFC Bank pension products using RAG, financial simulations, and agentic recommendation orchestration.

---

# Overview

Retirement CoPilot is a domain-specific GenAI assistant designed to help customers:
- understand retirement readiness
- estimate future retirement corpus
- simulate pension outcomes
- receive grounded pension product recommendations
- compare guaranteed vs market-linked retirement plans

The system combines:
- metadata-aware RAG
- pension knowledge retrieval
- financial projection models
- AI orchestration
- structured recommendation generation

---

# Key Features

## Metadata-Aware Pension RAG
- Pension product markdown knowledge base
- OpenAI embeddings
- ChromaDB vector retrieval
- Semantic search with metadata filtering

---

## Retirement Simulation Engine
- Future corpus projection
- SIP growth estimation
- Monthly pension estimation
- Retirement readiness classification

---

## AI Recommendation Orchestration
- Suitability-aware pension recommendations
- Guaranteed vs market-linked reasoning
- Risk-profile aligned retrieval
- Grounded financial explanation generation

---

## Structured AI Responses
- UI-ready structured outputs
- Recommendation cards support
- Future dashboard integration support
- Streamlit-ready response formatting

---

## Observability
- Structured logging
- Retrieval tracing
- Simulation execution logging

---

# Architecture

```text
User Query
    ↓
Orchestrator Agent
    ↓
Metadata-Aware Retrieval
    ↓
Simulation Agent
    ↓
Financial Projection Engine
    ↓
LLM Recommendation Synthesis
    ↓
Structured Retirement Response
```

---

# Tech Stack

## Frontend
- Streamlit (in progress)

## Core AI
- OpenAI GPT-4.1 Mini

## RAG Layer
- LangChain
- ChromaDB
- OpenAI Embeddings

## Knowledge Base
- Pension markdown documents
- Metadata-enriched retrieval

## Simulation Layer
- Python financial projection models

## Observability
- Structured logging

---

# Project Structure

```text
app/
│
├── agents/
│   ├── orchestrator.py
│   ├── simulation_agent.py
│
├── rag/
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── chunker.py
│   ├── ingestion.py
│
├── simulations/
│   ├── pension_projection.py
│
├── observability/
│   ├── traces.py
│
├── docs/
│   ├── pension_markdowns/
│
├── utils/
│   ├── config.py
│   ├── constants.py
│   ├── helpers.py
│
└── main.py (frontend integration in progress)
```

---

# Example Capabilities

## Pension Recommendation

Input:

```text
I want guaranteed retirement income at age 60.
```

Output:
- Suitable pension plans
- Risk-aligned recommendations
- Guaranteed income analysis
- Retirement gap assessment

---

## Retirement Simulation

Input:

```text
Current corpus: ₹35L
Monthly SIP: ₹35K
Retirement age: 60
```

Output:
- Projected retirement corpus
- Estimated monthly pension
- Retirement readiness classification

---

# Current Status

## Backend MVP Completed

Implemented:
- metadata-aware RAG
- semantic retrieval
- retirement simulation engine
- AI recommendation orchestration
- structured response generation

Frontend Streamlit integration is currently in progress.

---

# Setup Instructions

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create `.env`

```env
OPENAI_API_KEY=your_openai_api_key
```

---

## Run Pension Document Ingestion

```bash
python -m app.rag.ingestion
```

---

## Test Retrieval

```bash
python test_retrieval.py
```

---

## Test Orchestrator

```bash
python test_orchestrator.py
```

---

# Future Enhancements

- Streamlit dashboard
- Monte Carlo retirement simulations
- Firefly visualization integration
- LangSmith observability
- Scenario comparison engine
- Dynamic suitability scoring
- Multi-agent orchestration

---

# Disclaimer

This project is intended for educational and demonstration purposes only and should not be treated as financial advice.
