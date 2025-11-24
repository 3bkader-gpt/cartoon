from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from typing import Optional

class BrowserManager:
    """
    Manages Playwright browser instance and contexts.
    Singleton-like behavior to reuse browser across requests if needed.
    """
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None

    def start(self):
        """Start Playwright and launch browser"""
        if not self.playwright:
            self.playwright = sync_playwright().start()
        
        if not self.browser:
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )

    def get_context(self) -> BrowserContext:
        """Get a new or existing browser context"""
        if not self.browser:
            self.start()
        
        # Create new context for isolation (or reuse if strategy changes)
        return self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

    def close(self):
        """Close browser and stop Playwright"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        
        self.context = None
        self.browser = None
        self.playwright = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
