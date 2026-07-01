<div align="center">

# 🤖 Autonomous Multi-Agent Platform

A full-stack platform for orchestrating AI agents, semantic memory, and real-time task execution.

![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React_18-61DAFB?style=flat&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-FF4081?style=flat)

</div>

---

## 🚀 Overview

A personal project to explore multi-agent systems, task orchestration, vector memory, and real-time monitoring.

Users submit a task, which is broken into subtasks and executed by specialized agents including Research, RAG, Coding, Browser, and Critic agents. Results are streamed back through a React dashboard.

---

## 🛠️ Tech Stack

**Frontend**
- React 18
- TypeScript
- Tailwind CSS
- Zustand
- WebSockets

**Backend**
- FastAPI
- Python 3.11
- SQLAlchemy
- JWT Authentication

**Infrastructure**
- PostgreSQL
- Redis
- Qdrant Vector DB

**AI**
- Groq LLaMA 3.3
- Tavily Search
- Sentence Transformers

---

## ✨ Highlights

- Multi-agent orchestration
- Redis-backed task queue
- Vector memory with Qdrant
- Real-time updates via WebSockets
- Modular and scalable architecture
- Automated testing

---

## 🏗️ Architecture

```text
React Dashboard
       │
REST + WebSocket
       │
FastAPI Gateway
       │
┌──────┼──────┐
▼      ▼      ▼
PG    Redis  Agents
              │
              ▼
           Qdrant
```

---

## 🚀 Getting Started

```bash
git clone https://github.com/abhi1574/autonomous-agent.git
cd autonomous-agent

uv sync
cp .env.example .env

uvicorn backend.main:app --reload
python run_agents.py

cd frontend
npm install
npm run dev
```

---

## 👨‍💻 Author

**Abhishek Saini**

Frontend Engineer | React.js • TypeScript • Vue.js

🔗 LinkedIn: https://linkedin.com/in/abhi00574