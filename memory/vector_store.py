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
VECTOR_SIZE     = 384

class VectorStore:
    def __init__(self):
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        qdrant_host    = os.getenv("QDRANT_HOST", "localhost")
        qdrant_port    = int(os.getenv("QDRANT_PORT", 6333))

        if qdrant_api_key:
            # Qdrant Cloud
            self.client = QdrantClient(
                host   =qdrant_host,
                port   =qdrant_port,
                api_key=qdrant_api_key,
                https  =True
            )
        else:
            # Local Qdrant
            self.client = QdrantClient(
                host=qdrant_host,
                port=qdrant_port
            )

        self.collection_name = "agent_memory"
        self._ensure_collection()

    def _ensure_collection(self):
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

    def store(
        self,
        text    : str,
        metadata: dict,
        vector  : list[float]   # caller always provides real vector
    ) -> str:
        point_id = str(uuid.uuid4())
        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id     = point_id,
                    vector = vector,
                    payload= {"text": text, **metadata}
                )
            ]
        )
        return point_id

    def search(
        self,
        vector   : list[float],  # caller always provides real vector
        limit    : int = 5,
        filter_by: dict = None
    ) -> list[dict]:
        query_filter = None
        if filter_by:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key  = k,
                        match= MatchValue(value=v)
                    ) for k, v in filter_by.items()
                ]
            )

        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query         = vector,
            limit         = limit,
            query_filter  = query_filter
        ).points

        return [
            {
                "score"   : r.score,
                "text"    : r.payload.get("text"),
                "metadata": r.payload
            }
            for r in results
        ]