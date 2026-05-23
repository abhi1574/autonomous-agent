import pytest
from unittest.mock import MagicMock, patch
from agents.orchestrator.task_queue import TaskQueue

@pytest.fixture
def queue():
    with patch("agents.orchestrator.task_queue.redis.Redis") as mock_redis:
        mock_client        = MagicMock()
        mock_redis.return_value = mock_client
        q                  = TaskQueue()
        q.client           = mock_client
        yield q, mock_client

def test_push_success(queue):
    q, mock_client = queue
    mock_client.lpush.return_value = 1
    result = q.push({"job_id": "1", "agent": "research"})
    assert result == True
    mock_client.lpush.assert_called_once()

def test_push_failure(queue):
    q, mock_client = queue
    mock_client.lpush.side_effect = Exception("Redis down")
    result = q.push({"job_id": "1"})
    assert result == False

def test_pop_returns_job(queue):
    q, mock_client = queue
    mock_client.brpop.return_value = ("task_queue", '{"job_id": "1"}')
    result = q.pop()
    assert result == {"job_id": "1"}

def test_pop_returns_none_on_timeout(queue):
    q, mock_client = queue
    mock_client.brpop.return_value = None
    result = q.pop()
    assert result is None

def test_size(queue):
    q, mock_client = queue
    mock_client.llen.return_value = 5
    assert q.size() == 5

def test_clear(queue):
    q, mock_client = queue
    mock_client.delete.return_value = 1
    assert q.clear() == True

def test_mark_completed(queue):
    q, mock_client = queue
    q.mark_completed("task-1", "subtask-1")
    mock_client.sadd.assert_called_once_with("completed:task-1", "subtask-1")

def test_dependencies_met_no_deps(queue):
    q, _ = queue
    assert q.dependencies_met("task-1", []) == True

def test_dependencies_met_all_done(queue):
    q, mock_client = queue
    mock_client.smembers.return_value = {"1", "2"}
    assert q.dependencies_met("task-1", ["1", "2"]) == True

def test_dependencies_not_met(queue):
    q, mock_client = queue
    mock_client.smembers.return_value = {"1"}
    assert q.dependencies_met("task-1", ["1", "2"]) == False