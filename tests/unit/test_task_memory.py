import pytest
from unittest.mock import MagicMock, patch
from memory.task_memory import TaskMemory
from backend.models.task import TaskStatus

@pytest.fixture
def task_memory():
    with patch("memory.task_memory.SessionLocal") as mock_session:
        tm         = TaskMemory()
        mock_db    = MagicMock()
        mock_session.return_value = mock_db
        yield tm, mock_db

def test_update_task_status_success(task_memory):
    tm, mock_db  = task_memory
    mock_task    = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_task
    tm.update_task_status("task-1", TaskStatus.completed, "done")
    assert mock_task.status == TaskStatus.completed
    assert mock_task.result == "done"
    mock_db.commit.assert_called_once()

def test_update_task_status_not_found(task_memory):
    tm, mock_db = task_memory
    mock_db.query.return_value.filter.return_value.first.return_value = None
    # Should not raise — just log
    tm.update_task_status("nonexistent", TaskStatus.failed)

def test_get_task_returns_dict(task_memory):
    tm, mock_db  = task_memory
    mock_task    = MagicMock()
    mock_task.id = "task-1"
    mock_task.title       = "Test"
    mock_task.description = "Desc"
    mock_task.status      = TaskStatus.pending
    mock_task.result      = None
    mock_db.query.return_value.filter.return_value.first.return_value = mock_task
    result = tm.get_task("task-1")
    assert result["title"] == "Test"

def test_get_task_not_found(task_memory):
    tm, mock_db = task_memory
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = tm.get_task("nonexistent")
    assert result is None