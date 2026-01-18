"""
Base Extractor Class
Abstract base class providing common functionality for all server extractors
"""

import re
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union
from playwright.sync_api import BrowserContext, Page
from dataclasses import dataclass, asdict

from .common.ad_blocker import setup_ad_blocking
from .common.popup_handler import setup_popup_handler

logger = logging.getLogger(__name__)

@dataclass
class ExtractionResult:
    """
    Standardized result from an extractor
    """
    video_url: str
    quality: str = "Auto"
    server: str = "Unknown"
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        if result['metadata'] is None:
            result['metadata'] = {}
        return result

class BaseExtractor(ABC):
    """
    Abstract base class for server extractors
    
    Provides common functionality:
    - Ad blocking
    - Popup handling
    - Video URL extraction
    - Timer waiting
    """
    
    def __init__(self, browser_context: BrowserContext):
        """
        Initialize extractor with browser context
        
        Args:
            browser_context: Playwright BrowserContext for creating pages
        """
        self.context = browser_context
        # Setup popup handler at context level (once per context)
        setup_popup_handler(browser_context)
    
    @abstractmethod
    def extract(self, url: str, page: Optional[Page] = None) -> Union[ExtractionResult, List[ExtractionResult], None]:
        """
        Extract direct video link(s) from server URL
        
        Args:
            url: Server URL to extract from
            page: Optional existing Playwright Page to use (prevents opening new tab)
            
        Returns:
            Single ExtractionResult, List of ExtractionResult, or None
        """
        pass
    
    def setup_page(self, page: Page):
        """
        Configure page with ad blocking and popup handling
        
        Args:
            page: Playwright Page object to configure
        """
        try:
            setup_ad_blocking(page)
        except Exception as e:
            logger.warning(f"Failed to setup page (may be closed): {e}")
    
    def extract_video_url(self, page: Page) -> Optional[str]:
        """
        Common video extraction logic
        Checks for video tags, iframes, m3u8 links, etc.
        
        Args:
            page: Playwright Page object
            
        Returns:
            Video URL string or None if not found
        """
        # 1. Check for video tag
        video_url = page.evaluate("""
            () => {
                const video = document.querySelector('video');
                if (video) {
                    if (video.src) return video.src;
                    if (video.currentSrc) return video.currentSrc;
                    const source = video.querySelector('source');
                    if (source) return source.src;
                }
                
                const source = document.querySelector('source[src*=".mp4"]');
                if (source) return source.src;
                
                const link = document.querySelector('a[href*=".mp4"]');
                if (link && link.href.endsWith('.mp4')) return link.href;
                
                return null;
            }
        """)
        
        if video_url:
            return video_url
        
        # 2. Check for iframe (but exclude known ad iframes)
        iframe = page.locator('iframe').first
        if iframe.count() > 0:
            src = iframe.get_attribute("src")
            if src and not any(ad in src.lower() for ad in ["google", "facebook", "doubleclick"]):
                return src
        
        # 3. Check for m3u8 in page content
        try:
            content = page.content()
            m3u8_matches = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', content)
            if m3u8_matches:
                return m3u8_matches[0]
        except Exception as e:
            logger.warning(f"Error checking for m3u8: {e}")
        
        return None
    
    def wait_for_timer(self, page: Page, timer_locator: str, max_wait: int = 30) -> bool:
        """
        Wait for countdown timer to finish
        
        Args:
            page: Playwright Page object
            timer_locator: CSS selector for timer element
            max_wait: Maximum seconds to wait
            
        Returns:
            True if timer completed, False if timeout
        """
        try:
            timer = page.locator(timer_locator)
            if timer.count() == 0:
                return True  # No timer found, assume ready
            
            # Wait for timer to disappear or reach 0
            timer.wait_for(state="hidden", timeout=max_wait * 1000)
            return True
        except Exception as e:
            logger.warning(f"Timer wait failed: {e}")
            return False
    
    def remove_overlays(self, page: Page, overlay_selectors: Optional[List[str]] = None):
        """
        Remove overlay divs that block clicks
        
        Args:
            page: Playwright Page object
            overlay_selectors: List of CSS selectors for overlays to remove
        """
        if overlay_selectors is None:
            overlay_selectors = [
                '[class*="overlay"]',
                '[id*="overlay"]',
                '[class*="popup"]',
                '[id*="popup"]',
            ]
        
        try:
            page.evaluate(f"""
                () => {{
                    const selectors = {overlay_selectors};
                    selectors.forEach(selector => {{
                        const elements = document.querySelectorAll(selector);
                        elements.forEach(el => {{
                            if (el.style.position === 'fixed' || el.style.position === 'absolute') {{
                                el.remove();
                            }}
                        }});
                    }});
                }}
            """)
        except Exception as e:
            logger.warning(f"Error removing overlays: {e}")

