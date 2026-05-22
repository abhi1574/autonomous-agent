from agents.base_agent import BaseAgent
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

class RAGAgent(BaseAgent):
    def __init__(self):
        super().__init__("rag")
        self.groq  = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    def execute(self, job: dict) -> str:
        query = job.get("description") or job.get("title")

        # Search Qdrant for relevant past memories
        results = self.vector.search(
            vector=[0.0] * 384,  # placeholder — real embeddings in Phase 5
            limit=5,
            filter_by={"agent": "research"}
        )

        if not results:
            return f"No relevant memories found in knowledge base for: {query}"

        # Build context from retrieved memories
        context = "\n\n".join([
            f"Memory {i+1}: {r.get('text', '')[:500]}"
            for i, r in enumerate(results)
        ])

        # Use Groq to synthesise answer from context
        response = self.groq.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a knowledge retrieval assistant. Answer based only on the provided context."
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {query}"
                }
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content