import os
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue
)
from dotenv import load_dotenv
import uuid

load_dotenv()

class VectorStore:
    def __init__(self):
        qdrant_api_key = os.getenv("QDRANT_API_KEY", "").strip()
        qdrant_host    = os.getenv("QDRANT_HOST", "localhost")
        qdrant_port    = int(os.getenv("QDRANT_PORT", 6333))

        if qdrant_api_key:
            self.client = QdrantClient(
                host   =qdrant_host,
                port   =qdrant_port,
                api_key=qdrant_api_key,
                https  =True
            )
        else:
            self.client = QdrantClient(
                host=qdrant_host,
                port=qdrant_port
            )

        self.collection_name = "agent_memory"
        self._ensure_collection()

    def _ensure_collection(self):
        existing = [c.name for c in self.client.get_collections().collections]
        if self.collection_name not in existing:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config =VectorParams(size=384, distance=Distance.COSINE)
            )
            print(f"✅ Created Qdrant collection: {self.collection_name}")
        else:
            print(f"✅ Qdrant collection exists: {self.collection_name}")

    def store(self, text: str, metadata: dict, vector: list) -> str:
        point_id = str(uuid.uuid4())
        self.client.upsert(
            collection_name=self.collection_name,
            points=[PointStruct(
                id     =point_id,
                vector =vector,
                payload={**metadata, "text": text}
            )]
        )
        return point_id

    def search(self, vector: list, limit: int = 5, filter_by: dict = None):
        query_filter = None
        if filter_by:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key  =k,
                        match=MatchValue(value=v)
                    )
                    for k, v in filter_by.items()
                ]
            )
        results = self.client.query_points(
            collection_name=self.collection_name,
            query          =vector,
            limit          =limit,
            query_filter   =query_filter
        ).points

        return [
            {
                "id"      : str(r.id),
                "score"   : r.score,
                "text"    : r.payload.get("text", ""),
                "metadata": r.payload
            }
            for r in results
        ]