"""
Ad blocking utilities for extractors
Blocks known ad networks to speed up loading and reduce clutter
"""

from playwright.sync_api import Page, Route
from typing import List

# Known ad network patterns
AD_DOMAINS = [
    "googleads",
    "googlesyndication",
    "doubleclick",
    "popads",
    "popads.net",
    "adsafeprotected",
    "adnxs",
    "adservice",
    "advertising.com",
    "adform",
    "adtech",
    "advertising",
]

def should_block_request(url: str) -> bool:
    """Check if a request URL should be blocked"""
    url_lower = url.lower()
    return any(domain in url_lower for domain in AD_DOMAINS)

def setup_ad_blocking(page: Page):
    """
    Setup request interception to block ad networks
    
    Args:
        page: Playwright Page object
    """
    def handle_route(route: Route):
        if should_block_request(route.request.url):
            route.abort()
        else:
            route.continue_()
    
    page.route("**/*", handle_route)

