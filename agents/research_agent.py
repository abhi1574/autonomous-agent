from agents.base_agent import BaseAgent
import time

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__("research")

    def execute(self, job: dict) -> str:
        # Use description first, fall back to title, then use a default
        query = job.get("description") or job.get("title") or "latest trends"
        query = query.strip() if query else "latest trends"

        if not query or query == "None":
            return "No search query provided for this subtask"

        retries = 3
        for attempt in range(retries):
            try:
                return self.router.run(
                    tool_name  = "web_search",
                    input      = {"query": query, "max_results": 5},
                    agent_name = self.agent_name,
                    task_id    = job.get("task_id")
                )
            except Exception as e:
                self.logger.warning(f"Research attempt {attempt+1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)

        return f"Research failed after {retries} attempts for: {query}"