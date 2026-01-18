"""
Generic Extractor
Fallback extractor for unknown server URLs
Uses common patterns to extract video links
"""

import logging
from typing import Dict, Any
from playwright.sync_api import Page

from .base import BaseExtractor

logger = logging.getLogger(__name__)

class GenericExtractor(BaseExtractor):
    """
    Generic extractor for unknown servers
    
    Uses common patterns:
    - Video tags
    - Iframes
    - M3U8 links
    - Direct MP4 links
    """
    
    def extract(self, url: str) -> Dict[str, Any]:
        """
        Extract video URL using generic patterns
        
        Args:
            url: Server URL
            
        Returns:
            Dict with video_url, quality, server, and metadata
        """
        page = self.context.new_page()
        
        try:
            logger.info(f"Extracting from unknown server: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            self.setup_page(page)
            
            # Wait a bit for dynamic content
            page.wait_for_timeout(2000)
            
            # Try to extract video URL using common patterns
            video_url = self.extract_video_url(page)
            
            if not video_url:
                logger.warning(f"Could not extract video URL from {url}")
                return {
                    "video_url": None,
                    "quality": "Unknown",
                    "server": "Generic",
                    "metadata": {}
                }
            
            logger.info(f"Successfully extracted video URL using generic patterns")
            return {
                "video_url": video_url,
                "quality": "Auto",
                "server": "Generic",
                "metadata": {}
            }
            
        except Exception as e:
            logger.error(f"Error extracting from {url}: {e}")
            return {
                "video_url": None,
                "quality": "Unknown",
                "server": "Generic",
                "metadata": {"error": str(e)}
            }
        finally:
            page.close()

