from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from app.infra.db.models import SourceEnum


class EpisodeBase(BaseModel):
    title: str = Field(...)
    url: str = Field(...)
    episode_number: int | None = Field(default=None)

    model_config = {
        "from_attributes": True,
    }


class SeriesBase(BaseModel):
    title: str = Field(...)
    url: str = Field(...)
    source: SourceEnum = Field(...)

    model_config = {
        "from_attributes": True,
    }


class ScrapeResult(BaseModel):
    series: SeriesBase
    episodes: List[EpisodeBase]

    model_config = {
        "from_attributes": True,
    }
