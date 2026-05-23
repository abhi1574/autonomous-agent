import pytest
from unittest.mock import MagicMock, patch

def test_code_executor_success():
    from tools.code_executor import CodeExecutorTool
    tool   = CodeExecutorTool()
    result = tool.run({"code": "print('hello')"})
    assert "hello" in result

def test_code_executor_timeout():
    from tools.code_executor import CodeExecutorTool
    tool   = CodeExecutorTool()
    result = tool.run({"code": "import time; time.sleep(30)", "timeout": 1})
    assert "timed out" in result.lower()

def test_code_executor_empty_code():
    from tools.code_executor import CodeExecutorTool
    tool   = CodeExecutorTool()
    result = tool.run({"code": ""})
    assert "No code provided" in result

def test_code_executor_syntax_error():
    from tools.code_executor import CodeExecutorTool
    tool   = CodeExecutorTool()
    result = tool.run({"code": "def broken(:"})
    assert "Error" in result or "error" in result

def test_llm_tool_returns_string():
    from tools.llm import LLMTool
    with patch("tools.llm.Groq") as mock_groq:
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Test response"
        mock_groq.return_value.chat.completions.create.return_value = mock_response
        tool   = LLMTool()
        result = tool.run({"prompt": "Hello"})
        assert result == "Test response"

def test_embeddings_returns_correct_size():
    from tools.embeddings import EmbeddingTool
    tool   = EmbeddingTool()
    vector = tool.embed("Test text")
    assert len(vector) == 384
    assert isinstance(vector[0], float)

def test_vector_search_requires_vector():
    from tools.vector_search import VectorSearchTool
    tool   = VectorSearchTool()
    result = tool.run({"limit": 3})
    assert "No vector provided" in result