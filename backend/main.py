from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import sys
import os
from fastapi.responses import StreamingResponse
import json

# Add parent directory to path to import api module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.arabic_toons_api import ArabicToonsAPI

app = FastAPI(title="Arabic Toons API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoResponse(BaseModel):
    video_url: Optional[str]
    video_info: Optional[Dict]

@app.get("/")
def read_root():
    return {"message": "Arabic Toons API is running"}

@app.get("/api/resolve")
def resolve_url(url: str):
    if "anime-streaming" in url:
        raise HTTPException(status_code=400, detail="This looks like a series URL. Please use the Season Downloader for full series.")
        
    try:
        with ArabicToonsAPI(headless=True) as api:
            result = api.get_episode_video_url(url, include_metadata=True)
            
            if not result:
                raise HTTPException(status_code=404, detail="Could not find video URL. Make sure this is a valid episode page.")
            
            # Handle both return types (str or dict) just in case
            if isinstance(result, str):
                video_url = result
                metadata = {}
            else:
                video_url = result["video_url"]
                metadata = result["metadata"]

            # Parse video info from URL
            video_info = api.parse_video_url(video_url)
            
            # Enhance video info with page metadata
            h1 = metadata.get("h1", "")
            print(f"DEBUG: Raw H1 = '{h1}'")
            
            if h1:
                # Try to extract series name and episode number from H1
                import re
                
                # Try to find episode number
                ep_match = re.search(r'(?:الحلقة|Episode)\s*(\d+)', h1, re.IGNORECASE)
                if ep_match:
                    video_info["episode"] = ep_match.group(1)
                
                # Try to find season number
                season_match = re.search(r'(?:الموسم|Season)\s*(\d+)', h1, re.IGNORECASE)
                if season_match:
                    video_info["season"] = season_match.group(1)
                    
                # Try to clean series name
                # Remove "Episode X", "Season Y", "Watch", "Download" etc.
                clean_name = h1
                clean_name = re.sub(r'(?:الحلقة|Episode)\s*\d+', '', clean_name, flags=re.IGNORECASE)
                clean_name = re.sub(r'(?:الموسم|Season)\s*\d+', '', clean_name, flags=re.IGNORECASE)
                clean_name = re.sub(r'(?:مشاهدة|تحميل|Watch|Download)', '', clean_name, flags=re.IGNORECASE)
                clean_name = re.sub(r'(?:مترجم|مدبلج|اون لاين|Online)', '', clean_name, flags=re.IGNORECASE)
                
                # Remove special chars at ends
                clean_name = clean_name.strip(' -_:.|')
                
                print(f"DEBUG: Cleaned Name = '{clean_name}'")
                
                if clean_name and len(clean_name) > 1:
                    video_info["series_name"] = clean_name
            
            # Generate a nice filename if we have series name and episode
            if "series_name" in video_info and "episode" in video_info:
                safe_name = video_info["series_name"].replace(" ", "_")
                # Remove unsafe chars for filenames
                safe_name = re.sub(r'[\\/*?:"<>|]', '', safe_name)
                video_info["suggested_filename"] = f"{safe_name}_E{video_info['episode']}.mp4"
            else:
                video_info["suggested_filename"] = video_info.get("filename", "episode.mp4")

            return {
                "video_url": video_url,
                "video_info": video_info
            }
    except Exception as e:
        print(f"Error resolving URL: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/series")
def get_series_episodes(url: str):
    try:
        with ArabicToonsAPI(headless=True) as api:
            episodes = api.get_series_episodes(url)
            return episodes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/season")
def download_season(url: str):
    """
    Legacy endpoint - keeps working but blocks until finished
    """
    try:
        with ArabicToonsAPI(headless=True) as api:
            results = api.download_season(url)
            return {
                "success": True,
                "total": len(results),
                "episodes": results
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/season/stream")
async def stream_season(url: str):
    print(f"Received stream request for: {url}")
    def event_generator():
        try:
            with ArabicToonsAPI(headless=True) as api:
                print("API initialized, starting generator...")
                for event in api.download_season_generator(url):
                    print(f"Yielding event: {event['type']}")
                    yield json.dumps(event) + "\n"
        except Exception as e:
            print(f"Stream error: {e}")
            yield json.dumps({"type": "error", "episode": "System", "message": str(e)}) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")

# Placeholder for search - to be implemented
@app.get("/api/search")
def search_cartoons(q: str):
    try:
        with ArabicToonsAPI(headless=True) as api:
            results = api.search(q)
            return {"results": results, "message": f"Found {len(results)} results"}
    except Exception as e:
        print(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/proxy")
async def proxy_video(url: str, filename: Optional[str] = None):
    """
    Proxy video download to bypass 403 Forbidden checks (Referer/User-Agent)
    """
    import requests
    from fastapi.responses import StreamingResponse
    from urllib.parse import urlparse
    import os
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.arabic-toons.com/",
    }
    
    try:
        # Determine filename
        if not filename:
            # Extract filename from URL if not provided
            parsed_url = urlparse(url)
            path = parsed_url.path
            filename = os.path.basename(path)
            
            # Fallback if filename is empty or weird
            if not filename or '.' not in filename:
                filename = "episode.mp4"
        
        # Ensure .mp4 extension
        if not filename.endswith('.mp4'):
            filename += '.mp4'

        # Stream the content to avoid loading large files into memory
        r = requests.get(url, headers=headers, stream=True)
        r.raise_for_status()
        
        return StreamingResponse(
            r.iter_content(chunk_size=8192),
            media_type=r.headers.get("content-type", "video/mp4"),
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
    except Exception as e:
        print(f"Proxy error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
