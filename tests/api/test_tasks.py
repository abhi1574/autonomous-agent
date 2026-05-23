import pytest
from unittest.mock import patch, MagicMock

def test_create_task_success(client, auth_headers):
    with patch("backend.routers.tasks.planner") as mock_planner, \
         patch("backend.routers.tasks.dispatcher") as mock_dispatcher, \
         patch("backend.routers.tasks.task_mem"):

        mock_planner.plan.return_value  = []
        mock_dispatcher.dispatch.return_value = []

        response = client.post(
            "/api/tasks",
            json={"title": "Test task", "description": "Test description"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"]  == "Test task"
        assert data["status"] == "pending"
        assert "id" in data

def test_create_task_no_auth(client):
    response = client.post(
        "/api/tasks",
        json={"title": "Test task"}
    )
    assert response.status_code == 401

def test_create_task_missing_title(client, auth_headers):
    response = client.post(
        "/api/tasks",
        json={"description": "No title"},
        headers=auth_headers
    )
    assert response.status_code == 422

def test_get_task_success(client, auth_headers):
    with patch("backend.routers.tasks.planner") as mock_planner, \
         patch("backend.routers.tasks.dispatcher"), \
         patch("backend.routers.tasks.task_mem"):

        mock_planner.plan.return_value = []

        # Create task first
        create = client.post(
            "/api/tasks",
            json={"title": "Get test", "description": "Test"},
            headers=auth_headers
        )
        task_id = create.json()["id"]

        # Now get it
        response = client.get(f"/api/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["id"] == task_id

def test_get_task_not_found(client, auth_headers):
    response = client.get(
        "/api/tasks/00000000-0000-0000-0000-000000000000",
        headers=auth_headers
    )
    assert response.status_code == 404

def test_get_task_no_auth(client):
    response = client.get("/api/tasks/some-id")
    assert response.status_code == 401

def test_list_tasks_success(client, auth_headers):
    response = client.get("/api/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_tasks_no_auth(client):
    response = client.get("/api/tasks")
    assert response.status_code == 401

def test_get_tool_logs_success(client, auth_headers):
    response = client.get("/api/tool-logs", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)