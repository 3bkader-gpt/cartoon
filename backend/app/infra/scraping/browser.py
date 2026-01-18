from __future__ import annotations

import asyncio
from typing import Optional

from playwright.async_api import Browser, BrowserContext, Playwright, async_playwright

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/123.0.0.0 Safari/537.36"
)
DEFAULT_VIEWPORT = {"width": 1366, "height": 768}


class BrowserManager:
    """Singleton-like manager for Playwright browser lifecycle."""

    def __init__(self) -> None:
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._lock = asyncio.Lock()

    async def start(self, headless: bool = True) -> None:
        async with self._lock:
            if self._browser is not None:
                return
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(headless=headless)

    async def stop(self) -> None:
        async with self._lock:
            if self._browser is not None:
                await self._browser.close()
                self._browser = None
            if self._playwright is not None:
                await self._playwright.stop()
                self._playwright = None

    async def get_new_context(self) -> BrowserContext:
        if self._browser is None:
            raise RuntimeError("Browser not started. Call start() first.")

        context = await self._browser.new_context(
            viewport=DEFAULT_VIEWPORT,
            user_agent=DEFAULT_USER_AGENT,
            java_script_enabled=True,
        )
        return context


browser_manager = BrowserManager()
