import time
from agents.base_agent import BaseAgent

class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__("critic")

    def execute(self, job: dict) -> str:
        query_vector = self.router.embed(job.get("title", ""))
        task_id      = job.get("task_id")

        # Wait for research + rag agents to store results
        results  = []
        attempts = 0
        while not results and attempts < 15:
            results = self.vector.search(
                vector   = query_vector,
                limit    = 10,
                filter_by= {"task_id": task_id}
            )
            if not results:
                self.logger.info(f"Critic waiting for agent results — attempt {attempts+1}/15")
                time.sleep(4)
                attempts += 1

        if not results:
            results = self.vector.search(vector=query_vector, limit=5)

        if not results:
            return "No agent outputs found to synthesise."

        # Combine all raw content
        raw_content = "\n\n".join([
            r.get('text', '')[:1000]
            for r in results
        ])

        return self.router.run(
            tool_name  = "llm",
            input      = {
                "system": """You are an expert analyst. Transform raw research data into a clean, professional report.

Structure your response EXACTLY like this:

## Executive Summary
2-3 sentences covering the main answer to the user's question.

## Key Findings
- Finding 1 with specific detail
- Finding 2 with specific detail
- Finding 3 with specific detail
- Finding 4 with specific detail
- Finding 5 with specific detail

## Detailed Analysis
3-4 paragraphs with in-depth analysis of the most important aspects.

## Latest Trends & Updates
Bullet points of the most recent developments.

## Recommendations
3-5 actionable recommendations based on the research.

## Quality Score
X/10 — brief reason

Write in a professional, clear tone. Be specific and insightful. Never mention memory numbers, sources, or raw data artifacts.""",

                "prompt": f"""User asked about: {job.get('title')}

Raw research data gathered by agents:
{raw_content}

Transform this into a comprehensive, user-friendly report following the structure above."""
            },
            agent_name = self.agent_name,
            task_id    = task_id
        )