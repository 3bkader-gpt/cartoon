"""
EgyDead Configuration
Domain: egydead.skin
Content: Series, Movies, Anime, Cartoons
"""

SITE_NAME = "EgyDead"
BASE_URL = "https://egydead.skin"
SUPPORTED_PATTERNS = ["egydead.skin", "egydead."]

# URL Patterns
SEASON_PATTERN = "/season/"
EPISODE_PATTERN = "/episode/"
SERIE_PATTERN = "/serie/"

# Selectors
SELECTORS = {
    "episode_links": "a[href*='/episode/']",
    "video_iframe": "iframe[src*='embed']",
    "download_links": "a[href*='.mp4'], a[href*='download']",
    "poster": "meta[property='og:image'], .poster img, img.thumbnail",
    "title": "h1, .entry-title",
}

# Quality options (if available)
QUALITIES = ["1080p", "720p", "480p", "360p"]
