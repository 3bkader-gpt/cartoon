from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import logging
import traceback
import sys
from ..scraper.scraper import ArabicToonsScraper
from ..core.browser import BrowserManager

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
        # BrowserManager will be created inside if not passed, but we pass None to let it handle it
        # or we can create it here if we want more control. 
        # Scraper __init__ handles BrowserManager() creation if None.
        _scraper = ArabicToonsScraper()
        print("[INIT] Scraper initialized successfully", flush=True)
    return _scraper

class URLRequest(BaseModel):
    url: str

@router.get("/season/stream")
def stream_season(url: str):
    """Stream season episodes from Arabic Toons"""
    # Log simplified for production/cleanliness, but keeping debug file for safely
    try:
        scraper = get_scraper()
        
        def event_generator():
            try:
                event_count = 0
                for event in scraper.download_season_generator(url):
                    event_count += 1
                    yield json.dumps(event) + "\n"
                
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
