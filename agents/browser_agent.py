from agents.base_agent import BaseAgent

class BrowserAgent(BaseAgent):
    def __init__(self):
        super().__init__("browser")

    def execute(self, job: dict) -> str:
        task = job.get("description") or job.get("title")
        url  = self._extract_url(task)

        if not url:
            return f"No URL found in task: {task}"

        return self.router.run(
            tool_name  = "browser",
            input      = {"url": url},
            agent_name = self.agent_name,
            task_id    = job.get("task_id")
        )

    def _extract_url(self, text: str) -> str | None:
        import re
        urls = re.findall(r'https?://[^\s]+', text)
        return urls[0] if urls else None