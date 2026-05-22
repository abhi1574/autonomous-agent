import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.research_agent import ResearchAgent
from agents.rag_agent import RAGAgent
from agents.critic_agent import CriticAgent
from agents.coding_agent import CodingAgent

# Test job template
def make_job(agent: str, title: str, description: str) -> dict:
    return {
        "job_id"     : "test-001",
        "task_id"    : "00000000-0000-0000-0000-000000000001",
        "subtask_id" : "1",
        "agent"      : agent,
        "title"      : title,
        "description": description,
        "depends_on" : []
    }

print("\n--- Testing Research Agent ---")
research = ResearchAgent()
result   = research.execute(make_job(
    "research",
    "Latest AI agent frameworks",
    "Find the latest AI agent frameworks in 2025"
))
print(result[:500])

print("\n--- Testing Coding Agent ---")
coding = CodingAgent()
result = coding.execute(make_job(
    "coding",
    "Write fibonacci function",
    "Write a Python function that returns the nth fibonacci number"
))
print(result[:500])

print("\n--- Testing Critic Agent ---")
critic = CriticAgent()
result = critic.execute(make_job(
    "critic",
    "Review research findings",
    "Review and critique the latest AI agent research findings"
))
print(result[:500])

print("\n--- Testing RAG Agent ---")
rag    = RAGAgent()
result = rag.execute(make_job(
    "rag",
    "Search knowledge base",
    "Find relevant information about AI agents from knowledge base"
))
print(result[:500])