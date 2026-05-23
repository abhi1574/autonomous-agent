from agents.base_agent import BaseAgent
import time

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__("research")

    def execute(self, job: dict) -> str:
        query   = job.get("description") or job.get("title")
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
                print(f"⚠️ Research attempt {attempt+1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # exponential backoff

        return f"Research failed after {retries} attempts for: {query}"