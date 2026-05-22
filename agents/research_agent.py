from tavily import TavilyClient
from agents.base_agent import BaseAgent
import os
from dotenv import load_dotenv

load_dotenv()

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__("research")
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def execute(self, job: dict) -> str:
        query   = job.get("description") or job.get("title")
        results = self.client.search(
            query=query,
            max_results=5,
            search_depth="advanced"
        )

        # Format results into readable summary
        summary = f"Research Results for: {query}\n\n"
        for i, result in enumerate(results.get("results", []), 1):
            summary += f"{i}. {result.get('title')}\n"
            summary += f"   URL: {result.get('url')}\n"
            summary += f"   {result.get('content', '')[:300]}\n\n"

        return summary