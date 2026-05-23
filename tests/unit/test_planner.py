import pytest
from unittest.mock import MagicMock, patch
from agents.orchestrator.planner import Planner

@pytest.fixture
def planner():
    with patch("agents.orchestrator.planner.Groq") as mock_groq:
        p = Planner()
        p.client = mock_groq.return_value
        yield p

def test_plan_returns_subtasks(planner):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = '''[
        {"subtask_id": "1", "title": "Search web", "description": "Find info", "agent": "research", "depends_on": []},
        {"subtask_id": "2", "title": "Review", "description": "Critique", "agent": "critic", "depends_on": ["1"]}
    ]'''
    planner.client.chat.completions.create.return_value = mock_response
    result = planner.plan("Test task", "Test description")
    assert len(result) == 2
    assert result[0]["agent"] == "research"
    assert result[1]["depends_on"] == ["1"]

def test_plan_handles_json_parse_error(planner):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "invalid json"
    planner.client.chat.completions.create.return_value = mock_response
    result = planner.plan("Test task", "Test description")
    assert result == []

def test_plan_handles_api_failure(planner):
    planner.client.chat.completions.create.side_effect = Exception("API down")
    result = planner.plan("Test task", "Test description")
    assert result == []

def test_plan_strips_markdown_fences(planner):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = '```json\n[{"subtask_id": "1", "title": "T", "description": "D", "agent": "research", "depends_on": []}]\n```'
    planner.client.chat.completions.create.return_value = mock_response
    result = planner.plan("Test", "Test")
    assert len(result) == 1