from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import logging
import traceback
import sys
from ..core.selector import ScraperSelector

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = APIRouter()

# Create selector lazily to avoid import-time issues
_selector = None

def get_selector():
    global _selector
    if _selector is None:
        print("[INIT] Creating ScraperSelector...", flush=True)
        _selector = ScraperSelector()
        print("[INIT] ScraperSelector created", flush=True)
    return _selector

class URLRequest(BaseModel):
    url: str

@router.get("/season/stream")
def stream_season(url: str):  # Changed to sync function
    """Stream season episodes - using sync to work with Playwright"""
    with open("backend_debug.log", "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"🎬 stream_season called with URL: {url}\n")
    
    try:
        with open("backend_debug.log", "a", encoding="utf-8") as f:
            f.write("[1] Getting selector...\n")
        selector = get_selector()
        
        with open("backend_debug.log", "a", encoding="utf-8") as f:
            f.write(f"[2] Selector: {selector}\n")
            f.write("[3] Getting scraper...\n")
        
        scraper = selector.get_scraper(url)
        
        with open("backend_debug.log", "a", encoding="utf-8") as f:
            f.write(f"[4] Scraper: {type(scraper).__name__}\n")
        
        def event_generator():
            try:
                with open("backend_debug.log", "a", encoding="utf-8") as f:
                    f.write("[5] Starting generator...\n")
                    f.write("[6] Calling download_season_generator...\n")
                
                event_count = 0
                for event in scraper.download_season_generator(url):
                    event_count += 1
                    event_type = event.get('type', 'unknown')
                    with open("backend_debug.log", "a", encoding="utf-8") as f:
                        f.write(f"[7] Event #{event_count}: {event_type}\n")
                    yield json.dumps(event) + "\n"
                
                with open("backend_debug.log", "a", encoding="utf-8") as f:
                    f.write(f"[8] Generator done. Total: {event_count}\n")
            except Exception as e:
                err_msg = repr(e)
                with open("backend_debug.log", "a", encoding="utf-8") as f:
                    f.write(f"[ERROR] Generator exception: {err_msg}\n")
                    f.write(traceback.format_exc() + "\n")
                yield json.dumps({'type': 'error', 'message': err_msg}) + "\n"
        
        with open("backend_debug.log", "a", encoding="utf-8") as f:
            f.write("[9] Returning StreamingResponse\n")
        return StreamingResponse(event_generator(), media_type="text/event-stream")
        
    except ValueError as e:
        err_msg = repr(e)
        with open("backend_debug.log", "a", encoding="utf-8") as f:
            f.write(f"[ERROR] ValueError: {err_msg}\n")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        err_msg = repr(e)
        with open("backend_debug.log", "a", encoding="utf-8") as f:
            f.write(f"[ERROR] Exception: {err_msg}\n")
            f.write(traceback.format_exc() + "\n")
        raise HTTPException(status_code=500, detail=str(e))


import httpx
from fastapi import Request

@router.on_event("shutdown")
def shutdown_event():
    global _selector
    if _selector:
        _selector.close()

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
                # We can't really return an error HTTP response once streaming starts
                pass

    # Determine filename
    if not filename:
        filename = url.split('/')[-1]

    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"'
    }
    
    return StreamingResponse(iterfile(), media_type="application/octet-stream", headers=headers)
