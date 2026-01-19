from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import backend.database as db

router = APIRouter(prefix="/api/library", tags=["library"])

class ToggleFavoriteRequest(BaseModel):
    url: str
    title: Optional[str] = None
    thumbnail: Optional[str] = None

class SeriesResponse(BaseModel):
    url: str
    title: str
    thumbnail: Optional[str]
    total_episodes: int
    is_favorite: bool

@router.get("/", response_model=List[SeriesResponse])
def get_library():
    """Get all favorite series from the unified series table"""
    return db.get_favorite_series()

@router.post("/toggle")
def toggle_favorite(req: ToggleFavoriteRequest):
    """Toggle favorite status for a series"""
    result = db.toggle_favorite(req.url, req.title, req.thumbnail)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to toggle favorite")
    return result

@router.get("/check")
def check_favorite(url: str):
    """Check if a URL is marked as favorite"""
    return {"is_favorite": db.is_favorite(url)}

# Legacy endpoints for backward compatibility
@router.post("/")
def add_to_library_legacy(req: ToggleFavoriteRequest):
    """Legacy: Add a show to favorites (calls toggle)"""
    # If already favorite, don't toggle off
    if db.is_favorite(req.url):
        series = db.get_series(req.url)
        return series
    return db.toggle_favorite(req.url, req.title, req.thumbnail)

@router.delete("/")
def remove_from_library(url: str):
    """Remove a series from favorites"""
    existing = db.get_series(url)
    if existing and existing.get('is_favorite'):
        db.toggle_favorite(url)
        return {"status": "success", "message": "Removed from library"}
    raise HTTPException(status_code=404, detail="Favorite not found")

