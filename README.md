# 💰 Retirement CoPilot

AI-powered Retirement Planning CoPilot for HDFC Bank pension products with:

- Retrieval-Augmented Generation (RAG)
- Retirement simulation engine
- Streaming AI responses
- Strict grounded pension-document reasoning
- Conversational memory
- Modular AI orchestration
- ChromaDB vector retrieval
- Streamlit conversational UI

---

# 🚀 Features

## ✅ Retirement Planning Assistant

Supports:

- retirement readiness analysis
- pension corpus estimation
- SIP-based retirement projections
- guaranteed vs market-linked pension comparisons
- retirement risk analysis
- grounded pension product recommendations

---

# 🎨 Adobe Firefly Enhancement Direction

This project is being designed as a foundation for future Adobe Firefly-powered retirement visualization workflows.

## Planned Visualization Enhancements

Future enhancements may include:

- retirement lifestyle visualizations
- pension growth storytelling
- retirement readiness infographics
- AI-generated financial visuals
- personalized retirement scenario imagery

These enhancements are planned on top of the current grounded RAG architecture.

---

# 🧠 AI Architecture

## Retrieval-Augmented Generation (RAG)

The system retrieves relevant pension documents from ChromaDB vector storage before generating responses.

### Grounding Rules

Responses are strictly grounded using:

1. Retrieved pension documents
2. Retirement simulation outputs
3. Conversation context

The assistant:
- does NOT invent pension product features
- does NOT hallucinate guarantees
- does NOT use unsupported financial claims
- explicitly states when information is unavailable

---

# 📡 Streaming Responses

The assistant streams responses token-by-token for:

- better UX
- lower perceived latency
- real-time AI interaction

Includes:
- thinking workflow indicators
- retrieval status
- simulation status
- live streaming output

---

# 🧵 Conversation Threads

Supports:
- multi-turn retirement conversations
- follow-up questions
- contextual memory
- thread-based chat sessions

Conversation history is used for:
- contextual understanding
- follow-up clarification
- continuity

while still grounding responses on fresh retrieval + simulation.

---

# 📈 Retirement Simulation Engine

Calculates:
- projected retirement corpus
- estimated pension income
- SIP growth projections
- retirement readiness assessment

Inputs:
- current age
- retirement age
- current corpus
- monthly SIP
- expected annual returns

---

# 🔍 Vector Retrieval

Uses:
- ChromaDB
- OpenAI embeddings
- metadata-aware filtering
- Max Marginal Relevance (MMR) retrieval

Supports:
- guaranteed pension filtering
- market-linked filtering
- contextual pension retrieval

---

# 🖥️ Streamlit Conversational UI

Features:
- conversational chat interface
- suggested retirement questions
- thread history
- source attribution
- streaming AI responses
- retirement projection cards
- footer observability metrics

---

# 📊 Observability Metrics

Tracks:
- frontend latency
- backend latency
- token usage
- estimated API cost
- retrieved sources

---

# 🏗️ Project Structure

```text
app/
│
├── agents/
│   ├── orchestrator.py
│   ├── simulation_agent.py
│
├── rag/
│   ├── retriever.py
│   ├── vector_store.py
│
├── ui/
│   ├── styles.py
│   ├── sidebar.py
│   ├── chat.py
│   ├── cards.py
│   └── metrics.py
│
├── observability/
│   └── traces.py
│
├── utils/
│   └── helpers.py
│
└── main.py
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone <your_repo_url>
cd retirement-copilot
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### macOS/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\\Scripts\\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create:

```text
.env
```

Add:

```env
OPENAI_API_KEY=your_openai_key
```

---

# ▶️ Run Application

```bash
streamlit run app/main.py
```

---

# 🧪 Example Queries

## Retirement Readiness

```text
Can I retire comfortably at 60?
```

## Pension Estimation

```text
How much SIP is needed for ₹1L monthly pension?
```

## Product Comparison

```text
Market-linked or guaranteed pension plans?
```

## Risk Analysis

```text
Why is my retirement readiness weak?
```

---

# 🧠 Current AI Capabilities

## Implemented

✅ Strict grounded RAG  
✅ Streaming AI responses  
✅ Threaded conversations  
✅ Source attribution  
✅ Retirement simulation engine  
✅ Pension retrieval filters  
✅ Conversational memory  
✅ Observability metrics  
✅ Modular architecture  

---

# 🚧 Planned Enterprise Enhancements

## Next Phase

- Guardrails
- Hallucination detection
- Evaluation framework
- Intent routing
- Hybrid retrieval
- Retrieval confidence scoring
- Groundedness metrics
- BM25 + vector search
- Agentic orchestration
- Adobe Firefly visualization integration

---

# 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | OpenAI GPT-4.1-mini |
| Vector DB | ChromaDB |
| Embeddings | OpenAI Embeddings |
| UI | Streamlit |
| Retrieval | LangChain |
| Observability | Custom Metrics |
| Language | Python |

---

# 🎯 Design Goals

This project focuses on:

- grounded enterprise AI
- retirement advisory workflows
- production-style RAG architecture
- conversational financial copilots
- observable AI systems
- modular AI infrastructure

---

# 📌 Notes

This project is intended for:
- AI engineering demonstrations
- RAG architecture exploration
- retirement advisory copilots
- enterprise GenAI experimentation

It is NOT intended as licensed financial advice.

---

# 👨‍💻 Author

Built as a production-style AI Retirement Planning CoPilot using:
- RAG
- streaming orchestration
- grounded AI reasoning
- simulation-driven retirement analysis