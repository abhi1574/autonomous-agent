```markdown
<div align="center">

# 🤖 Autonomous Agent System

### Give it a task. Multiple AI agents collaborate in real-time to deliver a detailed, structured result.

![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React_18-61DAFB?style=flat&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-FF4081?style=flat)
[![Tests](https://img.shields.io/badge/Tests-69_passing-22C55E?style=flat)]()
[![Coverage](https://img.shields.io/badge/Coverage-85%25-22C55E?style=flat)]()

</div>

---

## 🎯 What is this?

A **production-grade multi-agent AI system** built from scratch.

Type any task → an LLM planner decomposes it → specialist agents execute in parallel → results stored in vector memory → critic synthesises everything into a clean structured report.

**No LangChain. No AutoGen. No frameworks. Built from first principles.**

---

## ⚡ How it works

```
User submits task
       │
       ▼
  Groq LLaMA 3.3 70B
  breaks it into subtasks
       │
  ┌────┴──────────────┐
  ▼                   ▼
Research Agent      RAG Agent
(Tavily web search) (Qdrant vector search)
  │                   │
  └────────┬──────────┘
           ▼
      Critic Agent
  (reviews + scores + writes report)
           │
           ▼
   Result delivered via WebSocket
```

---

## 🤖 The 5 Agents

| Agent | Responsibility | Tool |
|---|---|---|
| 🔍 **Research** | Live web search | Tavily API |
| 🧠 **RAG** | Semantic memory retrieval | Qdrant vector DB |
| ⭐ **Critic** | Reviews all outputs · writes final report | Groq LLaMA 3.3 |
| 💻 **Coding** | Code generation + sandboxed execution | Python subprocess |
| 🌐 **Browser** | Scrapes any URL | Playwright Chromium |

---

## 🛠️ Tech Stack

```
Backend        FastAPI · Python 3.11 · SQLAlchemy · JWT · SlowAPI
AI             Groq LLaMA 3.3 70B · Tavily Search · Sentence Transformers
Databases      PostgreSQL · Redis (task queue) · Qdrant (vector memory)
Agents         5 specialist agents · dependency resolution · retry logic
Frontend       React 18 · TypeScript · Vite · Tailwind CSS · Zustand
Real-time      WebSocket live feed · polling · animated pipeline
Testing        69 tests · 85% coverage · pytest · unit + integration + API
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│         React + TypeScript          │
│  Dashboard · Tasks · Agents · Logs  │
└──────────────┬──────────────────────┘
               │ REST + WebSocket
┌──────────────▼──────────────────────┐
│           FastAPI Gateway            │
│  JWT · Rate limiting · Logging       │
└───┬──────────┬───────────┬──────────┘
    │          │           │
┌───▼──┐  ┌───▼───┐  ┌────▼──────────────────┐
│  PG  │  │ Redis │  │   Agent Threads        │
│Tasks │  │Queue  │  │ Research·RAG·Critic    │
│Users │  │       │  │ Coding·Browser         │
│Logs  │  │       │  └──────────┬─────────────┘
└──────┘  └───────┘             │
                        ┌───────▼──────┐
                        │    Qdrant    │
                        │Vector Memory │
                        └──────────────┘
```

---

## ✨ Key Engineering Highlights

- **Zero framework dependency** — agents, orchestration, memory built from scratch
- **Redis task queue** with dependency resolution — agents wait for upstream results
- **Vector memory** — every result embedded (384-dim) and stored for semantic retrieval
- **Singleton tool router** — all agents share one model instance, saving ~270MB RAM
- **Background threads** — all 5 agents run concurrently inside FastAPI lifespan
- **Structured logging** — every request, tool call and agent action logged with duration
- **Rate limiting** — SlowAPI protects all endpoints
- **69 automated tests** — unit, integration and API layers with 85% coverage

---

## 📁 Structure

```
autonomous-agent/
├── agents/
│   ├── orchestrator/        # planner · dispatcher · task queue
│   ├── base_agent.py        # abstract lifecycle with retry logic
│   ├── research_agent.py
│   ├── rag_agent.py
│   ├── critic_agent.py
│   ├── coding_agent.py
│   └── browser_agent.py
├── backend/
│   ├── main.py              # FastAPI app + agent thread launcher
│   ├── config.py            # env validation
│   ├── logger.py            # structured logging
│   ├── middleware/          # JWT auth
│   ├── models/              # SQLAlchemy ORM
│   ├── routers/             # REST endpoints
│   └── websocket/           # connection manager
├── memory/
│   ├── vector_store.py      # Qdrant wrapper
│   └── task_memory.py       # PostgreSQL task state
├── tools/
│   ├── router.py            # central registry + tool logging
│   ├── llm.py
│   ├── web_search.py
│   ├── embeddings.py
│   ├── vector_search.py
│   ├── code_executor.py
│   └── browser.py
├── frontend/src/
│   ├── pages/               # Login · Register · Dashboard
│   ├── components/          # Topbar · Sidebar · Pipeline · Feed
│   ├── hooks/               # useAuth · useTasks · useWebSocket
│   └── store/               # Zustand auth store
└── tests/                   # 69 tests · 85% coverage
```

---

## 🚀 Run locally

### Prerequisites
```
Python 3.11+   Node.js 18+   PostgreSQL   Redis   Qdrant
```

### Setup
```bash
# Clone
git clone https://github.com/abhi1574/autonomous-agent
cd autonomous-agent

# Install backend
uv sync
cp .env.example .env

# Terminal 1 — Qdrant
./qdrant.exe

# Terminal 2 — Backend
uvicorn backend.main:app --reload --port 8000

# Terminal 3 — Agents
python run_agents.py

# Terminal 4 — Frontend
cd frontend && npm install && npm run dev

# Seed default user
python seed_user.py
# Login → admin / admin123
```

### Required environment variables
```bash
GROQ_API_KEY=        # groq.com — free tier
TAVILY_API_KEY=      # tavily.com — free tier
JWT_SECRET_KEY=      # any random string
POSTGRES_HOST=       # localhost
POSTGRES_PORT=       # 5432
POSTGRES_DB=         # autonomous_agent
POSTGRES_USER=       # postgres
POSTGRES_PASSWORD=   # your password
REDIS_HOST=          # localhost
REDIS_PORT=          # 6379
QDRANT_HOST=         # localhost
QDRANT_PORT=         # 6333
```

---

## 🧪 Tests

```bash
pytest tests/ -v --cov=. --cov-report=term-missing
# 69 tests · 85% coverage · 0 warnings
```

---

## 🗺️ Phases completed

| Phase | What was built |
|---|---|
| ✅ Phase 1 | Local infrastructure — PostgreSQL · Redis · Qdrant |
| ✅ Phase 2 | FastAPI gateway — JWT auth · endpoints · WebSocket |
| ✅ Phase 3 | Orchestrator — Planner · Dispatcher · Task queue |
| ✅ Phase 4 | 5 specialist agents with retry and dependency logic |
| ✅ Phase 5 | Tool router — central registry · embeddings · logging |
| ✅ Phase 6 | React frontend — dashboard · live feed · pipeline view |
| ✅ Phase 7 | Hardening — structured logs · rate limiting · env validation |

---

<div align="center">

**Built by [Abhishek Saini](https://linkedin.com/in/abhi00574)**
Frontend Engineer · Tech Mahindra

*FastAPI · React · PostgreSQL · Redis · Qdrant · Groq · Tavily · Playwright*

⭐ **Star this repo if you found it interesting**

</div>
```
