from __future__ import annotations

import re
from typing import List

from playwright.async_api import Page

from app.infra.scraping.browser import browser_manager
from app.infra.db.models import SourceEnum
from app.schemas import EpisodeBase, ScrapeResult, SeriesBase


class ArabicToonsScraper:
    """Scraper to extract series metadata and episode list from Arabic Toons."""

    def __init__(self) -> None:
        self.source = SourceEnum.arabic_toons

    async def fetch_series(self, url: str, debug: bool = False) -> ScrapeResult:
        context = await browser_manager.get_new_context()
        page: Page | None = None
        try:
            page = await context.new_page()
            await page.goto(url, wait_until="networkidle", timeout=30_000)

            # Wait for an episode list container; try multiple selectors to be resilient
            selectors = [
                "div.episodes-list a",
                "ul.episodes a",
                "a.episode",
                "a[href*='episode']",
                "a[href*='ep']",
            ]

            episode_elements = []
            for selector in selectors:
                try:
                    await page.wait_for_selector(selector, timeout=5_000)
                    episode_elements = await page.query_selector_all(selector)
                    if episode_elements:
                        if debug:
                            print(f"Selector hit: '{selector}' found {len(episode_elements)} elements")
                        break
                except Exception:
                    continue

            # Series title
            title_text = await page.title()
            series_title = title_text.strip() if title_text else "Arabic Toons Series"

            if debug:
                print(f"Page title: {series_title}")
                print(f"Using selector count: {len(episode_elements)}")

            episodes: List[EpisodeBase] = []
            for el in episode_elements:
                text = (await el.inner_text()) or ""
                href = await el.get_attribute("href")
                if not href:
                    continue

                # Attempt to extract episode number from text
                match = re.search(r"(\d+)", text)
                ep_num = int(match.group(1)) if match else None

                ep_title = text.strip() or f"Episode {ep_num}" if ep_num else "Episode"
                ep_url = href.strip()

                episodes.append(
                    EpisodeBase(
                        title=ep_title,
                        url=ep_url,
                        episode_number=ep_num,
                    )
                )

            series = SeriesBase(title=series_title, url=url, source=self.source)
            return ScrapeResult(series=series, episodes=episodes)

        finally:
            if page is not None:
                await page.close()
            await context.close()
