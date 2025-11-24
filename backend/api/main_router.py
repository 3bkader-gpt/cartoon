from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
from ..core.selector import ScraperSelector

router = APIRouter()
selector = ScraperSelector()

class URLRequest(BaseModel):
    url: str

@router.get("/season/stream")
async def stream_season(url: str):
    try:
        scraper = selector.get_scraper(url)
        
        def event_generator():
            try:
                for event in scraper.download_season_generator(url):
                    yield json.dumps(event) + "\n"
            except Exception as e:
                yield json.dumps({'type': 'error', 'message': str(e)}) + "\n"
                
        return StreamingResponse(event_generator(), media_type="text/event-stream")
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.on_event("shutdown")
def shutdown_event():
    selector.close()
