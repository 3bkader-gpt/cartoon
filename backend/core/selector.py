from typing import Optional
from ..sites.arabic_toons.scraper import ArabicToonsScraper
from ..sites.arabic_toons.config import SUPPORTED_PATTERNS as ARABIC_TOONS_PATTERNS
from ..sites.egydead.scraper import EgyDeadScraper
from ..sites.egydead.config import SUPPORTED_PATTERNS as EGYDEAD_PATTERNS
from .browser import BrowserManager

class ScraperSelector:
    """Selects the appropriate scraper based on URL"""
    
    def __init__(self):
        self.browser_manager = BrowserManager()

    def get_scraper(self, url: str):
        """Return scraper instance for the given URL"""
        
        # Check Arabic Toons
        if any(pattern in url for pattern in ARABIC_TOONS_PATTERNS):
            return ArabicToonsScraper(self.browser_manager)
        
        # Check EgyDead
        if any(pattern in url for pattern in EGYDEAD_PATTERNS):
            return EgyDeadScraper(self.browser_manager)
            
        raise ValueError(f"No scraper found for URL: {url}")

    def close(self):
        self.browser_manager.close()
