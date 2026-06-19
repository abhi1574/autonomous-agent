import os
import json
from groq import Groq
from dotenv import load_dotenv
from backend.logger import get_logger

load_dotenv()

class Planner:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model  = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.logger = get_logger("orchestrator.planner")

    def plan(self, task_title: str, task_description: str) -> list[dict]:
        prompt = f"""You are an AI task planner for an autonomous agent system.
        Break down this task into clear, actionable subtasks.

        STRICT RULES:
        - Maximum 4 subtasks
        - Use ONLY: research, rag, critic
        - NEVER use browser unless task has a URL starting with http or https
        - NEVER use coding unless task explicitly asks to write code
        - ALL depends_on must be EMPTY [] — never add dependencies
        - subtask_id must be: "1", "2", "3", "4"
        - Order subtasks so research runs first, critic runs last

        Task Title: {task_title}
        Task Description: {task_description}

        Respond ONLY with valid JSON array. No markdown, no explanation.
        [
        {{"subtask_id": "1", "title": "Search web", "description": "Search for {task_title}", "agent": "research", "depends_on": []}},
        {{"subtask_id": "2", "title": "Search knowledge base", "description": "Search stored knowledge", "agent": "rag", "depends_on": []}},
        {{"subtask_id": "3", "title": "Critique and summarise", "description": "Review all findings and provide detailed summary", "agent": "critic", "depends_on": []}}
        ]"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            raw = response.choices[0].message.content.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            subtasks = json.loads(raw.strip())
            self.logger.info(f"Planned {len(subtasks)} subtasks for: {task_title}")
            return subtasks
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON parse failed: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Planner failed: {e}")
            return []