import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_job():
    return {
        "job_id"     : "job-1",
        "task_id"    : "task-1",
        "subtask_id" : "1",
        "agent"      : "coding",
        "title"      : "Write fibonacci",
        "description": "Write a Python fibonacci function",
        "depends_on" : []
    }

def test_coding_agent_execute(mock_job):
    with patch("agents.orchestrator.task_queue.redis.Redis"), \
         patch("memory.task_memory.SessionLocal"), \
         patch("memory.vector_store.QdrantClient") as mock_qdrant, \
         patch("tools.router.get_router") as mock_get_router:

        mock_qdrant.return_value.get_collections.return_value.collections = []
        mock_router = MagicMock()
        mock_router.run.side_effect = lambda tool_name, input, **kwargs: (
            "def fibonacci(n): return n" if tool_name == "llm"
            else "Output:\n0"
        )
        mock_get_router.return_value = mock_router

        from agents.coding_agent import CodingAgent
        agent  = CodingAgent()
        result = agent.execute(mock_job)
        assert "fibonacci" in result or "Generated Code" in result

def test_critic_agent_execute(mock_job):
    with patch("agents.orchestrator.task_queue.redis.Redis"), \
         patch("memory.task_memory.SessionLocal"), \
         patch("memory.vector_store.QdrantClient") as mock_qdrant, \
         patch("tools.router.get_router") as mock_get_router:

        mock_qdrant.return_value.get_collections.return_value.collections = []

        mock_router        = MagicMock()
        mock_vector        = MagicMock()
        mock_vector.search.return_value = [{
            "score"   : 0.9,
            "text"    : "Some research output",
            "metadata": {"agent": "research"}
        }]
        mock_router.run.return_value = "Strengths: Good research. Score: 8/10"

        mock_get_router.return_value = mock_router

        from agents.critic_agent import CriticAgent
        agent        = CriticAgent()
        agent.vector = mock_vector
        result       = agent.execute({**mock_job, "agent": "critic"})
        assert len(result) > 0

def test_critic_agent_no_memories(mock_job):
    with patch("agents.orchestrator.task_queue.redis.Redis"), \
         patch("memory.task_memory.SessionLocal"), \
         patch("memory.vector_store.QdrantClient") as mock_qdrant, \
         patch("tools.router.get_router") as mock_get_router:

        mock_qdrant.return_value.get_collections.return_value.collections = []
        mock_router        = MagicMock()
        mock_vector        = MagicMock()
        mock_vector.search.return_value = []
        mock_get_router.return_value    = mock_router

        from agents.critic_agent import CriticAgent
        agent        = CriticAgent()
        agent.vector = mock_vector
        result       = agent.execute({**mock_job, "agent": "critic"})
        assert result == "No output available to critique yet."

def test_research_agent_execute(mock_job):
    with patch("agents.orchestrator.task_queue.redis.Redis"), \
         patch("memory.task_memory.SessionLocal"), \
         patch("memory.vector_store.QdrantClient") as mock_qdrant, \
         patch("tools.router.get_router") as mock_get_router:

        mock_qdrant.return_value.get_collections.return_value.collections = []
        mock_router     = MagicMock()
        mock_router.run.return_value = "Research results: AI frameworks"
        mock_get_router.return_value = mock_router

        from agents.research_agent import ResearchAgent
        agent  = ResearchAgent()
        result = agent.execute({**mock_job, "agent": "research"})
        assert "Research results" in result or len(result) > 0

def test_rag_agent_no_memories(mock_job):
    with patch("agents.orchestrator.task_queue.redis.Redis"), \
         patch("memory.task_memory.SessionLocal"), \
         patch("memory.vector_store.QdrantClient") as mock_qdrant, \
         patch("tools.router.get_router") as mock_get_router:

        mock_qdrant.return_value.get_collections.return_value.collections = []
        mock_router        = MagicMock()
        mock_router.embed.return_value  = [0.1] * 384
        mock_vector        = MagicMock()
        mock_vector.search.return_value = []
        mock_get_router.return_value    = mock_router

        from agents.rag_agent import RAGAgent
        agent        = RAGAgent()
        agent.vector = mock_vector
        result       = agent.execute({**mock_job, "agent": "rag"})
        assert "No relevant memories" in result