# 💰 Retirement CoPilot

Enterprise-grade AI-powered Retirement Planning Assistant built using Streamlit, FastAPI, Retrieval-Augmented Generation (RAG), ChromaDB, and OpenAI LLMs.

Retirement CoPilot enables users to simulate retirement outcomes, analyze retirement readiness, retrieve pension intelligence through semantic search, and generate grounded AI-driven retirement insights via an interactive analytics dashboard and modular backend architecture.

---

# 🚀 Live Demo

```text
hhttps://retirement-copilot.streamlit.app
```

---

# 📸 Screenshots

## Dashboard Overview

![alt text](screenshots/ui-dashboard.png)

---

## AI Retirement Insights & Summary

![alt text](screenshots/insights.png)

---

## Grounded Sources

![alt text](screenshots/sources.png)

---

# ✨ Features

## AI Retirement Analytics

- AI-generated retirement readiness analysis
- Grounded pension recommendations
- Retirement risk assessment
- Actionable retirement planning insights

## Retirement Simulation Engine

- SIP-based retirement corpus projections
- Risk-adjusted growth simulations
- Monthly retirement income estimation
- Retirement readiness scoring

## RAG-Powered Pension Intelligence

- Retrieval-Augmented Generation (RAG)
- Pension document semantic search
- Context-grounded AI responses
- Hallucination reduction guardrails

## FastAPI Backend Services

- Modular REST API architecture
- Decoupled orchestration layer
- Simulation service endpoints
- AI analysis service integration
- Enterprise-ready backend separation

## Interactive Dashboard

- Modern enterprise-style Streamlit UI
- Corpus growth visualization
- Retirement analytics cards
- Chat-based retirement assistant

## AI Guardrails

- Intent classification
- Retrieval validation
- Grounded response generation
- Context-aware recommendation filtering

---

# 🏗️ Architecture

## High-Level Architecture

```text
┌──────────────────────────┐
│      Streamlit UI        │
│ Dashboard + Chat Layer   │
└────────────┬─────────────┘
             │ REST API
             ▼
┌──────────────────────────┐
│      FastAPI Backend     │
│ API Gateway + Routing    │
└────────────┬─────────────┘
             │
     ┌───────┴────────┐
     ▼                ▼
┌──────────────┐ ┌────────────────┐
│ Simulation   │ │ RAG Retrieval  │
│ Service      │ │ Service        │
└──────────────┘ └────────────────┘
                         │
                         ▼
                ┌────────────────┐
                │ Chroma Vector  │
                │ Database       │
                └────────────────┘
                         │
                         ▼
                ┌────────────────┐
                │ Pension Docs   │
                │ Embeddings DB  │
                └────────────────┘
                         │
                         ▼
                ┌────────────────────┐
                │ LLM Inference Layer│
                │   OpenAI GPT-4.1   │
                └────────────────────┘
```

---

# 🧠 Tech Stack

## Frontend
- Streamlit
- Plotly

## AI / LLM
- OpenAI GPT-4.1 Mini
- LangChain

## Vector Database
- ChromaDB

## Embeddings
- OpenAI Embeddings

## Backend Logic
- Python 3.11

---

# 📂 Project Structure

```text
retirement-copilot/
│
├── app/
│   ├── agents/
│   ├── api/
│   ├── rag/
│   ├── docs/
│   ├── backend/
│   ├── ui/
│   ├── simulations/
│   ├── guardrails/
│   ├── utils/
│   └── main.py
│
├── chroma_db/
├── requirements.txt
└── README.md
```

---

# 🔍 Core Components

## Simulation Engine
Projects retirement corpus growth using:
- current age
- retirement age
- SIP contribution
- risk profile
- annualized returns

## RAG Retrieval System
Uses:
- OpenAI embeddings
- Chroma vector database
- semantic pension search
- grounded retrieval pipeline

## AI Orchestrator
Handles:
- prompt engineering
- context injection
- conversation continuity
- grounded response generation

## Guardrails
Implements:
- query intent validation
- retrieval quality checks
- hallucination prevention
- grounded recommendation enforcement

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/your-username/retirement-copilot.git

cd retirement-copilot
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### macOS/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create `.env`

```env
OPENAI_API_KEY=your_openai_api_key
```

---

# 🧱 Build Vector Database

```bash
python -m app.rag.ingestion
```

This generates:

```text
chroma_db/
```

---

# ▶️ Run Application

```bash
streamlit run app/main.py
```

---

# 📊 Example Capabilities

- “Am I on track for retirement?”
- “Which pension plans provide guaranteed income?”
- “What retirement corpus will I need?”
- “Compare guaranteed vs market-linked pension products.”
- “What happens if I stop SIP contributions?”

---

# 🔒 AI Safety & Grounding

Retirement CoPilot enforces:
- retrieval-grounded responses
- pension-context-only recommendations
- hallucination reduction
- controlled retirement guidance generation

The assistant does NOT:
- invent pension features
- generate unsupported guarantees
- fabricate returns or tax benefits
- use external financial assumptions

---

# 🚀 Deployment

## Streamlit Cloud

1. Push repository to GitHub
2. Create Streamlit Cloud app
3. Select deployment branch
4. Configure secrets:

```toml
OPENAI_API_KEY="your_key"
```

5. Deploy

---

# 🛣️ Future Enhancements

- Multi-user authentication
- Persistent chat memory
- Financial goal optimization
- Advanced Monte Carlo simulations
- Portfolio allocation engine
- SaaS multi-tenant architecture
- Broker/API integrations

---

# 📌 Notes

This project is designed as:
- an AI financial assistant demo
- enterprise AI architecture showcase
- RAG + LLM integration reference
- retirement analytics prototype

---

# 👨‍💻 Author

Febin Wilson

GitHub:
https://github.com/wilsonfebin

LinkedIn:
https://www.linkedin.com/in/febinwilson

---

# 📄 License

MIT License