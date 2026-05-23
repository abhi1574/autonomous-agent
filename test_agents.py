import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.research_agent import ResearchAgent
from agents.rag_agent import RAGAgent
from agents.critic_agent import CriticAgent
from agents.coding_agent import CodingAgent

SHARED_TASK_ID = "00000000-0000-0000-0000-000000000001"

def make_job(agent, title, description):
    return {
        "job_id"     : "test-001",
        "task_id"    : SHARED_TASK_ID,  # same ID across all agents
        "subtask_id" : "1",
        "agent"      : agent,
        "title"      : title,
        "description": description,
        "depends_on" : []
    }

# Step 1 — Research stores results to Qdrant
print("\n--- Step 1: Research Agent (stores to Qdrant) ---")
research = ResearchAgent()
result   = research.test_execute(make_job(
    "research",
    "Latest AI agent frameworks",
    "Find the latest AI agent frameworks in 2025"
))
print(result[:300])

# Step 2 — RAG reads what Research stored
print("\n--- Step 2: RAG Agent (reads from Qdrant) ---")
rag    = RAGAgent()
result = rag.execute(make_job(
    "rag",
    "Search knowledge base for AI frameworks",
    "Find relevant information about AI agents from knowledge base"
))
print(result[:300])

# Step 3 — Critic reviews what Research stored
print("\n--- Step 3: Critic Agent (reviews Research output) ---")
critic = CriticAgent()
result = critic.execute(make_job(
    "critic",
    "Review AI framework research",
    "Review and critique the latest AI agent research findings"
))
print(result[:300])

# Step 4 — Coding
print("\n--- Step 4: Coding Agent ---")
coding = CodingAgent()
result = coding.execute(make_job(
    "coding",
    "Write fibonacci function",
    "Write a Python function that returns the nth fibonacci number"
))
print(result[:300])