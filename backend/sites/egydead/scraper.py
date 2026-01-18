"""
EgyDead Scraper
Handles scraping logic for egydead.skin using Playwright
"""

import logging
import re
from typing import List, Dict, Generator, Optional
from ...core.browser import BrowserManager
from ...extractors import ExtractorFactory
from .parser import EgyDeadParser
from .config import BASE_URL, SELECTORS, EPISODE_PATTERN

logger = logging.getLogger(__name__)

class EgyDeadScraper:
    """Scraper implementation for EgyDead using Playwright"""
    
    def __init__(self, browser_manager: BrowserManager = None):
        self.browser_manager = browser_manager or BrowserManager()
        self.parser = EgyDeadParser()

    def get_episode_video_url(self, episode_url: str, include_metadata: bool = False):
        """Extract video URL from episode page"""
        context = self.browser_manager.get_context()
        page = context.new_page()
        sources = []
        
        try:
            logger.info(f"Navigating to episode page: {episode_url}")
            page.goto(episode_url, wait_until="domcontentloaded", timeout=30000)
            
            # 1. Try to find Watch Now button and click it FIRST
            # This reveals the download list with span.ser-name
            potential_sources = []
            
            download_btn = page.locator(SELECTORS["download_button"]).first
            
            if download_btn.count() > 0:
                logger.info("Found Watch Now button, clicking...")
                try:
                    # Try clicking with longer timeout
                    with page.expect_navigation(wait_until="domcontentloaded", timeout=15000):
                        download_btn.click()
                    logger.info(f"Page navigated to: {page.url}")
                    page.wait_for_timeout(3000)  # Wait for download list to appear
                except Exception as nav_e:
                    logger.warning(f"Navigation check failed or timed out: {nav_e}")
                    # Try clicking without waiting for navigation
                    try:
                        download_btn.click()
                        page.wait_for_timeout(3000)
                        logger.info(f"Clicked button, current URL: {page.url}")
                    except Exception as click_e:
                        logger.warning(f"Click also failed: {click_e}")
            
            # 2. Capture Download List (AFTER clicking Watch Now)
            # Try multiple strategies to find download links
            # Strategy A: Find by span.ser-name (most common structure after Watch Now click)
            ser_name_spans = page.locator("span.ser-name")
            if ser_name_spans.count() > 0:
                logger.info(f"Found {ser_name_spans.count()} servers using span.ser-name")
                # Extract links from parent elements
                for i in range(ser_name_spans.count()):
                    try:
                        span = ser_name_spans.nth(i)
                        text = span.inner_text()
                        parent = span.locator("..")  # Parent element (usually <li>)
                        
                        # Find link in parent or grandparent
                        link = parent.locator("a").first
                        if link.count() == 0:
                            grandparent = parent.locator("..")
                            link = grandparent.locator("a").first
                        
                        if link.count() > 0:
                            href = link.get_attribute("href")
                            if href and "javascript" not in href:
                                # Get quality from <em> tag if available
                                em = parent.locator("em").first
                                quality_text = em.inner_text() if em.count() > 0 else "Unknown"
                                
                                quality = "Unknown"
                                quality_lower = quality_text.lower()
                                if "1080" in quality_lower: quality = "1080p"
                                elif "720" in quality_lower: quality = "720p"
                                elif "480" in quality_lower: quality = "480p"
                                elif "360" in quality_lower: quality = "360p"
                                
                                server_name = text.strip()
                                # Don't clean "تحميل متعدد" - we need it for detection
                                if "تحميل متعدد" not in server_name:
                                    for prefix in ["تحميل", "سيرفر", "Download", "Server"]:
                                        server_name = server_name.replace(prefix, "").strip()
                                
                                potential_sources.append({
                                    "url": href,
                                    "quality": quality,
                                    "server": server_name if server_name else "Server"
                                })
                    except Exception as e:
                        logger.debug(f"Error reading ser-name span {i}: {e}")
            
            # Strategy B: Standard Selectors (fallback)
            if not potential_sources:
                dl_selectors = [
                    ".DownloadList li a",
                    ".dls_table tbody tr a", 
                    "ul.downloads li a",
                    ".servers_list li a",
                    "a.dlink"
                ]
                
                download_list = None
                for sel in dl_selectors:
                    elements = page.locator(sel)
                    if elements.count() > 0:
                        logger.info(f"Found download list using selector: {sel}")
                        download_list = elements
                        break
                
                if download_list and download_list.count() > 0:
                    count = download_list.count()
                    logger.info(f"Found {count} download servers/links")
                    
                    for i in range(count):
                        try:
                            link = download_list.nth(i)
                            href = link.get_attribute("href")
                            text = link.inner_text() or link.get_attribute("title") or "Server"
                            
                            if href and "javascript" not in href:
                                quality = "Unknown"
                                text_lower = text.lower()
                                if "1080" in text_lower: quality = "1080p"
                                elif "720" in text_lower: quality = "720p"
                                elif "480" in text_lower: quality = "480p"
                                elif "360" in text_lower: quality = "360p"
                                
                                server_name = text.strip()
                                for prefix in ["تحميل", "سيرفر", "Download", "Server"]:
                                    server_name = server_name.replace(prefix, "").strip()

                                potential_sources.append({
                                    "url": href,
                                    "quality": quality,
                                    "server": server_name if server_name else "Server"
                                })
                        except Exception as e:
                            logger.warning(f"Error reading download link {i}: {e}")
            
            # Strategy C: Find by text if selectors fail
            if not potential_sources:
                box = page.locator("div", has=page.locator("text=تحميل")).last
                if box.count() > 0:
                     links = box.locator("a")
                     if links.count() > 0:
                         logger.info("Found download links via text search")
                         download_list = links
                         for i in range(links.count()):
                             try:
                                 link = links.nth(i)
                                 href = link.get_attribute("href")
                                 text = link.inner_text() or "Server"
                                 if href and "javascript" not in href:
                                     potential_sources.append({
                                         "url": href,
                                         "quality": "Unknown",
                                         "server": text.strip()
                                     })
                             except Exception as e:
                                 logger.debug(f"Error reading link {i}: {e}")

            # 3. Extract Primary Video URL (Current Page)
            video_url = None
            
            # Check provider stuff and extractors on current page (Forafile, etc)
            current_url = page.url
            
            # A. Check for known extractors first (Forafile/Redirected page)
            if ExtractorFactory.needs_extraction(current_url):
                logger.info(f"Detected server URL, using extractor: {current_url}")
                try:
                    extractor = ExtractorFactory.get_extractor(current_url, context)
                    result = extractor.extract(current_url, page)
                    
                    # Handle result
                    from ...extractors.base import ExtractionResult
                    if result:
                        if isinstance(result, list):
                            for res in result:
                                res_dict = res.to_dict() if hasattr(res, 'to_dict') else res
                                if res_dict.get("video_url"):
                                    sources.append({
                                        "url": res_dict["video_url"],
                                        "quality": res_dict.get("quality", "Unknown"),
                                        "server": res_dict.get("server", "Extractor"),
                                        "type": "direct",
                                        "metadata": res_dict.get("metadata", {})
                                    })
                                    if not video_url: video_url = res_dict["video_url"]
                        else:
                            res_dict = result.to_dict() if hasattr(result, 'to_dict') else result
                            if res_dict.get("video_url"):
                                video_url = res_dict["video_url"]
                                sources.append({
                                    "url": video_url,
                                    "quality": res_dict.get("quality", "Auto"),
                                    "server": res_dict.get("server", "Primary"),
                                    "type": "direct"
                                })
                except Exception as e:
                     logger.warning(f"Error using extractor for {current_url}: {e}")

            # C. Check for provider links (Anchor tags) if no direct video found
            # This logic was missing! It finds links like forafile.com in the body
            if not video_url:
                provider_url = page.evaluate("""
                    () => {
                        const links = document.querySelectorAll('a[href*="forafile"], a[href*="foupix"], a[href*="uqload"]');
                        for (const link of links) {
                            if (link.href) return link.href;
                        }
                        return null;
                    }
                """)
                
                if provider_url:
                    logger.info(f"Found provider URL: {provider_url}")
                    try:
                        # Navigate to provider page if we are not already there
                        if page.url != provider_url:
                            page.goto(provider_url, wait_until="domcontentloaded", timeout=30000)
                        
                        # Use Extractor on new URL
                        if ExtractorFactory.needs_extraction(provider_url):
                             extractor = ExtractorFactory.get_extractor(provider_url, context)
                             res = extractor.extract(provider_url, page)
                             
                             if res:
                                 if isinstance(res, list):
                                     for r in res:
                                         rd = r.to_dict() if hasattr(r, 'to_dict') else r
                                         if rd.get("video_url"):
                                             sources.append({
                                                 "url": rd["video_url"],
                                                 "quality": rd.get("quality", "Unknown"),
                                                 "server": rd.get("server", "Provider"),
                                                 "type": "direct",
                                                 "metadata": rd.get("metadata", {})
                                             })
                                             if not video_url: video_url = rd["video_url"]
                                 else:
                                     rd = res.to_dict() if hasattr(res, 'to_dict') else res
                                     if rd.get("video_url"):
                                         video_url = rd["video_url"]
                                         sources.append({
                                             "url": video_url, 
                                             "quality": "Auto", 
                                             "server": "Provider", 
                                             "type": "direct"
                                         })
                    except Exception as e:
                        logger.warning(f"Error handling provider URL {provider_url}: {e}")

            # B. Fallback checks (iframe, generic video tag)
            if not video_url:
                # Check for iframe
                iframe = page.locator('iframe').first
                if iframe.count() > 0:
                    src = iframe.get_attribute("src")
                    if src and ("google" not in src and "facebook" not in src):
                        # Special handling for provider iframes
                        if "forafile" in src or "foupix" in src or "uqload" in src:
                             # ... provider logic ...
                             # For brevity, rely on recursive extractor call if we navigated there. 
                             # But here we assume we might need to navigate.
                             try:
                                 page.goto(src, wait_until="domcontentloaded")
                                 # Recursively try extractor on new URL
                                 if ExtractorFactory.needs_extraction(src):
                                      extractor = ExtractorFactory.get_extractor(src, context)
                                      res = extractor.extract(src, page) # Reuse page
                                      if res:
                                           # Add result ...
                                           res_dict = res.to_dict() if hasattr(res, 'to_dict') else res
                                           if res_dict.get("video_url"):
                                                video_url = res_dict["video_url"]
                                                sources.append({"url": video_url, "quality": "Auto", "server": "Provider", "type": "direct"})
                             except: pass
                        else:
                             video_url = src

            if not video_url:
                 # Generic check
                 video_url = page.evaluate("""() => {
                        const v = document.querySelector('video');
                        if (v) return v.src || v.currentSrc;
                        const s = document.querySelector('source[src*=".mp4"]');
                        if (s) return s.src;
                        return null;
                 }""")

            # 4. Process Potential Sources (Multi Download)
            # Now we iterate through the list we captured in Step 1
            if potential_sources:
                logger.info(f"Processing {len(potential_sources)} potential additional sources...")
                
                # We can reuse 'page' now since we are done with primary video
                # OR use a new page to be safe. Let's reuse 'page' to save resources, 
                # but be aware of navigation state.
                
                for source in potential_sources:
                    s_url = source["url"]
                    s_server = source["server"]
                    
                    # Check if it's a Multi server (تحميل متعدد or known Multi domains)
                    is_multi = (
                        "تحميل متعدد" in s_server or 
                        "Multi" in s_server or 
                        "haxloppd" in s_url or 
                        "hglink" in s_url or 
                        "cavanhabg" in s_url or
                        "premilkyway" in s_url
                    )
                    
                    logger.debug(f"Processing source: {s_server}, URL: {s_url[:50]}..., is_multi: {is_multi}, needs_extraction: {ExtractorFactory.needs_extraction(s_url)}")
                    
                    # Only process if it looks like a Multi server or needs extraction
                    if is_multi or ExtractorFactory.needs_extraction(s_url):
                        try:
                            logger.info(f"Resolving additional source: {s_server}")
                            extractor = ExtractorFactory.get_extractor(s_url, context)
                            
                            # We must be careful reusing 'page' if extractor closes it or fails. 
                            # MultiServerExtractor is well behaved now.
                            # But if we navigate away, we can't 'go back' easily without reloading.
                            # Since we have a list of URLs, we just navigate to the next one.
                            
                            res = extractor.extract(s_url, page)
                            
                            if res:
                                if isinstance(res, list):
                                    for r in res:
                                        rd = r.to_dict() if hasattr(r, 'to_dict') else r
                                        if rd.get("video_url"):
                                            sources.append({
                                                "url": rd["video_url"],
                                                "quality": rd.get("quality", source["quality"]),
                                                "server": rd.get("server", s_server),
                                                "type": "direct",
                                                "metadata": rd.get("metadata", {})
                                            })
                                else:
                                    rd = res.to_dict() if hasattr(res, 'to_dict') else res
                                    if rd.get("video_url"):
                                        sources.append({
                                            "url": rd["video_url"],
                                            "quality": rd.get("quality", source["quality"]),
                                            "server": rd.get("server", s_server),
                                            "type": "direct"
                                        })
                        except Exception as e:
                            logger.warning(f"Failed to resolve source {s_server}: {e}")
                    else:
                         # Just add as server link
                         sources.append({
                             "url": s_url,
                             "quality": source["quality"],
                             "server": s_server,
                             "type": "server"
                         })

            # 5. Finalize Result
            if video_url:
                 # Ensure primary video is in sources
                 found = False
                 for s in sources:
                     if s["url"] == video_url:
                         found = True
                         break
                 if not found:
                     sources.insert(0, {
                         "url": video_url,
                         "quality": "Auto",
                         "server": "Primary",
                         "type": "direct"
                     })
            
            if include_metadata:
                metadata = self.parser.get_page_metadata(page)
                return {"video_url": video_url, "sources": sources, "metadata": metadata}

            return {"video_url": video_url, "sources": sources}
            
        except Exception as e:
            logger.error(f"Error processing episode: {e}")
            return {"video_url": None, "sources": [], "error": str(e)}
        finally:
            page.close()

    def get_series_episodes(self, series_url: str) -> List[Dict]:
        """Get all episodes from season page"""
        context = self.browser_manager.get_context()
        page = context.new_page()
        episodes = []
        
        try:
            logger.info(f"Navigating to season page: {series_url}")
            page.goto(series_url, wait_until="domcontentloaded", timeout=30000)
            
            # Find all episode links
            links = page.locator(SELECTORS["episode_links"])
            count = links.count()
            
            logger.info(f"Found {count} episode links")
            
            # Iterate in reverse order (since site lists them descending)
            for i in range(count - 1, -1, -1):
                try:
                    link = links.nth(i)
                    href = link.get_attribute("href")
                    text = link.inner_text()
                    
                    if href and EPISODE_PATTERN in href:
                        full_url = href if href.startswith('http') else f"{BASE_URL}{href}"
                        
                        info = self.parser.parse_episode_url(full_url)
                        info["title"] = text.strip() if text else info["title"]
                        
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

    def download_season_generator(self, season_url: str, season_number: int = None) -> Generator:
        """Generator for downloading season episodes"""
        try:
            episodes = self.get_series_episodes(season_url)
            
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
                        
                        result = {
                            **ep,
                            "video_url": video_url,
                            "video_info": self.parser.parse_video_url(video_url),
                            "metadata": {"size_bytes": 0, "size_formatted": "Unknown"}, # Size usually unknown until download
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
