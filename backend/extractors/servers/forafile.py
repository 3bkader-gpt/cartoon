"""
Forafile Extractor
Handles extraction of direct video links from Forafile server
"""

import logging
from typing import Optional
from playwright.sync_api import Page
from ..base import BaseExtractor, ExtractionResult

logger = logging.getLogger(__name__)

class ForafileExtractor(BaseExtractor):
    """
    Extractor for Forafile server
    
    Flow:
    1. Navigate to Forafile URL
    2. Click #download overlay (triggers popup)
    3. Close popup immediately
    4. Click #downloadbtn button
    5. Wait for navigation to video player
    6. Extract video URL
    """
    
    def extract(self, url: str, page: Optional[Page] = None) -> ExtractionResult:
        """
        Extract direct video link from Forafile URL
        
        Args:
            url: Forafile server URL
            page: Optional existing page
            
        Returns:
            ExtractionResult with video_url, quality, server, and metadata
        """
        should_close_page = False
        if not page:
            try:
                page = self.context.new_page()
                should_close_page = True
                logger.info(f"Extracting from Forafile (New Page): {url}")
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
            except Exception as e:
                logger.error(f"Failed to create/navigate page: {e}")
                return None
        else:
            logger.info(f"Extracting from Forafile (Existing Page): {url}")
            # Ensure we are on the right URL if using existing page
            if page.url != url:
                 try:
                     page.goto(url, wait_until="domcontentloaded", timeout=30000)
                 except Exception:
                     pass # Maybe already there or redirect happened
        
        try:
            self.setup_page(page)
            
            # Handle potential overlay/popup
            # Forafile often has an overlay that triggers a popup on first click
            overlay = page.locator("#download")
            if overlay.is_visible():
                logger.info("Handling Forafile overlay...")
                try:
                    with self.context.expect_page(timeout=5000) as popup_info:
                        overlay.click()
                    
                    # Close the popup that opens
                    popup = popup_info.value
                    popup.close()
                    logger.debug("Closed Forafile popup")
                except Exception as e:
                    logger.debug(f"No popup opened or popup handling failed: {e}")
                
                # Small wait for UI update
                page.wait_for_timeout(1000)
            
            # Click download button
            download_btn = page.locator("#downloadbtn")
            if download_btn.is_visible():
                logger.info("Clicking Forafile download button...")
                try:
                    with page.expect_navigation(timeout=60000, wait_until="domcontentloaded"):
                        download_btn.click()
                    
                    # Wait for page to stabilize
                    page.wait_for_load_state("domcontentloaded")
                    page.wait_for_timeout(1000)
                except Exception as e:
                    logger.warning(f"Navigation after download button click failed: {e}")
            
            # Extract video URL
            video_url = self.extract_video_url(page)
            
            if not video_url:
                logger.warning("Could not extract video URL from Forafile")
                return ExtractionResult(
                    video_url=None,
                    quality="Unknown",
                    server="Forafile",
                    metadata={}
                )
            
            logger.info(f"Successfully extracted Forafile video URL")
            return ExtractionResult(
                video_url=video_url,
                quality="Auto",
                server="Forafile",
                metadata={}
            )
            
        except Exception as e:
            logger.error(f"Error extracting from Forafile: {e}")
            return ExtractionResult(
                video_url=None,
                quality="Unknown",
                server="Forafile",
                metadata={"error": str(e)}
            )
        finally:
            if should_close_page and page:
                try:
                    page.close()
                except:
                    pass

