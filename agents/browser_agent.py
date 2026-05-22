from agents.base_agent import BaseAgent
import os
from dotenv import load_dotenv

load_dotenv()

class BrowserAgent(BaseAgent):
    def __init__(self):
        super().__init__("browser")

    def execute(self, job: dict) -> str:
        try:
            from playwright.sync_api import sync_playwright

            task = job.get("description") or job.get("title")
            url  = self._extract_url(task)

            if not url:
                return f"No URL found in task: {task}"

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page    = browser.new_page()
                page.goto(url, timeout=30000)

                # Extract page title and text content
                title   = page.title()
                content = page.inner_text("body")[:2000]

                browser.close()

            return f"Page: {title}\nURL: {url}\n\nContent:\n{content}"

        except ImportError:
            return "Playwright not installed. Run: playwright install chromium"
        except Exception as e:
            return f"Browser agent failed: {e}"

    def _extract_url(self, text: str) -> str | None:
        """Extract URL from task description"""
        import re
        urls = re.findall(r'https?://[^\s]+', text)
        return urls[0] if urls else None