"""
Popup handling utilities for extractors
Auto-closes popups and new tabs opened by ad networks
"""

from playwright.sync_api import BrowserContext
import logging

logger = logging.getLogger(__name__)

def setup_popup_handler(context: BrowserContext):
    """
    Setup automatic popup/tab closing for aggressive ad popups
    
    Args:
        context: Playwright BrowserContext object
    """
    def handle_popup(page):
        """Auto-close popups that open in new tabs"""
        try:
            logger.debug(f"Auto-closing popup: {page.url}")
            page.close()
        except Exception as e:
            logger.warning(f"Error closing popup: {e}")
    
    context.on("page", handle_popup)

