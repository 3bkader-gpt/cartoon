import re
from typing import Dict, Optional, List
from urllib.parse import urlparse, parse_qs
from .config import BASE_URL

class ArabicToonsParser:
    """Parses HTML/Data for Arabic Toons"""

    @staticmethod
    def get_page_metadata(page) -> Dict:
        """Extract metadata from page using JS evaluation"""
        try:
            return page.evaluate("""
                () => {
                    const h1 = document.querySelector('h1')?.innerText || '';
                    const breadcrumbs = Array.from(document.querySelectorAll('.breadcrumb li, .breadcrumb a')).map(el => el.innerText);
                    const title = document.title;
                    let thumbnail = document.querySelector('meta[property="og:image"]')?.content || '';
                    if (!thumbnail) thumbnail = document.querySelector('.poster img, .anime-poster img, img[class*="poster"]')?.src || '';
                    if (!thumbnail) thumbnail = document.querySelector('img')?.src || '';
                    return { h1, breadcrumbs, title, thumbnail };
                }
            """)
        except:
            return {"h1": "", "breadcrumbs": [], "title": "", "thumbnail": ""}

    @staticmethod
    def parse_video_url(video_url: str) -> Dict:
        """Parse video URL to extract series/episode info"""
        parsed = urlparse(video_url)
        params = parse_qs(parsed.query)
        path_parts = parsed.path.strip('/').split('/')
        series_id = path_parts[-2] if len(path_parts) >= 2 else None
        filename = path_parts[-1] if path_parts else None
        
        series_name = season = episode = None
        if filename:
            match1 = re.match(r'(.+?)_s(\d+)_(\d+)\.mp4', filename)
            if match1:
                series_name, season, episode = match1.groups()
            else:
                match2 = re.match(r'(\d+)_(\d+)\.mp4', filename)
                if match2:
                    episode = match2.group(2)
        
        return {
            "full_url": video_url,
            "base_url": f"{parsed.scheme}://{parsed.netloc}{'/'.join(path_parts[:-1])}",
            "series_id": series_id,
            "filename": filename,
            "series_name": series_name,
            "season": season,
            "episode": episode,
            "parameters": {k: v[0] for k, v in params.items()}
        }

    @staticmethod
    def get_episode_info(episode_url: str) -> Dict:
        """Extract info from episode URL"""
        parts = episode_url.split('/')[-1].replace('.html', '').split('-')
        return {
            "episode_url": episode_url,
            "series_slug": '-'.join(parts[:-2]) if len(parts) >= 2 else None,
            "series_id": parts[-2] if len(parts) >= 2 else None,
            "episode_id": parts[-1] if parts else None
        }
