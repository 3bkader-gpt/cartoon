from __future__ import annotations

import asyncio
import sys
from sqlalchemy import text

from app.infra.scraping.browser import browser_manager
from app.infra.scraping.arabic_toons import ArabicToonsScraper
from app.infra.db.session import AsyncSessionLocal

TEST_URL = "https://www.arabic-toons.com/the-flintstones-1740913500-anime-streaming.html"


async def main() -> None:
    scraper = ArabicToonsScraper()

    try:
        await browser_manager.start(headless=True)

        # Lightweight DB connectivity check
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))

        print(f"Fetching: {TEST_URL}")
        result = await scraper.fetch_series(TEST_URL, debug=True)
        print(f"Scraper Success! Found {len(result.episodes)} episodes.")

        # Log a few episode entries for debugging
        for idx, ep in enumerate(result.episodes[:10], start=1):
            print(f"  #{idx}: title='{ep.title}' url='{ep.url}' num={ep.episode_number}")

        if not result.episodes:
            print("No episodes detected. Possible selector mismatch or dynamic loading issue.")
    except Exception as exc:  # pragma: no cover - diagnostic script
        print("Scraper failed.")
        print(repr(exc))
        raise
    finally:
        await browser_manager.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted.")
        sys.exit(1)
