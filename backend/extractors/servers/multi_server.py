"""
Multi Download Server Extractor
Handles extraction of multiple quality options from 'Multi Download' server
"""
import logging
import re
from typing import List, Optional
from playwright.sync_api import Page

from ..base import BaseExtractor, ExtractionResult

logger = logging.getLogger(__name__)

class MultiServerExtractor(BaseExtractor):
    """
    Extractor for Multi Download server that supports multiple quality options
    
    Returns a list of ExtractionResult objects, one for each available quality
    """
    
    def extract(self, url: str, page: Optional[Page] = None) -> List[ExtractionResult]:
        """
        Extracts multiple qualities from 'Multi Download' server.
        Returns a LIST of ExtractionResult objects.
        """
        should_close_page = False
        if not page:
            try:
                page = self.context.new_page()
                should_close_page = True
            except Exception as e:
                logger.error(f"Failed to create page: {e}")
                return []
        
        try:
            logger.info(f"MultiServerExtractor processing: {url}")
            # Setup page (ad blocking, popup handling) - only if page is valid
            try:
                self.setup_page(page)
            except Exception as setup_e:
                logger.warning(f"Failed to setup page: {setup_e}")
                # Continue anyway - page might still work
            
            # 1. Navigate to page if needed
            if page.url != url:
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=60000)
                except Exception:
                    pass # Already there or redirect
        
            # Handle initial redirects if any
            try:
                page.wait_for_load_state('networkidle', timeout=5000)
            except:
                pass


            # --- STEP 1: Handle "Download" / "Create Download Link" button ---
            # Flow: hglink.to → click Download → cavanhabg.com/f/... (with quality options)
            
            # Check if we need to click a download button first
            # Try multiple button selectors
            download_buttons = [
                "a[href*='/f/']",  # Try this first - it's the most reliable
                "a:has-text('Download')",
                "button:has-text('Download')",
                "a:has-text('Create Download Link')",
                "button:has-text('Create Download Link')"
            ]
            
            clicked_download = False
            
            # Check if we're already on the quality page (cavanhabg.com/f/...)
            if "cavanhabg.com/f/" in page.url or "haxloppd.com/f/" in page.url:
                logger.info("Already on quality selection page")
                clicked_download = True
            elif "cavanhabg.com" in page.url and "/f/" not in page.url:
                # We're on cavanhabg.com but not on /f/ page, try to navigate to /f/
                file_id = page.url.split('/')[-1]
                if file_id and file_id not in ['', 'f']:
                    try:
                        f_url = f"https://cavanhabg.com/f/{file_id}"
                        logger.info(f"Navigating to quality page: {f_url}")
                        page.goto(f_url, wait_until="domcontentloaded", timeout=20000)
                        page.wait_for_timeout(2000)
                        clicked_download = True
                        logger.info(f"Navigated to: {page.url}")
                    except Exception as nav_e:
                        logger.debug(f"Failed to navigate to /f/ page: {nav_e}")
            else:
                # Remove any overlays that might block clicks
                try:
                    self.remove_overlays(page)
                except Exception as overlay_e:
                    logger.debug(f"Error removing overlays: {overlay_e}")
                
                for btn_selector in download_buttons:
                    btn = page.locator(btn_selector).first
                    if btn.count() > 0:
                        try:
                            # Wait for countdown if exists
                            if page.locator("#countdown").count() > 0:
                                logger.info("Waiting for countdown...")
                                page.wait_for_timeout(5000)
                            
                            # Try JavaScript click if normal click fails
                            logger.info(f"Found download button ({btn_selector}), clicking...")
                            try:
                                with page.expect_navigation(timeout=20000, wait_until="domcontentloaded"):
                                    btn.click()
                                clicked_download = True
                                page.wait_for_timeout(2000)
                                logger.info(f"Navigated to: {page.url}")
                                break
                            except Exception as click_e:
                                # Try JavaScript click as fallback
                                logger.debug(f"Normal click failed, trying JavaScript click: {click_e}")
                                try:
                                    href = btn.get_attribute("href")
                                    if href:
                                        # Ensure we navigate to /f/ URL if it's a quality page
                                        if '/f/' not in href and 'cavanhabg.com' in page.url:
                                            # Try to construct /f/ URL
                                            file_id = page.url.split('/')[-1]
                                            if file_id:
                                                href = f"https://cavanhabg.com/f/{file_id}"
                                        
                                        page.goto(href, wait_until="domcontentloaded", timeout=20000)
                                        clicked_download = True
                                        page.wait_for_timeout(2000)
                                        logger.info(f"Navigated via href to: {page.url}")
                                        break
                                except Exception as js_e:
                                    logger.debug(f"JavaScript navigation also failed: {js_e}")
                                    continue
                        except Exception as e:
                            logger.debug(f"Error with {btn_selector}: {e}")
                            continue

            # --- STEP 2: Find Quality Options on Page ---
            results = []
            
            # Method 1: Look for quality text patterns (Full HD quality, HD quality, Normal quality)
            # Also check for "Click to download" links near quality text
            quality_patterns = [
                {"text": "Full HD quality", "quality": "1080p", "selector": "text=Full HD quality"},
                {"text": "HD quality", "quality": "720p", "selector": "text=HD quality"},
                {"text": "Normal quality", "quality": "480p", "selector": "text=Normal quality"},
                {"text": "SD quality", "quality": "480p", "selector": "text=SD quality"},
                {"text": "Low quality", "quality": "360p", "selector": "text=Low quality"},
            ]
            
            # Also try finding by "Click to download" text which appears near quality options
            click_to_download_links = page.locator("a:has-text('Click to download')")
            if click_to_download_links.count() > 0:
                logger.info(f"Found {click_to_download_links.count()} 'Click to download' links")
            
            found_qualities = []
            
            # First, try to find all links and match them with quality text
            # Get all links with their parent text to find quality options
            all_page_links = page.evaluate("""
                () => {
                    return Array.from(document.querySelectorAll('a')).map(a => ({
                        href: a.href,
                        text: a.innerText.trim(),
                        parentText: a.parentElement ? a.parentElement.innerText.trim() : '',
                        fullText: a.parentElement ? a.parentElement.innerText.trim() : a.innerText.trim()
                    }));
                }
            """)
            
            logger.info(f"Found {len(all_page_links)} total links on page")
            logger.info(f"Current page URL: {page.url}")
            
            # Match all links with quality patterns
            # The quality info is in the link text or parent text
            for link in all_page_links:
                full_text = link['fullText'].lower()
                href = link['href']
                
                if not href or "javascript" in href or href == "#":
                    continue
                
                # Match quality - check for quality indicators in full text
                quality = None
                size = "Unknown"
                
                # First check URL pattern (most reliable: setft11iyw7b_h, setft11iyw7b_n, setft11iyw7b_l)
                if href.endswith('_h') or ('/f/' in href and '_h' in href and not href.endswith('_n') and not href.endswith('_l')):
                    quality = "1080p"
                elif href.endswith('_n') or ('/f/' in href and '_n' in href and not href.endswith('_l')):
                    quality = "720p"
                elif href.endswith('_l') or ('/f/' in href and '_l' in href):
                    quality = "480p"
                # Then check for quality in full text (parent text contains quality info)
                elif "full hd quality" in full_text or ("full hd" in full_text and "1920" in full_text):
                    quality = "1080p"
                elif "hd quality" in full_text and "full" not in full_text or ("hd" in full_text and "1440" in full_text) or ("hd" in full_text and "720" in full_text):
                    quality = "720p"
                elif "normal quality" in full_text or ("normal" in full_text and "960" in full_text) or ("normal" in full_text and "480" in full_text):
                    quality = "480p"
                elif "360" in full_text:
                    quality = "360p"
                
                if quality:
                    # Extract size from full text
                    size_match = re.search(r'(\d+(?:\.\d+)?\s*(?:GB|MB|KB))', link['fullText'], re.IGNORECASE)
                    size = size_match.group(1) if size_match else "Unknown"
                    
                    # Construct absolute URL if relative
                    if not href.startswith("http"):
                        base_parts = page.url.split("/")[:3]
                        base_url = "/".join(base_parts)
                        href = base_url + href if href.startswith("/") else base_url + "/" + href
                    
                    if not any(q['url'] == href for q in found_qualities):
                        found_qualities.append({
                            "quality": quality,
                            "url": href,
                            "size": size,
                            "name": f"{quality} quality"
                        })
                        logger.info(f"Found quality: {quality} ({size}) - {href[:60]}...")
            
            # Fallback: Try to find quality options by text patterns
            if not found_qualities:
                logger.info("Trying text pattern matching...")
                for pattern in quality_patterns:
                    quality_elem = page.locator(pattern["selector"]).first
                    if quality_elem.count() > 0:
                        try:
                            # Get the parent element that contains the link and size
                            parent = quality_elem.locator("..")
                            if parent.count() == 0:
                                parent = quality_elem.locator("../..")
                            
                            # Find link in parent or nearby
                            link = parent.locator("a").first
                            if link.count() == 0:
                                # Try finding link by text "Click to download"
                                link = page.locator(f"a:has-text('Click to download'):near(text={pattern['text']})").first
                            
                            if link.count() > 0:
                                href = link.get_attribute("href")
                                if href:
                                    # Get size from parent text
                                    parent_text = parent.inner_text() if parent.count() > 0 else ""
                                    size_match = re.search(r'(\d+(?:\.\d+)?\s*(?:GB|MB|KB))', parent_text, re.IGNORECASE)
                                    size = size_match.group(1) if size_match else "Unknown"
                                    
                                    # Construct absolute URL if relative
                                    if not href.startswith("http"):
                                        base_parts = page.url.split("/")[:3]
                                        base_url = "/".join(base_parts)
                                        href = base_url + href if href.startswith("/") else base_url + "/" + href
                                    
                                    found_qualities.append({
                                        "quality": pattern["quality"],
                                        "url": href,
                                        "size": size,
                                        "name": pattern["text"]
                                    })
                                    logger.info(f"Found quality: {pattern['quality']} ({size}) - {href[:60]}...")
                        except Exception as e:
                            logger.debug(f"Error extracting {pattern['text']}: {e}")
            
            # Method 2: If no qualities found, try parsing page content
            if not found_qualities:
                logger.info("Trying alternative method: parsing page content...")
                page_content = page.evaluate("() => document.body.innerText")
                
                # Look for quality patterns in text
                for pattern in quality_patterns:
                    if pattern["text"].lower() in page_content.lower():
                        # Find all links and check which one is near this quality text
                        all_links = page.evaluate("""
                            () => {
                                return Array.from(document.querySelectorAll('a')).map(a => ({
                                    href: a.href,
                                    text: a.innerText.trim(),
                                    parentText: a.parentElement ? a.parentElement.innerText.trim() : ''
                                }));
                            }
                        """)
                        
                        for link in all_links:
                            if pattern["text"].lower() in link["parentText"].lower() or pattern["text"].lower() in link["text"].lower():
                                href = link["href"]
                                if href and "javascript" not in href and href != "#":
                                    # Extract size from parent text
                                    size_match = re.search(r'(\d+(?:\.\d+)?\s*(?:GB|MB|KB))', link["parentText"], re.IGNORECASE)
                                    size = size_match.group(1) if size_match else "Unknown"
                                    
                                    if not any(q['url'] == href for q in found_qualities):
                                        found_qualities.append({
                                            "quality": pattern["quality"],
                                            "url": href,
                                            "size": size,
                                            "name": pattern["text"]
                                        })
                                        break
                
                logger.info(f"Found {len(found_qualities)} quality options via content parsing")
                
            # --- STEP 3: Resolve Final Download Links ---
            # Each quality link points to a download page, we need to extract the final video URL
            for quality_info in found_qualities:
                q_url = quality_info['url']
                q_quality = quality_info['quality']
                q_size = quality_info['size']
                
                try:
                    logger.info(f"Resolving {q_quality} quality link: {q_url[:60]}...")
                    
                    # Navigate to quality page to get final download link
                    quality_page = None
                    final_video_url = None
                    
                    try:
                        # Check if context is still valid
                        try:
                            quality_page = self.context.new_page()
                        except Exception as context_e:
                            logger.warning(f"Context error when creating page: {context_e}")
                            # Fallback: use quality URL directly
                            results.append(ExtractionResult(
                                video_url=q_url,
                                quality=q_quality,
                                server=f"Multi ({q_size})",
                                metadata={"size": q_size, "needs_resolution": True}
                            ))
                            continue
                        
                        try:
                            self.setup_page(quality_page)
                        except Exception as setup_e:
                            logger.debug(f"Setup page failed: {setup_e}")
                            # Continue anyway
                        
                        quality_page.goto(q_url, wait_until="domcontentloaded", timeout=20000)
                        quality_page.wait_for_timeout(2000)
                    
                        # Look for download button/link
                        download_selectors = [
                            "a:has-text('Download')",
                            "button:has-text('Download')",
                            "a:has-text('Download File')",
                            "a[href*='.mp4']",
                            "a.btn-primary",
                            "button.btn-primary"
                        ]
                        
                        for selector in download_selectors:
                            try:
                                dl_elem = quality_page.locator(selector).first
                                if dl_elem.count() > 0:
                                    # Check if it's a direct MP4 link
                                    if selector.endswith("a[href*='.mp4']"):
                                        final_video_url = dl_elem.get_attribute("href")
                                    else:
                                        # Get href from link or click button
                                        tag_name = dl_elem.evaluate("el => el.tagName")
                                        if tag_name == "A":
                                            href = dl_elem.get_attribute("href")
                                            if href and (".mp4" in href or href.startswith("http")):
                                                final_video_url = href
                                        else:
                                            # Try clicking button to get final URL
                                            try:
                                                with quality_page.expect_navigation(timeout=10000, wait_until="domcontentloaded"):
                                                    dl_elem.click()
                                                quality_page.wait_for_timeout(2000)
                                                # Check if we got redirected to video
                                                current_url = quality_page.url
                                                if ".mp4" in current_url or ".m3u8" in current_url:
                                                    final_video_url = current_url
                                                else:
                                                    # Try to extract video URL from page
                                                    final_video_url = self.extract_video_url(quality_page)
                                            except Exception as click_e:
                                                logger.debug(f"Click failed: {click_e}")
                                    
                                    if final_video_url:
                                        break
                            except Exception as selector_e:
                                logger.debug(f"Error with selector {selector}: {selector_e}")
                                continue
                        
                        # If still no video URL, try generic extraction
                        if not final_video_url:
                            final_video_url = self.extract_video_url(quality_page)
                        
                        # If still no video URL, check page URL
                        if not final_video_url:
                            current_url = quality_page.url
                            if ".mp4" in current_url or ".m3u8" in current_url:
                                final_video_url = current_url
                    except Exception as page_e:
                        logger.warning(f"Error processing quality page: {page_e}")
                    finally:
                        if quality_page:
                            try:
                                quality_page.close()
                            except:
                                pass
                    
                    if final_video_url:
                        results.append(ExtractionResult(
                            video_url=final_video_url,
                            quality=q_quality,
                            server=f"Multi ({q_size})",
                            metadata={"size": q_size}
                        ))
                        logger.info(f"✓ Extracted {q_quality} quality: {final_video_url[:60]}...")
                    else:
                        # Fallback: use quality URL directly
                        logger.warning(f"Could not extract final URL for {q_quality}, using quality URL")
                        results.append(ExtractionResult(
                            video_url=q_url,
                            quality=q_quality,
                            server=f"Multi ({q_size})",
                            metadata={"size": q_size, "needs_resolution": True}
                        ))
                except Exception as e:
                    logger.warning(f"Error resolving {q_quality} quality: {e}")
            
            # Fallback: If no qualities found, try generic extraction
            if not results:
                logger.info("No quality options found, trying generic extraction...")
                fallback_url = self.extract_video_url(page)
                if fallback_url:
                    results.append(ExtractionResult(
                        video_url=fallback_url,
                        quality="Auto",
                        server="Multi (Fallback)"
                    ))

            return results
            
        except Exception as e:
            logger.error(f"Error extracting from Multi Download server: {e}")
            return []
        finally:
            if should_close_page and page:
                try:
                    page.close()
                except:
                    pass
