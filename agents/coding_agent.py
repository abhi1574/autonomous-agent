from agents.base_agent import BaseAgent

class CodingAgent(BaseAgent):
    def __init__(self):
        super().__init__("coding")

    def execute(self, job: dict) -> str:
        task = job.get("description") or job.get("title")

        # Generate code
        code_response = self.router.run(
            tool_name  = "llm",
            input      = {
                "system": "You are an expert software engineer. Return ONLY raw Python code with no markdown, no fences, no explanation.",
                "prompt": task
            },
            agent_name = self.agent_name,
            task_id    = job.get("task_id")
        )

        # Strip markdown fences if model adds them anyway
        clean_code = code_response
        if "```python" in clean_code:
            clean_code = clean_code.split("```python")[1].split("```")[0].strip()
        elif "```" in clean_code:
            clean_code = clean_code.split("```")[1].split("```")[0].strip()

        # Execute clean code
        execution_result = self.router.run(
            tool_name  = "code_executor",
            input      = {"code": clean_code},
            agent_name = self.agent_name,
            task_id    = job.get("task_id")
        )

        return f"Generated Code:\n{clean_code}\n\nExecution Result:\n{execution_result}"