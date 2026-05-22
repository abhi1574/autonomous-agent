import os
import json
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

class Planner:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model  = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    def plan(self, task_title: str, task_description: str) -> list[dict]:
        """Break a task into subtasks using Groq"""

        prompt = f"""You are an AI task planner for an autonomous agent system.

            Your job is to break down a high-level task into clear, actionable subtasks.
            Each subtask must be assigned to one of these agents:
            - research   : search the web, find information, summarise findings
            - rag        : search internal knowledge base, retrieve stored documents
            - critic     : review and evaluate output from other agents
            - coding     : write, debug, or explain code
            - browser    : navigate websites, fill forms, extract data

            Task Title: {task_title}
            Task Description: {task_description}

            Respond ONLY with a valid JSON array. No explanation, no markdown, no preamble.
            Format:
            [
            {{
                "subtask_id": "1",
                "title": "short title",
                "description": "what needs to be done",
                "agent": "research|rag|critic|coding|browser",
                "depends_on": []
            }}
            ]

            Rules:
            - depends_on contains subtask_ids that must complete before this one starts
            - Keep subtasks focused and atomic
            - Use as many subtasks as the task genuinely needs
            """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )

            raw = response.choices[0].message.content.strip()

            # Strip markdown fences if model adds them
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]

            subtasks = json.loads(raw.strip())
            print(f"✅ Planner created {len(subtasks)} subtasks")
            return subtasks

        except json.JSONDecodeError as e:
            print(f"❌ Planner JSON parse failed: {e}")
            return []
        except Exception as e:
            print(f"❌ Planner failed: {e}")
            return []