from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams,
    PointStruct, Filter,
    FieldCondition, MatchValue
)
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

COLLECTION_NAME = "agent_memory"
VECTOR_SIZE     = 384  # will use embedding model in Phase 4

class VectorStore:
    def __init__(self):
        self.client = QdrantClient(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", 6333))
        )
        self._ensure_collection()

    def _ensure_collection(self):
        """Create collection if it doesn't exist"""
        collections = [c.name for c in self.client.get_collections().collections]
        if COLLECTION_NAME not in collections:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=VECTOR_SIZE,
                    distance=Distance.COSINE
                )
            )
            print(f"✅ Created Qdrant collection: {COLLECTION_NAME}")
        else:
            print(f"✅ Qdrant collection exists: {COLLECTION_NAME}")

    def store(self, text: str, metadata: dict, vector: list[float]) -> str:
        """Store a memory with its vector embedding"""
        point_id = str(uuid.uuid4())
        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={"text": text, **metadata}
                )
            ]
        )
        return point_id

    def search(self, vector: list[float], limit: int = 5, filter_by: dict = None) -> list[dict]:
        """Search for similar memories"""
        query_filter = None
        if filter_by:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key=k,
                        match=MatchValue(value=v)
                    ) for k, v in filter_by.items()
                ]
            )

        results = self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=limit,
            query_filter=query_filter
        )

        return [
            {"score": r.score, "text": r.payload.get("text"), "metadata": r.payload}
            for r in results
        ]