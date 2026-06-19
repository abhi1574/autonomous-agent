import time
from agents.base_agent import BaseAgent

class RAGAgent(BaseAgent):
    def __init__(self):
        super().__init__("rag")

    def execute(self, job: dict) -> str:
        query        = job.get("description") or job.get("title")
        task_id      = job.get("task_id")
        query_vector = self.router.embed(query)

        # First try: search only within this task's memories
        results = self.vector.search(
            vector   = query_vector,
            limit    = 5,
            filter_by= {"task_id": task_id}  # ← same task only
        )

        # If no results yet — research agent hasn't finished
        # Wait and retry a few times
        attempts = 0
        while not results and attempts < 5:
            self.logger.info(f"RAG waiting for research results — attempt {attempts+1}/5")
            time.sleep(4)
            results = self.vector.search(
                vector   = query_vector,
                limit    = 5,
                filter_by= {"task_id": task_id}
            )
            attempts += 1

        # If still no results — use query directly without RAG context
        if not results:
            self.logger.warning("No task-specific memories found — answering from query directly")
            return self.router.run(
                tool_name  = "llm",
                input      = {
                    "system": "You are a knowledgeable assistant. Answer the question directly and thoroughly.",
                    "prompt": query
                },
                agent_name = self.agent_name,
                task_id    = task_id
            )

        context = "\n\n".join([
            f"Source {i+1}:\n{r.get('text', '')[:600]}"
            for i, r in enumerate(results)
        ])

        return self.router.run(
            tool_name  = "llm",
            input      = {
                "system": "You are a knowledge synthesis assistant. Summarise and synthesise ONLY the provided context. Do not mention memory numbers or sources.",
                "prompt": f"Context:\n{context}\n\nSummarise the key information about: {query}"
            },
            agent_name = self.agent_name,
            task_id    = task_id
        )