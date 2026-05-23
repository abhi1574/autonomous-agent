from sentence_transformers import SentenceTransformer
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

class EmbeddingTool:
    name        = "embeddings"
    description = "Generate vector embeddings from text"

    def __init__(self):
        print("⏳ Loading embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")  # 384 dimensions
        print("✅ Embedding model loaded")

    def embed(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()