import re
import logging
import requests
import traceback
from typing import List, Dict, Generator
from ...core.browser import BrowserManager
from .parser import ArabicToonsParser
from .config import BASE_URL, SELECTORS

# Force logging to show
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def log(msg):
    """Print and log for guaranteed visibility"""
    print(msg, flush=True)
    logger.info(msg)

class ArabicToonsScraper:
    """Scraper implementation for Arabic Toons"""
    
    def __init__(self, browser_manager: BrowserManager = None):
        self.browser_manager = browser_manager or BrowserManager()
        self.parser = ArabicToonsParser()

    def get_episode_video_url(self, episode_url: str, include_metadata: bool = False):
        context = self.browser_manager.get_context()
        page = context.new_page()
        try:
            page.goto(episode_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)
            
            video_url = page.evaluate("""
                () => {
                    const video = document.querySelector('video');
                    return video ? (video.currentSrc || video.src) : null;
                }
            """)
            
            if not video_url:
                content = page.content()
                matches = re.findall(r'https://stream\.foupix\.com/[^\s"\'<>]+\.mp4[^\s"\'<>]*', content)
                if matches:
                    video_url = matches[0]
            
            if include_metadata and video_url:
                metadata = self.parser.get_page_metadata(page)
                return {"video_url": video_url, "metadata": metadata}
            
            return video_url
        except Exception as e:
            logger.error(f"Error extracting video URL: {e}")
            return None
        finally:
            page.close()

    def get_series_episodes(self, series_url: str) -> List[Dict]:
        log(f"🔍 get_series_episodes called with URL: {series_url}")
        context = self.browser_manager.get_context()
        page = context.new_page()
        episodes = []
        try:
            log(f"📄 Navigating to: {series_url}")
            page.goto(series_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2000)
            
            log(f"🔎 Looking for links with selector: {SELECTORS['series_link']}")
            links = page.locator(SELECTORS["series_link"])
            count = links.count()
            log(f"📊 Found {count} links on page")
            
            # Log first few link hrefs for debugging
            for i in range(min(10, count)):
                try:
                    href = links.nth(i).get_attribute("href")
                    text = links.nth(i).inner_text()
                    log(f"   Link {i}: href={href[:80] if href else 'None'}... text={text[:30] if text else 'N/A'}")
                except Exception as e:
                    log(f"   Link {i}: ERROR - {e}")
            
            for i in range(min(count, 100)):
                try:
                    link = links.nth(i)
                    href = link.get_attribute("href")
                    text = link.inner_text()
                    
                    # Episode links don't have "anime-streaming" but have .html
                    if href and "anime-streaming" not in href and ".html" in href:
                        clean_href = href.split('#')[0]
                        full_url = clean_href if clean_href.startswith('http') else f"{BASE_URL}/{clean_href.lstrip('/')}"
                        
                        # Clean up title: remove duplicate numbers (e.g., "الحلقة 1\n1" -> "الحلقة 1")
                        clean_title = text.strip()
                        lines = [line.strip() for line in clean_title.split('\n') if line.strip()]
                        if len(lines) > 1 and lines[-1].isdigit():
                            # Last line is just a number, likely duplicate
                            clean_title = ' '.join(lines[:-1])
                        else:
                            clean_title = ' '.join(lines)
                        
                        log(f"✅ Found episode: {clean_title[:40]} -> {full_url}")
                        info = self.parser.get_episode_info(full_url)
                        info["title"] = clean_title
                        episodes.append(info)
                except Exception as e:
                    log(f"⚠️ Error processing link {i}: {e}")
                    continue
            
            log(f"📋 Total episodes found: {len(episodes)}")
            return episodes
        except Exception as e:
            log(f"❌ Error getting episodes: {e}")
            log(traceback.format_exc())
            return []
        finally:
            page.close()

    def get_video_metadata(self, video_url: str) -> Dict:
        try:
            headers = {"User-Agent": "Mozilla/5.0", "Referer": BASE_URL}
            resp = requests.head(video_url, headers=headers, timeout=10)
            size = int(resp.headers.get('Content-Length', 0))
            
            if size:
                gb = size / (1024**3)
                mb = size / (1024**2)
                fmt = f"{gb:.2f} GB" if gb >= 1 else f"{mb:.2f} MB"
                return {"size_bytes": size, "size_formatted": fmt}
            return {"size_bytes": 0, "size_formatted": "Unknown"}
        except:
            return {"size_bytes": 0, "size_formatted": "Unknown"}

    def download_season_generator(self, series_url: str, season_number: int = None) -> Generator:
        log(f"🎬 download_season_generator called with URL: {series_url}")
        try:
            log("📥 Calling get_series_episodes...")
            episodes = self.get_series_episodes(series_url)
            log(f"📊 Got {len(episodes)} episodes")
            
            if season_number:
                episodes = [ep for ep in episodes if f"s{season_number}" in ep.get("episode_url", "")]
            
            total = len(episodes)
            log(f"📋 Total episodes to process: {total}")
            yield {"type": "start", "total": total}
            
            for i, ep in enumerate(episodes, 1):
                title = ep.get('title', 'Unknown')
                log(f"🎞️ Processing episode {i}/{total}: {title}")
                yield {"type": "progress", "current": i, "total": total, "title": title}
                
                try:
                    data = self.get_episode_video_url(ep["episode_url"], include_metadata=True)
                    if data:
                        video_url = data["video_url"] if isinstance(data, dict) else data
                        meta = data.get("metadata", {}) if isinstance(data, dict) else {}
                        
                        video_meta = self.get_video_metadata(video_url)
                        
                        result = {
                            **ep,
                            "video_url": video_url,
                            "video_info": self.parser.parse_video_url(video_url),
                            "metadata": video_meta,
                            "thumbnail": meta.get("thumbnail", "")
                        }
                        yield {"type": "result", "data": result}
                    else:
                        yield {"type": "error", "episode": title, "message": "No video URL"}
                except Exception as e:
                    log(f"❌ Error processing episode {title}: {e}")
                    yield {"type": "error", "episode": title, "message": str(e)}
                    
        except Exception as e:
            log(f"❌ FATAL ERROR in download_season_generator: {e}")
            log(traceback.format_exc())
            yield {"type": "error", "episode": "Series", "message": str(e)}

    def search(self, query: str) -> List[Dict]:
        # (Search logic similar to original, simplified for brevity)
        # For now, returning empty list to focus on core functionality
        # You can copy the full search logic here if needed
        return [] 
