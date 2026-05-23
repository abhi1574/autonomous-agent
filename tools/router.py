import time
from tools.llm import LLMTool
from tools.web_search import WebSearchTool
from tools.code_executor import CodeExecutorTool
from tools.browser import BrowserTool
from tools.vector_search import VectorSearchTool
from tools.embeddings import EmbeddingTool
from backend.models.database import SessionLocal
from backend.models.task import ToolLog

# Singleton — loads once, shared across all agents
_router_instance = None

def get_router():
    global _router_instance
    if _router_instance is None:
        _router_instance = ToolRouter()
    return _router_instance

class ToolRouter:
    def __init__(self):
        self._embedder = EmbeddingTool()  # loads model once
        self._tools = {
            "llm"          : LLMTool(),
            "web_search"   : WebSearchTool(),
            "code_executor": CodeExecutorTool(),
            "browser"      : BrowserTool(),
            "vector_search": VectorSearchTool(),
        }

    def embed(self, text: str) -> list[float]:
        return self._embedder.embed(text)

    def list_tools(self) -> list[dict]:
        return [
            {"name": t.name, "description": t.description}
            for t in self._tools.values()
        ]

    def run(
        self,
        tool_name : str,
        input     : dict,
        agent_name: str = "unknown",
        task_id   : str = None
    ) -> str:
        if tool_name not in self._tools:
            return f"❌ Unknown tool: {tool_name}. Available: {list(self._tools.keys())}"

        tool       = self._tools[tool_name]
        start_time = time.time()
        status     = "success"
        output     = ""

        try:
            output = tool.run(input)
        except Exception as e:
            output = f"Tool error: {e}"
            status = "failed"
        finally:
            duration_ms = int((time.time() - start_time) * 1000)
            self._log(
                tool_name  = tool_name,
                agent_name = agent_name,
                task_id    = task_id,
                input      = str(input),
                output     = output[:1000],
                status     = status,
                duration_ms= duration_ms
            )

        return output

    def _log(self, **kwargs):
        db = SessionLocal()
        try:
            log = ToolLog(**kwargs)
            db.add(log)
            db.commit()
            print(f"📝 Tool log: {kwargs['tool_name']} by {kwargs['agent_name']} — {kwargs['duration_ms']}ms [{kwargs['status']}]")
        except Exception as e:
            print(f"❌ Tool log failed: {e}")
            db.rollback()
        finally:
            db.close()