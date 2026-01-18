from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import backend.database as db

router = APIRouter(prefix="/api/library", tags=["library"])

class FavoriteRequest(BaseModel):
    title: str
    url: str
    thumbnail: Optional[str] = None

class FavoriteResponse(BaseModel):
    id: int
    title: str
    url: str
    thumbnail: Optional[str]
    created_at: str

@router.get("/", response_model=List[FavoriteResponse])
def get_library():
    """Get all favorite shows"""
    return db.get_favorites()

@router.post("/", response_model=FavoriteResponse)
def add_to_library(fav: FavoriteRequest):
    """Add a show to favorites"""
    result = db.add_favorite(fav.title, fav.url, fav.thumbnail)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to add favorite")
    return result

@router.delete("/")
def remove_from_library(url: str):
    """Remove a request from favorites"""
    success = db.remove_favorite(url)
    if not success:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return {"status": "success", "message": "Removed from library"}
