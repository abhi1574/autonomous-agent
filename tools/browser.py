import re

class BrowserTool:
    name        = "browser"
    description = "Navigate to a URL and extract page content using Playwright"

    def run(self, input: dict) -> str:
        url     = input.get("url", "")
        selector= input.get("selector", "body")

        if not url:
            return "No URL provided"

        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page    = browser.new_page()
                page.goto(url, timeout=30000)

                title   = page.title()
                content = page.inner_text(selector)[:3000]
                browser.close()

            return f"Title: {title}\nURL: {url}\n\nContent:\n{content}"

        except ImportError:
            return "Playwright not installed. Run: playwright install chromium"
        except Exception as e:
            return f"Browser tool failed: {e}"