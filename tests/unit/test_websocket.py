import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_connect_adds_client():
    from backend.websocket.manager import ConnectionManager
    manager   = ConnectionManager()
    mock_ws   = AsyncMock()
    await manager.connect(mock_ws, "client-1")
    assert "client-1" in manager.active_connections
    mock_ws.accept.assert_called_once()

@pytest.mark.asyncio
async def test_disconnect_removes_client():
    from backend.websocket.manager import ConnectionManager
    manager   = ConnectionManager()
    mock_ws   = AsyncMock()
    await manager.connect(mock_ws, "client-1")
    manager.disconnect("client-1")
    assert "client-1" not in manager.active_connections

@pytest.mark.asyncio
async def test_send_to_client():
    from backend.websocket.manager import ConnectionManager
    manager   = ConnectionManager()
    mock_ws   = AsyncMock()
    await manager.connect(mock_ws, "client-1")
    await manager.send_to_client("client-1", {"event": "test"})
    mock_ws.send_json.assert_called_once_with({"event": "test"})

@pytest.mark.asyncio
async def test_broadcast_to_all():
    from backend.websocket.manager import ConnectionManager
    manager  = ConnectionManager()
    mock_ws1 = AsyncMock()
    mock_ws2 = AsyncMock()
    await manager.connect(mock_ws1, "client-1")
    await manager.connect(mock_ws2, "client-2")
    await manager.broadcast({"event": "update"})
    mock_ws1.send_json.assert_called_once_with({"event": "update"})
    mock_ws2.send_json.assert_called_once_with({"event": "update"})