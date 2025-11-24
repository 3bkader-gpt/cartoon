"""
EgyDead Scraper with Scrapling (Alternative Implementation)
This is an experimental version using Scrapling instead of Playwright
"""

import logging
from typing import List, Dict, Generator
from scrapling.fetchers import StealthyFetcher, StealthySession
from .parser import EgyDeadParser
from .config import BASE_URL, SELECTORS, SEASON_PATTERN, EPISODE_PATTERN

logger = logging.getLogger(__name__)

class EgyDeadScraplerScraper:
    """
    Alternative EgyDead scraper using Scrapling for better anti-bot bypass
    
    Benefits:
    - Automatic Cloudflare bypass
    - Better fingerprint spoofing
    - Adaptive element finding
    - Faster parsing
    """
    
    def __init__(self):
        self.parser = EgyDeadParser()

    def get_episode_video_url(self, episode_url: str, include_metadata: bool = False):
        """Extract video URL from episode page using Scrapling"""
        try:
            # Fetch with stealth mode and Cloudflare solving
            page = StealthyFetcher.fetch(
                episode_url,
                headless=True,
                solve_cloudflare=True,
                network_idle=True,
                google_search=False
            )
            
            # Try to find video in iframe (Scrapling's CSS selector syntax)
            video_url = page.css_first('iframe[src*="embed"]::attr(src)')
            
            if not video_url:
                # Try video element
                video_url = page.css_first('video::attr(src)')
            
            if not video_url:
                # Try download links
                video_url = page.css_first('a[href*=".mp4"]::attr(href)')
            
            if include_metadata and video_url:
                # Extract metadata using Scrapling's text methods
                title = page.css_first('h1, .entry-title::text')
                thumbnail = page.css_first('meta[property="og:image"]::attr(content)')
                
                return {
                    "video_url": video_url,
                    "metadata": {
                        "title": title,
                        "thumbnail": thumbnail
                    }
                }
            
            return video_url
            
        except Exception as e:
            logger.error(f"Error extracting video URL with Scrapling: {e}")
            return None

    def get_season_episodes(self, season_url: str) -> List[Dict]:
        """Get all episodes from season page using Scrapling"""
        episodes = []
        
        try:
            page = StealthyFetcher.fetch(
                season_url,
                headless=True,
                solve_cloudflare=True,
                network_idle=True
            )
            
            # Find all episode links using Scrapling
            # Note: Scrapling returns a list directly, not a locator
            links = page.css('a[href*="/episode/"]')
            
            logger.info(f"Found {len(links)} episode links")
            
            for link in links[:100]:  # Limit to 100 episodes
                try:
                    href = link.attrib.get('href', '')
                    text = link.text
                    
                    if href and EPISODE_PATTERN in href:
                        # Make absolute URL
                        full_url = href if href.startswith('http') else f"{BASE_URL}{href}"
                        
                        # Parse episode info
                        info = self.parser.parse_episode_url(full_url)
                        info["title"] = text.strip() if text else ""
                        
                        episodes.append(info)
                except Exception as e:
                    logger.warning(f"Error processing link: {e}")
                    continue
            
            return episodes
            
        except Exception as e:
            logger.error(f"Error getting episodes with Scrapling: {e}")
            return []

    def download_season_generator(self, season_url: str, season_number: int = None) -> Generator:
        """Generator for downloading season episodes using Scrapling with session"""
        try:
            logger.info(f"Starting download for: {season_url}")
            
            # Use session for better performance
            with StealthySession(headless=True, solve_cloudflare=True) as session:
                # Get episodes list
                page = session.fetch(season_url)
                links = page.css('a[href*="/episode/"]')
                
                episodes = []
                for link in links[:100]:
                    href = link.attrib.get('href', '')
                    if href and EPISODE_PATTERN in href:
                        full_url = href if href.startswith('http') else f"{BASE_URL}{href}"
                        info = self.parser.parse_episode_url(full_url)
                        info["title"] = link.text.strip() if link.text else ""
                        episodes.append(info)
                
                total = len(episodes)
                yield {"type": "start", "total": total}
                
                for i, ep in enumerate(episodes, 1):
                    title = ep.get('title', 'Unknown')
                    yield {"type": "progress", "current": i, "total": total, "title": title}
                    
                    try:
                        # Fetch episode page (reuses session)
                        ep_page = session.fetch(ep["episode_url"])
                        
                        # Extract video URL
                        video_url = ep_page.css_first('iframe[src*="embed"]::attr(src)')
                        if not video_url:
                            video_url = ep_page.css_first('video::attr(src)')
                        if not video_url:
                            video_url = ep_page.css_first('a[href*=".mp4"]::attr(href)')
                        
                        if video_url:
                            result = {
                                **ep,
                                "video_url": video_url,
                                "video_info": self.parser.parse_video_url(video_url),
                                "metadata": {"size_bytes": 0, "size_formatted": "Unknown"},
                                "thumbnail": ep_page.css_first('meta[property="og:image"]::attr(content)') or ""
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
