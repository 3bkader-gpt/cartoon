from typing import Optional
from ..sites.arabic_toons.scraper import ArabicToonsScraper
from ..sites.arabic_toons.config import SUPPORTED_PATTERNS as ARABIC_TOONS_PATTERNS
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
            
        # Future sites go here...
        # if any(pattern in url for pattern in SITE2_PATTERNS):
        #     return Site2Scraper(self.browser_manager)
            
        raise ValueError(f"No scraper found for URL: {url}")

    def close(self):
        self.browser_manager.close()
