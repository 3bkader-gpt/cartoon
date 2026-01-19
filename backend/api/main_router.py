from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import logging
import traceback
import sys
import os
import subprocess
from ..scraper.scraper import ArabicToonsScraper
from ..core.browser import BrowserManager
from .. import database as db

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = APIRouter()

# Global scraper instance
_scraper = None

def get_scraper():
    global _scraper
    if _scraper is None:
        print("[INIT] Initializing Arabic Toons Scraper...", flush=True)
        _scraper = ArabicToonsScraper()
        print("[INIT] Scraper initialized successfully", flush=True)
    return _scraper

class URLRequest(BaseModel):
    url: str

@router.get("/season/stream")
def stream_season(url: str, force_refresh: bool = False):
    """
    Stream season episodes from Arabic Toons.
    Uses SQLite cache: if data is fresh (< 24h), serves from DB.
    Otherwise, fetches from web and caches to DB.
    """
    try:
        # Check if cache is fresh and we're not forcing refresh
        if not force_refresh and db.is_cache_fresh(url):
            logger.info(f"Cache HIT for {url} - serving from SQLite")
            cached_episodes = db.get_cached_episodes(url)
            series = db.get_series(url)
            
            def cached_event_generator():
                # Send start event
                yield json.dumps({
                    "type": "start",
                    "total": len(cached_episodes),
                    "series_title": series.get('title', 'Unknown Series'),
                    "cached": True
                }) + "\n"
                
                # Send each episode as result event
                for i, ep in enumerate(cached_episodes, 1):
                    yield json.dumps({
                        "type": "progress",
                        "current": i,
                        "total": len(cached_episodes),
                        "title": ep.get('title', f'Episode {i}')
                    }) + "\n"
                    
                    yield json.dumps({
                        "type": "result",
                        "data": {
                            "title": ep.get('title'),
                            "video_url": ep.get('video_url'),
                            "video_info": ep.get('video_info', {}),
                            "metadata": {"size_bytes": ep.get('size_bytes', 0)},
                            "thumbnail": ep.get('thumbnail'),
                            "episode_url": ep.get('episode_url')
                        }
                    }) + "\n"
            
            return StreamingResponse(cached_event_generator(), media_type="text/event-stream")
        
        # Cache MISS or force refresh - fetch from web
        logger.info(f"Cache MISS for {url} - fetching from web")
        scraper = get_scraper()
        
        def event_generator():
            try:
                event_count = 0
                episode_number = 0
                series_title = "Unknown Series"
                first_thumbnail = None
                
                for event in scraper.download_season_generator(url):
                    event_count += 1
                    
                    # Capture series title from start event AND upsert series FIRST
                    if event.get('type') == 'start':
                        series_title = event.get('series_title', 'Unknown Series')
                        total_episodes = event.get('total', 0)
                        
                        # Upsert series IMMEDIATELY so episodes can reference it
                        db.upsert_series(
                            url=url,
                            title=series_title,
                            thumbnail=None,  # Will update later with first episode thumbnail
                            total_episodes=total_episodes
                        )
                    
                    # Cache each episode result
                    if event.get('type') == 'result':
                        episode_number += 1
                        data = event.get('data', {})
                        
                        # Capture first thumbnail for series
                        if not first_thumbnail and data.get('thumbnail'):
                            first_thumbnail = data.get('thumbnail')
                            # Update series with thumbnail
                            db.upsert_series(
                                url=url,
                                title=series_title,
                                thumbnail=first_thumbnail,
                                total_episodes=total_episodes
                            )
                        
                        # Upsert episode to DB (series now exists!)
                        db.upsert_episode(
                            series_url=url,
                            episode_number=episode_number,
                            title=data.get('title', f'Episode {episode_number}'),
                            video_url=data.get('video_url', ''),
                            video_info=data.get('video_info', {}),
                            size_bytes=data.get('metadata', {}).get('size_bytes', 0),
                            thumbnail=data.get('thumbnail', ''),
                            episode_url=data.get('episode_url', '')
                        )
                    
                    yield json.dumps(event) + "\n"
                
                logger.info(f"Cached {episode_number} episodes for '{series_title}'")
                
                logger.info(f"Stream completed. Total events: {event_count}")
            except Exception as e:
                err_msg = repr(e)
                logger.error(f"Generator error: {err_msg}")
                logger.error(traceback.format_exc())
                yield json.dumps({'type': 'error', 'message': err_msg}) + "\n"
        
        return StreamingResponse(event_generator(), media_type="text/event-stream")
        
    except Exception as e:
        logger.error(f"Stream endpoint error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


import httpx
from fastapi import Request

@router.on_event("shutdown")
def shutdown_event():
    global _scraper
    if _scraper and _scraper.browser_manager:
        print("[SHUTDOWN] Closing browser...", flush=True)
        _scraper.browser_manager.close()

@router.get("/proxy")
async def proxy_download(url: str, filename: str = None):
    """
    Proxy file download to bypass CORS/Referer checks
    """
    if not url:
        raise HTTPException(status_code=400, detail="Missing URL")
        
    async def iterfile():
        async with httpx.AsyncClient(verify=False, follow_redirects=True) as client:
            # Basic headers to look like a browser
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": "https://forafile.com/" # Try generic referer
            }
            try:
                async with client.stream("GET", url, headers=headers) as response:
                    response.raise_for_status()
                    async for chunk in response.aiter_bytes():
                        yield chunk
            except Exception as e:
                print(f"Proxy error: {e}")
                pass

    if not filename:
        filename = url.split('/')[-1]

    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"'
    }
    
    return StreamingResponse(iterfile(), media_type="application/octet-stream", headers=headers)

@router.post("/open-downloads")
def open_downloads_folder():
    """
    Open the system's Downloads folder in the file explorer
    """
    try:
        # Get user's Downloads folder
        if sys.platform == "win32":
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            os.startfile(downloads_path)
        elif sys.platform == "darwin":
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            subprocess.run(["open", downloads_path], check=True)
        else:  # Linux
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            subprocess.run(["xdg-open", downloads_path], check=True)
        
        return {"status": "success", "path": downloads_path}
    except Exception as e:
        logger.error(f"Failed to open downloads folder: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to open folder: {str(e)}")

@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "4.2.0"}
