"""
EgyDead Configuration
Domain: egydead.skin
Content: Series, Movies, Anime
"""

SITE_NAME = "EgyDead"
BASE_URL = "https://egydead.skin"
SUPPORTED_PATTERNS = ["egydead.skin", "egydead.live", "x7k9f.sbs"]

# URL Patterns
SEASON_PATTERN = "/season/"
EPISODE_PATTERN = "/episode/"

# Selectors
SELECTORS = {
    "episode_links": ".EpsList li a",
    "episode_title": "h1.TitleMaster span em",
    "poster": ".single-thumbnail img",
    "iframe": "iframe.metaframe",
    "download_button": "div.watchNow button",
    "video_source": "video source",
}

# Request Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://egydead.skin/"
}
