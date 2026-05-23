import pytest
from unittest.mock import patch, MagicMock

def test_research_stores_rag_retrieves():
    """Test: Research stores to Qdrant → RAG retrieves it"""
    with patch("agents.orchestrator.task_queue.redis.Redis"), \
         patch("memory.task_memory.SessionLocal"), \
         patch("tools.router.ToolRouter.embed") as mock_embed, \
         patch("memory.vector_store.QdrantClient") as mock_qdrant, \
         patch("tools.web_search.TavilyClient") as mock_tavily, \
         patch("tools.llm.Groq") as mock_groq, \
         patch("tools.router.ToolRouter._log"):

        # Setup mocks
        mock_embed.return_value = [0.1] * 384

        mock_tavily.return_value.search.return_value = {
            "results": [{"title": "AI News", "url": "http://test.com", "content": "AI is growing"}]
        }

        mock_qdrant_client = MagicMock()
        mock_qdrant.return_value = mock_qdrant_client
        mock_qdrant_client.get_collections.return_value.collections = []

        mock_search_result       = MagicMock()
        mock_search_result.score = 0.95
        mock_search_result.payload = {
            "text" : "AI is growing",
            "agent": "research",
            "task_id": "test-task-1"
        }
        mock_qdrant_client.query_points.return_value.points = [mock_search_result]

        mock_llm_response = MagicMock()
        mock_llm_response.choices[0].message.content = "Based on context: AI is growing rapidly"
        mock_groq.return_value.chat.completions.create.return_value = mock_llm_response

        from agents.research_agent import ResearchAgent
        from agents.rag_agent      import RAGAgent

        research_job = {
            "job_id": "job-1", "task_id": "test-task-1",
            "subtask_id": "1", "agent": "research",
            "title": "Find AI info", "description": "Search for AI trends",
            "depends_on": []
        }

        rag_job = {
            "job_id": "job-2", "task_id": "test-task-1",
            "subtask_id": "2", "agent": "rag",
            "title": "Retrieve AI info", "description": "Find AI trends from knowledge base",
            "depends_on": ["1"]
        }

        research = ResearchAgent()
        result   = research.execute(research_job)
        assert "AI" in result

        rag    = RAGAgent()
        result = rag.execute(rag_job)
        assert len(result) > 0