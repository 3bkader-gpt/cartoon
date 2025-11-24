"""
EgyDead Scraper
Handles scraping logic for egydead.skin
"""

import re
import logging
import requests
from typing import List, Dict, Generator
from ...core.browser import BrowserManager
from .parser import EgyDeadParser
from .config import BASE_URL, SELECTORS, SEASON_PATTERN, EPISODE_PATTERN

logger = logging.getLogger(__name__)

class EgyDeadScraper:
    """Scraper implementation for EgyDead"""
    
    def __init__(self, browser_manager: BrowserManager = None):
        self.browser_manager = browser_manager or BrowserManager()
        self.parser = EgyDeadParser()

    def get_episode_video_url(self, episode_url: str, include_metadata: bool = False):
        """Extract video URL from episode page"""
        context = self.browser_manager.get_context()
        page = context.new_page()
        
        try:
            page.goto(episode_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)
            
            # Try to find video in iframe
            video_url = page.evaluate("""
                () => {
                    // Try iframe first
                    const iframe = document.querySelector('iframe[src*="embed"]');
                    if (iframe) {
                        return iframe.src;
                    }
                    
                    // Try video element
                    const video = document.querySelector('video');
                    if (video) {
                        return video.currentSrc || video.src;
                    }
                    
                    // Try download links
                    const downloadLink = document.querySelector('a[href*=".mp4"]');
                    if (downloadLink) {
                        return downloadLink.href;
                    }
                    
                    return null;
                }
            """)
            
            # If iframe found, try to extract actual video URL
            if video_url and 'embed' in video_url:
                # For now, return the iframe URL
                # In production, you might need to navigate to it and extract the actual video
                pass
            
            if include_metadata and video_url:
                metadata = self.parser.get_page_metadata(page)
                return {"video_url": video_url, "metadata": metadata}
            
            return video_url
            
        except Exception as e:
            logger.error(f"Error extracting video URL: {e}")
            return None
        finally:
            page.close()

    def get_season_episodes(self, season_url: str) -> List[Dict]:
        """Get all episodes from season page"""
        context = self.browser_manager.get_context()
        page = context.new_page()
        episodes = []
        
        try:
            page.goto(season_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2000)
            
            # Find all episode links
            links = page.locator(SELECTORS["episode_links"])
            count = links.count()
            
            logger.info(f"Found {count} episode links")
            
            for i in range(min(count, 100)):
                try:
                    link = links.nth(i)
                    href = link.get_attribute("href")
                    text = link.inner_text()
                    
                    if href and EPISODE_PATTERN in href:
                        # Make absolute URL
                        full_url = href if href.startswith('http') else f"{BASE_URL}{href}"
                        
                        # Parse episode info
                        info = self.parser.parse_episode_url(full_url)
                        info["title"] = text.strip()
                        
                        episodes.append(info)
                except Exception as e:
                    logger.warning(f"Error processing link {i}: {e}")
                    continue
            
            return episodes
            
        except Exception as e:
            logger.error(f"Error getting episodes: {e}")
            return []
        finally:
            page.close()

    def get_video_metadata(self, video_url: str) -> Dict:
        """Get video file metadata"""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": BASE_URL
            }
            
            response = requests.head(video_url, headers=headers, timeout=10, allow_redirects=True)
            size = int(response.headers.get('Content-Length', 0))
            
            if size:
                gb = size / (1024**3)
                mb = size / (1024**2)
                fmt = f"{gb:.2f} GB" if gb >= 1 else f"{mb:.2f} MB"
                return {"size_bytes": size, "size_formatted": fmt}
            
            return {"size_bytes": 0, "size_formatted": "Unknown"}
        except Exception as e:
            logger.warning(f"Error getting video metadata: {e}")
            return {"size_bytes": 0, "size_formatted": "Unknown"}

    def download_season_generator(self, season_url: str, season_number: int = None) -> Generator:
        """Generator for downloading season episodes"""
        try:
            logger.info(f"Starting download for: {season_url}")
            episodes = self.get_season_episodes(season_url)
            
            total = len(episodes)
            yield {"type": "start", "total": total}
            
            for i, ep in enumerate(episodes, 1):
                title = ep.get('title', 'Unknown')
                yield {"type": "progress", "current": i, "total": total, "title": title}
                
                try:
                    data = self.get_episode_video_url(ep["episode_url"], include_metadata=True)
                    
                    if data:
                        video_url = data["video_url"] if isinstance(data, dict) else data
                        meta = data.get("metadata", {}) if isinstance(data, dict) else {}
                        
                        video_meta = self.get_video_metadata(video_url) if video_url else {}
                        
                        result = {
                            **ep,
                            "video_url": video_url,
                            "video_info": self.parser.parse_video_url(video_url) if video_url else {},
                            "metadata": video_meta,
                            "thumbnail": meta.get("thumbnail", "")
                        }
                        yield {"type": "result", "data": result}
                    else:
                        yield {"type": "error", "episode": title, "message": "No video URL"}
                        
                except Exception as e:
                    logger.error(f"Error processing episode {i}: {e}")
                    yield {"type": "error", "episode": title, "message": str(e)}
                    
        except Exception as e:
            logger.error(f"Error in download_season_generator: {e}")
            yield {"type": "error", "episode": "Season", "message": str(e)}
