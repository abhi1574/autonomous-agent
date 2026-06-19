import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

class WebSearchTool:
    name        = "web_search"
    description = "Search the web using Tavily and return summarised results"

    def __init__(self):
        pass  # don't import at init time

    def run(self, input: dict) -> str:
        try:
            from tavily import TavilyClient  # ← lazy import here
            import os
            client  = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
            query   = input.get("query", "")
            results = client.search(
                query       = query,
                max_results = input.get("max_results", 5),
                search_depth= "advanced"
            )
            summary = f"Search Results for: {query}\n\n"
            for i, r in enumerate(results.get("results", []), 1):
                summary += f"{i}. {r.get('title')}\n"
                summary += f"   URL: {r.get('url')}\n"
                summary += f"   {r.get('content', '')[:300]}\n\n"
            return summary
        except ImportError:
            return "❌ Tavily not installed. Run: uv add tavily-python"
        except Exception as e:
            return f"❌ Web search failed: {e}"