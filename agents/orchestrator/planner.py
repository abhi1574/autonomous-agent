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
Each subtask must be assigned to one of: research, rag, critic, coding, browser

Task Title: {task_title}
Task Description: {task_description}

Respond ONLY with a valid JSON array. No explanation, no markdown.
Format:
[
  {{
    "subtask_id": "1",
    "title": "short title",
    "description": "what needs to be done",
    "agent": "research|rag|critic|coding|browser",
    "depends_on": []
  }}
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