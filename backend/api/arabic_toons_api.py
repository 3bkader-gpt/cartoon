"""
Unofficial API for arabic-toons.com
استخراج video URLs و قائمة الحلقات
"""

from playwright.sync_api import sync_playwright
import re
from typing import Optional, List, Dict, Union
from urllib.parse import urlparse, parse_qs


class ArabicToonsAPI:
    """API class لموقع arabic-toons.com"""
    
    BASE_URL = "https://www.arabic-toons.com"
    CDN_BASE = "https://stream.foupix.com/animeios2_4"
    
    def __init__(self, headless: bool = True):
        """
        Initialize API
        
        Args:
            headless: Run browser in headless mode
        """
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
    
    def __enter__(self):
        """Context manager entry"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def get_page_metadata(self, page) -> Dict:
        """
        Extract metadata (title, breadcrumbs, thumbnail) from the open page
        """
        try:
            return page.evaluate("""
                () => {
                    const h1 = document.querySelector('h1')?.innerText || '';
                    const breadcrumbs = Array.from(document.querySelectorAll('.breadcrumb li, .breadcrumb a')).map(el => el.innerText);
                    const title = document.title;
                    
                    // Try to get thumbnail from og:image meta tag
                    let thumbnail = document.querySelector('meta[property="og:image"]')?.content || '';
                    
                    // Fallback: try to find poster image
                    if (!thumbnail) {
                        thumbnail = document.querySelector('.poster img, .anime-poster img, img[class*="poster"]')?.src || '';
                    }
                    
                    // Fallback: get first image on page
                    if (!thumbnail) {
                        thumbnail = document.querySelector('img')?.src || '';
                    }
                    
                    return { h1, breadcrumbs, title, thumbnail };
                }
            """)
        except:
            return {"h1": "", "breadcrumbs": [], "title": "", "thumbnail": ""}

    def get_episode_video_url(self, episode_url: str, include_metadata: bool = False) ->  Union[str, Dict, None]:
        """
        استخراج video URL من صفحة حلقة
        
        Args:
            episode_url: URL صفحة الحلقة
            include_metadata: If True, returns dict with url and metadata
            
        Returns:
            Video URL (str) or Dict {video_url, metadata} or None
        """
        page = self.context.new_page()
        
        try:
            # فتح صفحة الحلقة
            page.goto(episode_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)  # انتظار تحميل JavaScript
            
            # استخراج video URL
            video_url = page.evaluate("""
                () => {
                    const video = document.querySelector('video');
                    if (video) {
                        return video.currentSrc || video.src || null;
                    }
                    return null;
                }
            """)
            
            # إذا لم نجد في video element، نبحث في page content
            if not video_url:
                page_content = page.content()
                foupix_pattern = r'https://stream\.foupix\.com/[^\s"\'<>]+\.mp4[^\s"\'<>]*'
                matches = re.findall(foupix_pattern, page_content)
                if matches:
                    video_url = matches[0]
            
            if include_metadata and video_url:
                metadata = self.get_page_metadata(page)
                return {
                    "video_url": video_url,
                    "metadata": metadata
                }
            
            return video_url
            
        except Exception as e:
            print(f"Error extracting video URL from {episode_url}: {e}")
            return None
        finally:
            page.close()

    def get_video_metadata(self, video_url: str) -> Dict:
        """
        Get video file metadata (size, etc.) using HTTP HEAD request
        
        Args:
            video_url: Direct video URL
            
        Returns:
            Dictionary with size_bytes, size_mb, etc.
        """
        import requests
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.arabic-toons.com/"
        }
        
        try:
            response = requests.head(video_url, headers=headers, timeout=10)
            content_length = response.headers.get('Content-Length')
            
            if content_length:
                size_bytes = int(content_length)
                size_mb = round(size_bytes / (1024 * 1024), 2)
                size_gb = round(size_bytes / (1024 * 1024 * 1024), 2)
                
                # Format size nicely
                if size_gb >= 1:
                    size_formatted = f"{size_gb} GB"
                else:
                    size_formatted = f"{size_mb} MB"
                
                return {
                    "size_bytes": size_bytes,
                    "size_mb": size_mb,
                    "size_gb": size_gb,
                    "size_formatted": size_formatted
                }
            else:
                return {
                    "size_bytes": None,
                    "size_mb": None,
                    "size_gb": None,
                    "size_formatted": "Unknown"
                }
        except Exception as e:
            print(f"Error getting video metadata: {e}")
            return {
                "size_bytes": None,
                "size_mb": None,
                "size_gb": None,
                "size_formatted": "Unknown"
            }

    def get_episode_info(self, episode_url: str) -> Dict:
        """
        استخراج معلومات الحلقة من URL
        
        Args:
            episode_url: URL صفحة الحلقة
            
        Returns:
            Dictionary يحتوي على series_id, episode_id, etc.
        """
        parts = episode_url.split('/')[-1].replace('.html', '').split('-')
        return {
            "episode_url": episode_url,
            "series_slug": '-'.join(parts[:-2]) if len(parts) >= 2 else None,
            "series_id": parts[-2] if len(parts) >= 2 else None,
            "episode_id": parts[-1] if parts else None
        }
    
    def parse_video_url(self, video_url: str) -> Dict:
        """
        تحليل video URL لاستخراج المعلومات
        
        Args:
            video_url: Video URL كامل
            
        Returns:
            Dictionary يحتوي على series_id, filename, tokens, etc.
        """
        parsed = urlparse(video_url)
        params = parse_qs(parsed.query)
        
        # Extract path info
        path_parts = parsed.path.strip('/').split('/')
        series_id = path_parts[-2] if len(path_parts) >= 2 else None
        filename = path_parts[-1] if path_parts else None
        
        # Extract filename pattern
        series_name = season = episode = None
        if filename:
            # Pattern 1: name_s01_01.mp4
            match1 = re.match(r'(.+?)_s(\d+)_(\d+)\.mp4', filename)
            if match1:
                series_name, season, episode = match1.groups()
            else:
                # Pattern 2: SeriesID_Episode.mp4 (e.g. 1477294121_10.mp4)
                match2 = re.match(r'(\d+)_(\d+)\.mp4', filename)
                if match2:
                    # In this case, group 1 is likely series_id (already extracted), group 2 is episode
                    episode = match2.group(2)
                    # We don't have season info in this format, usually it's season 1 or unknown
        
        return {
            "full_url": video_url,
            "base_url": f"{parsed.scheme}://{parsed.netloc}{'/'.join(path_parts[:-1])}",
            "series_id": series_id,
            "filename": filename,
            "series_name": series_name,
            "season": season,
            "episode": episode,
            "parameters": {
                "tkn": params.get("tkn", [None])[0],
                "tms": params.get("tms", [None])[0],
                "ua": params.get("ua", [None])[0],
                "ips": params.get("ips", [None])[0],
                "_": params.get("_", [None])[0]
            }
        }
    
    def get_series_episodes(self, series_url: str) -> tuple[List[Dict], str]:
        """
        جلب قائمة الحلقات من صفحة المسلسل
        
        Args:
            series_url: URL صفحة المسلسل
            
        Returns:
            Tuple containing (List of episodes, Series Title)
        """
        page = self.context.new_page()
        episodes = []
        
        try:
            page.goto(series_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2000)
            
            # البحث عن روابط الحلقات
            episode_links = page.locator("a[href*='.html']")
            count = episode_links.count()
            
            for i in range(min(count, 100)):  # Limit to 100 episodes
                try:
                    link = episode_links.nth(i)
                    href = link.get_attribute("href")
                    text = link.inner_text()
                    
                    # Filter episode links
                    # Accept links with .html (even if they have #sets or other fragments)
                    if href and "anime-streaming" not in href and ".html" in href:
                        # Remove hash fragment if present
                        clean_href = href.split('#')[0]
                        full_url = clean_href if clean_href.startswith('http') else f"{self.BASE_URL}/{clean_href.lstrip('/')}"
                        episode_info = self.get_episode_info(full_url)
                        episode_info["title"] = text.strip()
                        episodes.append(episode_info)
                except:
                    continue
            
            # Extract series title from H1
            series_title = "Unknown Series"
            try:
                h1 = page.query_selector('h1')
                if h1:
                    series_title = h1.inner_text().strip()
            except:
                pass

            return episodes, series_title
            
        except Exception as e:
            print(f"Error getting series episodes: {e}")
            return []
        finally:
            page.close()
    
    def get_episode_with_video(self, episode_url: str) -> Dict:
        """
        جلب معلومات الحلقة مع video URL
        
        Args:
            episode_url: URL صفحة الحلقة
            
        Returns:
            Dictionary يحتوي على معلومات الحلقة + video URL
        """
        episode_info = self.get_episode_info(episode_url)
        video_url = self.get_episode_video_url(episode_url)
        
        result = {
            **episode_info,
            "video_url": video_url
        }
        
        if video_url:
            result["video_info"] = self.parse_video_url(video_url)
        
        return result
    
    def download_season_generator(self, series_url: str, season_number: int = None):
        """
        Generator version of download_season for streaming responses
        Yields progress updates and results using parallel processing
        """
        import logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        logger.info(f"Starting download_season_generator for: {series_url}")
        
        try:
            episodes, series_title = self.get_series_episodes(series_url)
            logger.info(f"Found {len(episodes)} episodes initially for '{series_title}'")
        except Exception as e:
            logger.error(f"Error fetching series episodes: {e}")
            yield {"type": "error", "episode": "Series", "message": f"Failed to fetch episodes: {str(e)}"}
            return

        # Filter by season if specified
        if season_number:
            episodes = [ep for ep in episodes if f"s{season_number}" in ep.get("episode_url", "")]
            logger.info(f"Filtered to {len(episodes)} episodes for season {season_number}")
        
        total = len(episodes)
        total = len(episodes)
        yield {"type": "start", "total": total, "series_title": series_title}
        
        for i, episode in enumerate(episodes, 1):
            episode_url = episode.get("episode_url")
            title = episode.get('title', 'Unknown')
            
            if not episode_url:
                logger.warning(f"Skipping episode {i} due to missing URL")
                continue
            
            logger.info(f"Processing episode {i}/{total}: {title}")
            
            # Yield progress update BEFORE processing
            yield {"type": "progress", "current": i, "total": total, "title": title}
            
            try:
                logger.info(f"Extracting video for: {episode_url}")
                result_data = self.get_episode_video_url(episode_url, include_metadata=True)
                
                if result_data:
                    if isinstance(result_data, str):
                        video_url = result_data
                        page_metadata = {}
                    else:
                        video_url = result_data.get("video_url")
                        page_metadata = result_data.get("metadata", {})
                    
                    logger.info(f"Success episode {i}: {video_url}")
                    
                    # Get video metadata (size, etc.)
                    video_metadata = self.get_video_metadata(video_url)
                    
                    result = {
                        **episode,
                        "video_url": video_url,
                        "video_info": self.parse_video_url(video_url),
                        "metadata": video_metadata,  # Add size info
                        "thumbnail": page_metadata.get("thumbnail", "")  # Add thumbnail
                    }
                    yield {"type": "result", "data": result}
                else:
                    logger.warning(f"Failed to extract video for episode {i}")
                    yield {"type": "error", "episode": title, "message": "Could not extract video URL"}
            except Exception as e:
                logger.error(f"Exception processing episode {i}: {e}")
                yield {"type": "error", "episode": title, "message": str(e)}
        
        logger.info("Finished download_season_generator")

    def search(self, query: str) -> List[Dict]:
        """
        البحث عن كرتون عن طريق جلب قائمة المسلسلات وفلترتها محلياً
        (لأن البحث في الموقع Client-Side)
        """
        print(f"DEBUG: Starting Local Search for '{query}'")
        page = self.context.new_page()
        results = []
        
        try:
            # 1. Go to Homepage
            page.goto(self.BASE_URL, wait_until="domcontentloaded", timeout=30000)
            
            # 2. Click 'مسلسلات' (Series) to get the full list
            # Using the selector from your codegen
            series_link = page.get_by_role("link", name="مسلسلات").first
            
            if series_link.count() > 0:
                print("DEBUG: Navigating to Series list...")
                series_link.click()
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(2000) # Wait for items to render
            else:
                print("DEBUG: 'مسلسلات' link not found, scanning homepage...")

            # 3. Scrape ALL items on the page
            print("DEBUG: Scraping all items...")
            
            # Try common selectors for grid items
            item_selectors = ['.anime-card', '.movie_poster', '.video-card', '.col-md-2', '.item', '.movie-item']
            
            items_found = []
            for sel in item_selectors:
                elements = page.locator(sel).all()
                if len(elements) > 10: # If we found a good chunk of items
                    items_found = elements
                    print(f"DEBUG: Found {len(elements)} items using selector '{sel}'")
                    break
            
            # Fallback: Look for any link with an image (common card pattern)
            if not items_found:
                print("DEBUG: Using fallback selector (links with images)...")
                items_found = page.locator("a:has(img)").all()

            print(f"DEBUG: Filtering {len(items_found)} items for '{query}'...")
            
            # 4. Filter items locally
            seen_urls = set()
            
            for item in items_found:
                try:
                    # Extract Text (Title)
                    text = item.inner_text().strip()
                    if not text:
                        text = item.get_attribute("title") or ""
                    if not text:
                        # Try alt text of image
                        img = item.locator("img").first
                        if img.count() > 0:
                            text = img.get_attribute("alt") or ""
                    
                    if not text:
                        continue
                        
                    # Check if query matches (Case insensitive)
                    # Normalize text (remove tashkeel if needed, but simple contains is usually enough)
                    if query.lower() in text.lower():
                        
                        # Extract URL
                        # If item is 'a', use it. If not, find 'a' inside.
                        if item.evaluate("el => el.tagName === 'A'"):
                            link = item
                        else:
                            link = item.locator("a").first
                        
                        href = link.get_attribute("href")
                        if not href or "anime-streaming" not in href:
                            continue
                            
                        full_url = href if href.startswith('http') else f"{self.BASE_URL}/{href.lstrip('/')}"
                        
                        if full_url in seen_urls:
                            continue
                            
                        # Extract Image
                        img_src = None
                        img = item.locator("img").first
                        if img.count() > 0:
                            img_src = img.get_attribute("src")
                        
                        # Determine type
                        is_episode = "الحلقة" in text or "Episode" in text
                        result_type = "episode" if is_episode else "series"
                        
                        seen_urls.add(full_url)
                        results.append({
                            "title": text,
                            "url": full_url,
                            "image": img_src,
                            "type": result_type
                        })
                        
                        if len(results) >= 20:
                            break
                except:
                    continue
            
            print(f"DEBUG: Found {len(results)} matching results")
            return results
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
        finally:
            page.close()

    def download_season(self, series_url: str, season_number: int = None) -> List[Dict]:
        """
        Legacy wrapper for backward compatibility
        """
        results = []
        for item in self.download_season_generator(series_url, season_number):
            if item["type"] == "result":
                results.append(item["data"])
        return results

    def search(self, query: str) -> List[Dict]:
        """
        البحث عن كرتون عن طريق جلب قائمة المسلسلات وفلترتها محلياً
        (لأن البحث في الموقع Client-Side)
        """
        print(f"DEBUG: Starting Local Search for '{query}'")
        page = self.context.new_page()
        results = []
        
        try:
            # 1. Go to Homepage
            page.goto(self.BASE_URL, wait_until="domcontentloaded", timeout=30000)
            
            # 2. Click 'مسلسلات' (Series) to get the full list
            # Using the selector from your codegen
            series_link = page.get_by_role("link", name="مسلسلات").first
            
            if series_link.count() > 0:
                print("DEBUG: Navigating to Series list...")
                series_link.click()
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(2000) # Wait for items to render
            else:
                print("DEBUG: 'مسلسلات' link not found, scanning homepage...")

            # 3. Scrape ALL items on the page
            print("DEBUG: Scraping all items...")
            
            # Try common selectors for grid items
            item_selectors = ['.anime-card', '.movie_poster', '.video-card', '.col-md-2', '.item', '.movie-item']
            
            items_found = []
            for sel in item_selectors:
                elements = page.locator(sel).all()
                if len(elements) > 10: # If we found a good chunk of items
                    items_found = elements
                    print(f"DEBUG: Found {len(elements)} items using selector '{sel}'")
                    break
            
            # Fallback: Look for any link with an image (common card pattern)
            if not items_found:
                print("DEBUG: Using fallback selector (links with images)...")
                items_found = page.locator("a:has(img)").all()

            print(f"DEBUG: Filtering {len(items_found)} items for '{query}'...")
            
            # 4. Filter items locally
            seen_urls = set()
            
            for item in items_found:
                try:
                    # Extract Text (Title)
                    text = item.inner_text().strip()
                    if not text:
                        text = item.get_attribute("title") or ""
                    if not text:
                        # Try alt text of image
                        img = item.locator("img").first
                        if img.count() > 0:
                            text = img.get_attribute("alt") or ""
                    
                    if not text:
                        continue
                        
                    # Check if query matches (Case insensitive)
                    # Normalize text (remove tashkeel if needed, but simple contains is usually enough)
                    if query.lower() in text.lower():
                        
                        # Extract URL
                        # If item is 'a', use it. If not, find 'a' inside.
                        if item.evaluate("el => el.tagName === 'A'"):
                            link = item
                        else:
                            link = item.locator("a").first
                        
                        href = link.get_attribute("href")
                        if not href or "anime-streaming" not in href:
                            continue
                            
                        full_url = href if href.startswith('http') else f"{self.BASE_URL}/{href.lstrip('/')}"
                        
                        if full_url in seen_urls:
                            continue
                            
                        # Extract Image
                        img_src = None
                        img = item.locator("img").first
                        if img.count() > 0:
                            img_src = img.get_attribute("src")
                        
                        # Determine type
                        is_episode = "الحلقة" in text or "Episode" in text
                        result_type = "episode" if is_episode else "series"
                        
                        seen_urls.add(full_url)
                        results.append({
                            "title": text,
                            "url": full_url,
                            "image": img_src,
                            "type": result_type
                        })
                        
                        if len(results) >= 20:
                            break
                except:
                    continue
            
            print(f"DEBUG: Found {len(results)} matching results")
            return results
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
        finally:
            page.close()

    def download_season(self, series_url: str, season_number: int = None) -> List[Dict]:
        """
        Legacy wrapper for backward compatibility
        """
        results = []
        for item in self.download_season_generator(series_url, season_number):
            if item["type"] == "result":
                results.append(item["data"])
        return results
    
    # The original `page.close()` was misplaced here, it should be inside the `download_season` method's `finally` block if it were to close a page opened within that method.
    # However, `download_season` uses `download_season_generator` which handles its own page closing.
    # So, this line is removed as it was likely a leftover or misplaced.
    # page.close()

if __name__ == "__main__":
    # Example usage
    with ArabicToonsAPI(headless=True) as api:
        # Test search
        print("Searching for 'conan'...")
        results = api.search("conan")
        for r in results:
            print(f"Found: {r['title']} ({r['type']})")

