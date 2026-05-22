from agents.base_agent import BaseAgent
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__("critic")
        self.groq  = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    def execute(self, job: dict) -> str:
        # Fetch recent results from memory to critique
        results = self.vector.search(
            vector=[0.0] * 384,
            limit=3,
            filter_by={"task_id": job.get("task_id")}
        )

        if not results:
            return "No output available to critique yet."

        content_to_review = "\n\n".join([
            f"Output {i+1} (by {r['metadata'].get('agent')} agent):\n{r.get('text', '')[:800]}"
            for i, r in enumerate(results)
        ])

        response = self.groq.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """You are a critical reviewer for an AI agent system.
Review the provided outputs and:
1. Identify strengths
2. Identify weaknesses or gaps
3. Give an overall quality score (1-10)
4. Suggest improvements
Be concise and specific."""
                },
                {
                    "role": "user",
                    "content": f"Task: {job.get('title')}\n\nOutputs to review:\n{content_to_review}"
                }
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content