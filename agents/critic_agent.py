from agents.base_agent import BaseAgent

class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__("critic")

    def execute(self, job: dict) -> str:
        # Generate real embedding for task context
        query_vector = self.router.embed(job.get("title", ""))

        # Search for relevant outputs from other agents
        results = self.vector.search(
            vector=query_vector,
            limit=3,
            filter_by={"task_id": job.get("task_id")}
        )

        if not results:
            return "No output available to critique yet."

        content_to_review = "\n\n".join([
            f"Output {i+1} (by {r['metadata'].get('agent')} agent):\n{r.get('text', '')[:800]}"
            for i, r in enumerate(results)
        ])

        return self.router.run(
            tool_name  = "llm",
            input      = {
                "system": """You are a critical reviewer for an AI agent system.
                Review the provided outputs and:
                1. Identify strengths
                2. Identify weaknesses or gaps
                3. Give an overall quality score (1-10)
                4. Suggest improvements
                Be concise and specific.""",
                "prompt": f"Task: {job.get('title')}\n\nOutputs to review:\n{content_to_review}"
            },
            agent_name = self.agent_name,
            task_id    = job.get("task_id")
        )