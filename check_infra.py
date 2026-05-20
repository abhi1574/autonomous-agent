import psycopg2, redis, os
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL
try:
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    print("✅ PostgreSQL connected")
    conn.close()
except Exception as e:
    print(f"❌ PostgreSQL failed: {e}")

# Redis
try:
    r = redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT"))
    )
    r.ping()
    print("✅ Redis connected")
except Exception as e:
    print(f"❌ Redis failed: {e}")

# Qdrant
try:
    client = QdrantClient(
        host=os.getenv("QDRANT_HOST"),
        port=int(os.getenv("QDRANT_PORT"))
    )
    client.get_collections()
    print("✅ Qdrant connected")
except Exception as e:
    print(f"❌ Qdrant failed: {e}")