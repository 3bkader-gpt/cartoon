from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.db.session import get_db
from app.services import scraper as scraper_service
from app.schemas import ScrapeResult

router = APIRouter(prefix="/scrape", tags=["scrape"])


class ScrapeRequest(BaseModel):
    url: HttpUrl


@router.post("", response_model=ScrapeResult, status_code=status.HTTP_200_OK)
async def scrape_endpoint(payload: ScrapeRequest, session: AsyncSession = Depends(get_db)) -> ScrapeResult:
    try:
        result = await scraper_service.scrape_series(session=session, url=str(payload.url))
        return result
    except scraper_service.UnsupportedSourceError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:  # fallback
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Scrape failed") from exc
