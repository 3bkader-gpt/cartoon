from __future__ import annotations

from typing import Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.db.models import Episode, Series, SourceEnum
from app.infra.scraping.arabic_toons import ArabicToonsScraper
from app.schemas import ScrapeResult, SeriesBase


class UnsupportedSourceError(ValueError):
    pass


def _detect_source(url: str) -> SourceEnum:
    lowered = url.lower()
    if "arabic" in lowered or "arabict" in lowered or "arabictoons" in lowered:
        return SourceEnum.arabic_toons
    if "egydead" in lowered:
        return SourceEnum.egydead
    return SourceEnum.unknown


async def scrape_series(session: AsyncSession, url: str) -> ScrapeResult:
    source = _detect_source(url)

    if source == SourceEnum.arabic_toons:
        scraper = ArabicToonsScraper()
    else:
        raise UnsupportedSourceError(f"Unsupported source for url: {url}")

    scrape_result: ScrapeResult = await scraper.fetch_series(url)

    # Upsert series
    existing_series = await session.scalar(select(Series).where(Series.url == url))
    if existing_series:
        existing_series.title = scrape_result.series.title
        existing_series.source = source
        series_obj = existing_series
    else:
        series_obj = Series(
            title=scrape_result.series.title,
            url=scrape_result.series.url,
            source=source,
        )
        session.add(series_obj)
        await session.flush()  # to get series id

    # Upsert episodes: avoid duplicates by URL within the series
    existing_eps = await session.scalars(
        select(Episode).where(Episode.series_id == series_obj.id)
    )
    existing_by_url = {ep.url: ep for ep in existing_eps}

    for ep in scrape_result.episodes:
        if ep.url in existing_by_url:
            # Optionally update metadata
            existing = existing_by_url[ep.url]
            existing.title = ep.title
            existing.episode_number = ep.episode_number
        else:
            session.add(
                Episode(
                    series_id=series_obj.id,
                    title=ep.title,
                    episode_number=ep.episode_number,
                    size_hint=None,
                    url=ep.url,
                )
            )

    await session.commit()

    # Rebuild response (ensuring source matches DB value)
    series_schema = SeriesBase(title=series_obj.title, url=series_obj.url, source=series_obj.source)
    return ScrapeResult(series=series_schema, episodes=scrape_result.episodes)
