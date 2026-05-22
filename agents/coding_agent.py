from agents.base_agent import BaseAgent
from groq import Groq
import os
import subprocess
import tempfile
from dotenv import load_dotenv

load_dotenv()

class CodingAgent(BaseAgent):
    def __init__(self):
        super().__init__("coding")
        self.groq  = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    def execute(self, job: dict) -> str:
        task = job.get("description") or job.get("title")

        # Generate code via Groq
        response = self.groq.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert software engineer.
Write clean, well commented code.
Always include:
- Brief explanation of what the code does
- The code itself
- Example usage"""
                },
                {
                    "role": "user",
                    "content": task
                }
            ],
            temperature=0.2,
        )

        result = response.choices[0].message.content

        # Try to execute if it's Python code
        if "```python" in result:
            try:
                code_block = result.split("```python")[1].split("```")[0].strip()
                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".py", delete=False
                ) as f:
                    f.write(code_block)
                    temp_path = f.name

                execution = subprocess.run(
                    ["python", temp_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if execution.stdout:
                    result += f"\n\n**Execution Output:**\n{execution.stdout}"
                if execution.stderr:
                    result += f"\n\n**Execution Errors:**\n{execution.stderr}"

                os.unlink(temp_path)
            except subprocess.TimeoutExpired:
                result += "\n\n**Execution timed out after 10 seconds**"
            except Exception as e:
                result += f"\n\n**Execution skipped:** {e}"

        return result