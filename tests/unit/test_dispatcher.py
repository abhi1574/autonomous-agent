import pytest
from unittest.mock import MagicMock, patch
from agents.orchestrator.dispatcher import Dispatcher

@pytest.fixture
def dispatcher():
    with patch("agents.orchestrator.dispatcher.TaskQueue") as mock_queue:
        d = Dispatcher()
        d.queue = mock_queue.return_value
        d.queue.push.return_value = True
        yield d

def test_dispatch_valid_subtasks(dispatcher):
    subtasks = [
        {"subtask_id": "1", "title": "Search", "description": "Find", "agent": "research", "depends_on": []},
        {"subtask_id": "2", "title": "Review", "description": "Critique", "agent": "critic", "depends_on": ["1"]}
    ]
    result = dispatcher.dispatch("task-1", subtasks)
    assert len(result) == 2

def test_dispatch_skips_unknown_agent(dispatcher):
    subtasks = [
        {"subtask_id": "1", "title": "Test", "description": "Test", "agent": "unknown_agent", "depends_on": []}
    ]
    result = dispatcher.dispatch("task-1", subtasks)
    assert len(result) == 0

def test_dispatch_independent_before_dependent(dispatcher):
    subtasks = [
        {"subtask_id": "1", "title": "Dep", "description": "D", "agent": "critic", "depends_on": ["2"]},
        {"subtask_id": "2", "title": "Indep", "description": "D", "agent": "research", "depends_on": []}
    ]
    result = dispatcher.dispatch("task-1", subtasks)
    # Independent (subtask 2) should be dispatched first
    assert result[0]["subtask_id"] == "2"
    assert result[1]["subtask_id"] == "1"

def test_dispatch_adds_retry_count(dispatcher):
    subtasks = [
        {"subtask_id": "1", "title": "T", "description": "D", "agent": "research", "depends_on": []}
    ]
    result = dispatcher.dispatch("task-1", subtasks)
    assert result[0]["retry_count"] == 0

def test_dispatch_adds_timestamp(dispatcher):
    subtasks = [
        {"subtask_id": "1", "title": "T", "description": "D", "agent": "research", "depends_on": []}
    ]
    result = dispatcher.dispatch("task-1", subtasks)
    assert "dispatched_at" in result[0]

def test_get_queue_size(dispatcher):
    dispatcher.queue.size.return_value = 3
    assert dispatcher.get_queue_size() == 3

def test_clear_queue(dispatcher):
    dispatcher.queue.clear.return_value = True
    assert dispatcher.clear_queue() == True