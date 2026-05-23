import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMTool:
    name        = "llm"
    description = "Send a prompt to Groq LLM and get a response"

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model  = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    def run(self, input: dict) -> str:
        prompt      = input.get("prompt", "")
        system      = input.get("system", "You are a helpful assistant.")
        temperature = input.get("temperature", 0.3)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt}
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content