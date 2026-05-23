import pytest
from unittest.mock import patch, MagicMock

def test_router_logs_every_call():
    """Test: every tool call gets logged to PostgreSQL"""
    with patch("tools.router.SessionLocal") as mock_session, \
         patch("tools.embeddings.SentenceTransformer") as mock_st:

        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_st.return_value.encode.return_value = [0.1] * 384

        from tools.router       import ToolRouter
        from tools.code_executor import CodeExecutorTool

        router = ToolRouter()
        router._tools["code_executor"] = CodeExecutorTool()

        router.run(
            tool_name  = "code_executor",
            input      = {"code": "print('test')"},
            agent_name = "coding",
            task_id    = "task-1"
        )

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

def test_router_returns_error_for_unknown_tool():
    with patch("tools.router.SessionLocal"), \
         patch("tools.embeddings.SentenceTransformer"):

        from tools.router import ToolRouter
        router = ToolRouter()
        result = router.run(
            tool_name  = "nonexistent_tool",
            input      = {},
            agent_name = "test"
        )
        assert "Unknown tool" in result

def test_router_handles_tool_failure():
    with patch("tools.router.SessionLocal") as mock_session, \
         patch("tools.embeddings.SentenceTransformer"):

        mock_db = MagicMock()
        mock_session.return_value = mock_db

        from tools.router import ToolRouter
        router = ToolRouter()

        # Make a tool raise an exception
        router._tools["code_executor"] = MagicMock()
        router._tools["code_executor"].run.side_effect = Exception("Tool crashed")

        result = router.run(
            tool_name  = "code_executor",
            input      = {},
            agent_name = "coding"
        )

        assert "Tool error" in result
        # Should still log even on failure
        mock_db.commit.assert_called_once()