import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture
def vector_store():
    with patch("memory.vector_store.QdrantClient") as mock_qdrant:
        mock_client = MagicMock()
        mock_qdrant.return_value = mock_client

        # Simulate collection already exists
        mock_collection      = MagicMock()
        mock_collection.name = "agent_memory"
        mock_client.get_collections.return_value.collections = [mock_collection]

        from memory.vector_store import VectorStore
        store        = VectorStore()
        store.client = mock_client
        yield store, mock_client

def test_collection_created_if_not_exists():
    with patch("memory.vector_store.QdrantClient") as mock_qdrant:
        mock_client = MagicMock()
        mock_qdrant.return_value = mock_client

        # Simulate no collections exist
        mock_client.get_collections.return_value.collections = []

        from memory.vector_store import VectorStore
        VectorStore()

        mock_client.create_collection.assert_called_once()

def test_collection_not_recreated_if_exists(vector_store):
    _, mock_client = vector_store
    mock_client.create_collection.assert_not_called()

def test_store_returns_point_id(vector_store):
    store, mock_client = vector_store
    mock_client.upsert.return_value = None

    point_id = store.store(
        text    = "Test result",
        metadata= {"agent": "research", "task_id": "task-1"},
        vector  = [0.1] * 384
    )

    assert isinstance(point_id, str)
    assert len(point_id) > 0
    mock_client.upsert.assert_called_once()

def test_store_includes_text_in_payload(vector_store):
    store, mock_client = vector_store
    store.store(
        text    = "Important finding",
        metadata= {"agent": "research"},
        vector  = [0.1] * 384
    )

    call_args = mock_client.upsert.call_args
    points    = call_args.kwargs.get("points") or call_args.args[1]
    assert points[0].payload["text"]  == "Important finding"
    assert points[0].payload["agent"] == "research"

def test_search_returns_results(vector_store):
    store, mock_client = vector_store

    mock_result         = MagicMock()
    mock_result.score   = 0.95
    mock_result.payload = {
        "text"   : "AI research result",
        "agent"  : "research",
        "task_id": "task-1"
    }
    mock_client.query_points.return_value.points = [mock_result]

    results = store.search(vector=[0.1] * 384, limit=5)

    assert len(results) == 1
    assert results[0]["score"]         == 0.95
    assert results[0]["text"]          == "AI research result"
    assert results[0]["metadata"]["agent"] == "research"

def test_search_returns_empty_list(vector_store):
    store, mock_client = vector_store
    mock_client.query_points.return_value.points = []

    results = store.search(vector=[0.1] * 384, limit=5)
    assert results == []

def test_search_with_filter(vector_store):
    store, mock_client = vector_store
    mock_client.query_points.return_value.points = []

    store.search(
        vector   = [0.1] * 384,
        limit    = 3,
        filter_by= {"agent": "research"}
    )

    call_args    = mock_client.query_points.call_args
    query_filter = call_args.kwargs.get("query_filter")
    assert query_filter is not None

def test_search_without_filter(vector_store):
    store, mock_client = vector_store
    mock_client.query_points.return_value.points = []

    store.search(vector=[0.1] * 384, limit=3)

    call_args    = mock_client.query_points.call_args
    query_filter = call_args.kwargs.get("query_filter")
    assert query_filter is None