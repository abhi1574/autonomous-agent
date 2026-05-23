from agents.base_agent import BaseAgent

class RAGAgent(BaseAgent):
    def __init__(self):
        super().__init__("rag")

    def execute(self, job: dict) -> str:
        query = job.get("description") or job.get("title")

        # Generate real embedding for query
        query_vector = self.router.embed(query)

        # Search Qdrant with real vector
        results = self.vector.search(
            vector=query_vector,
            limit=5,
            filter_by={"agent": "research"}
        )

        if not results:
            return f"No relevant memories found for: {query}"

        # Build context
        context = "\n\n".join([
            f"Memory {i+1} (score: {r['score']:.3f}):\n{r.get('text', '')[:500]}"
            for i, r in enumerate(results)
        ])

        # Synthesise answer via LLM tool
        return self.router.run(
            tool_name  = "llm",
            input      = {
                "system": "You are a knowledge retrieval assistant. Answer based only on the provided context.",
                "prompt": f"Context:\n{context}\n\nQuestion: {query}"
            },
            agent_name = self.agent_name,
            task_id    = job.get("task_id")
        )