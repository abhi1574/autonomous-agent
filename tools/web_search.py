import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

class WebSearchTool:
    name        = "web_search"
    description = "Search the web using Tavily and return summarised results"

    def __init__(self):
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def run(self, input: dict) -> str:
        query       = input.get("query", "")
        max_results = input.get("max_results", 5)

        results = self.client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced"
        )

        summary = f"Search Results for: {query}\n\n"
        for i, r in enumerate(results.get("results", []), 1):
            summary += f"{i}. {r.get('title')}\n"
            summary += f"   URL: {r.get('url')}\n"
            summary += f"   {r.get('content', '')[:300]}\n\n"

        return summary