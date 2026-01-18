from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.infra.scraping.browser import browser_manager
from app.api.routers import scrape as scrape_router


@asynccontextmanager
def lifespan(app: FastAPI):
    # Startup
    await browser_manager.start()
    try:
        yield
    finally:
        # Shutdown
        await browser_manager.stop()


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        openapi_url=f"{settings.api_prefix}/openapi.json" if settings.enable_docs else None,
        docs_url=f"{settings.api_prefix}/docs" if settings.enable_docs else None,
        redoc_url=f"{settings.api_prefix}/redoc" if settings.enable_docs else None,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(scrape_router.router, prefix=f"{settings.api_prefix}/v1")

    return app


app = create_app()
