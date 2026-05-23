import pytest
from unittest.mock import patch, MagicMock

def test_full_orchestration_flow():
    """Test: task → planner → dispatcher → redis queue"""
    with patch("agents.orchestrator.planner.Groq") as mock_groq, \
         patch("agents.orchestrator.task_queue.redis.Redis") as mock_redis:

        mock_response = MagicMock()
        mock_response.choices[0].message.content = '''[
            {"subtask_id": "1", "title": "Search", "description": "Find AI info",
             "agent": "research", "depends_on": []},
            {"subtask_id": "2", "title": "Critique", "description": "Review findings",
             "agent": "critic", "depends_on": ["1"]}
        ]'''
        mock_groq.return_value.chat.completions.create.return_value = mock_response
        mock_redis.return_value.lpush.return_value = 1

        from agents.orchestrator.planner    import Planner
        from agents.orchestrator.dispatcher import Dispatcher

        planner    = Planner()
        dispatcher = Dispatcher()

        subtasks   = planner.plan("Research AI", "Find latest AI info")
        assert len(subtasks) == 2

        dispatched = dispatcher.dispatch("task-123", subtasks)
        assert len(dispatched) == 2

        # Independent subtask dispatched first
        assert dispatched[0]["subtask_id"] == "1"
        assert dispatched[1]["depends_on"] == ["1"]

def test_planner_dispatcher_skips_invalid_agent():
    with patch("agents.orchestrator.planner.Groq") as mock_groq, \
         patch("agents.orchestrator.task_queue.redis.Redis"):

        mock_response = MagicMock()
        mock_response.choices[0].message.content = '''[
            {"subtask_id": "1", "title": "T", "description": "D",
             "agent": "invalid_agent", "depends_on": []}
        ]'''
        mock_groq.return_value.chat.completions.create.return_value = mock_response

        from agents.orchestrator.planner    import Planner
        from agents.orchestrator.dispatcher import Dispatcher

        planner    = Planner()
        dispatcher = Dispatcher()

        subtasks   = planner.plan("Test", "Test")
        dispatched = dispatcher.dispatch("task-123", subtasks)
        assert len(dispatched) == 0