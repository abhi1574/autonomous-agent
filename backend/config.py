import os
from dotenv import load_dotenv

load_dotenv()

REQUIRED_VARS = [
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "POSTGRES_DB",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "REDIS_HOST",
    "REDIS_PORT",
    "QDRANT_HOST",
    "QDRANT_PORT",
    "GROQ_API_KEY",
    "TAVILY_API_KEY",
    "JWT_SECRET_KEY",
]

def validate_env():
    missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
    if missing:
        raise EnvironmentError(
            f"❌ Missing required environment variables: {', '.join(missing)}\n"
            f"Please check your .env file."
        )
    return True

class Settings:
    POSTGRES_HOST    : str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT    : int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB      : str = os.getenv("POSTGRES_DB", "autonomous_agent")
    POSTGRES_USER    : str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    REDIS_HOST       : str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT       : int = int(os.getenv("REDIS_PORT", 6379))
    QDRANT_HOST      : str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT      : int = int(os.getenv("QDRANT_PORT", 6333))
    GROQ_API_KEY     : str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL       : str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    TAVILY_API_KEY   : str = os.getenv("TAVILY_API_KEY", "")
    JWT_SECRET_KEY   : str = os.getenv("JWT_SECRET_KEY", "change-this")
    CORS_ORIGINS     : list = ["http://localhost:5173"]

settings = Settings()