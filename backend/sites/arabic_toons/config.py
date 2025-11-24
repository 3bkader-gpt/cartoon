SITE_NAME = "Arabic Toons"
BASE_URL = "https://www.arabic-toons.com"
CDN_BASE = "https://stream.foupix.com/animeios2_4"
SUPPORTED_PATTERNS = ["arabic-toons.com"]

# Selectors
SELECTORS = {
    "series_link": "a[href*='.html']",
    "video_element": "video",
    "search_link": 'link[name="مسلسلات"]',
    "grid_items": ['.anime-card', '.movie_poster', '.video-card', '.col-md-2', '.item', '.movie-item']
}
