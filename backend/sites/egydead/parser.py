"""
EgyDead Parser
Extracts metadata and parses URLs
"""

import re
from typing import Dict
from urllib.parse import urlparse, unquote

class EgyDeadParser:
    """Parses HTML/Data for EgyDead"""

    @staticmethod
    def get_page_metadata(page) -> Dict:
        """Extract metadata from page using Playwright"""
        try:
            return page.evaluate("""
                () => {
                    const h1 = document.querySelector('h1.entry-title, h1')?.innerText || '';
                    const title = document.title;
                    let thumbnail = document.querySelector('div.postThumbnail img')?.src || '';
                    if (!thumbnail) thumbnail = document.querySelector('meta[property="og:image"]')?.content || '';
                    
                    return { h1, title, thumbnail };
                }
            """)
        except Exception:
            return {"h1": "", "title": "", "thumbnail": ""}

    @staticmethod
    def parse_episode_url(episode_url: str) -> Dict:
        """
        Extract info from episode URL
        Example: /episode/مسلسل-bel-air-الموسم-الرابع-الحلقة-1-مترجمة/
        """
        try:
            # Decode URL
            decoded = unquote(episode_url)
            slug = decoded.split('/')[-1] if decoded.split('/')[-1] else decoded.split('/')[-2]
            
            # Extract numbers
            numbers = re.findall(r'\d+', slug)
            
            season = None
            episode = None
            
            # Try to identify season and episode from slug structure
            # Usually: series-name-season-X-episode-Y
            
            if 'الموسم' in slug:
                season_match = re.search(r'الموسم[-_ ]?(\d+)', slug)
                if season_match:
                    season = season_match.group(1)
            
            if 'الحلقة' in slug:
                episode_match = re.search(r'الحلقة[-_ ]?(\d+)', slug)
                if episode_match:
                    episode = episode_match.group(1)
            
            # Fallback if specific keywords not found but numbers exist
            if not season and not episode and len(numbers) >= 2:
                # Assuming last number is episode, second to last is season
                episode = numbers[-1]
                season = numbers[-2]
            elif not episode and numbers:
                episode = numbers[-1]

            return {
                "episode_url": episode_url,
                "season": season,
                "episode": episode,
                "title": slug.replace('-', ' ').strip()
            }
        except Exception:
            return {
                "episode_url": episode_url,
                "season": None,
                "episode": None,
                "title": "Unknown Episode"
            }

    @staticmethod
    def parse_video_url(video_url: str) -> Dict:
        """Parse video URL to extract info"""
        try:
            parsed = urlparse(video_url)
            filename = parsed.path.split('/')[-1] if parsed.path else "video.mp4"
            
            return {
                "full_url": video_url,
                "domain": parsed.netloc,
                "filename": filename,
                "extension": filename.split('.')[-1] if '.' in filename else "mp4"
            }
        except Exception:
            return {"full_url": video_url, "filename": "video.mp4"}
