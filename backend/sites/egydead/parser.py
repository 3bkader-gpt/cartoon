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
        """Extract metadata from page"""
        try:
            return page.evaluate("""
                () => {
                    const h1 = document.querySelector('h1, .entry-title')?.innerText || '';
                    const title = document.title;
                    
                    // Get poster/thumbnail
                    let thumbnail = document.querySelector('meta[property="og:image"]')?.content || '';
                    if (!thumbnail) {
                        thumbnail = document.querySelector('.poster img, img.thumbnail')?.src || '';
                    }
                    
                    return { h1, title, thumbnail };
                }
            """)
        except:
            return {"h1": "", "title": "", "thumbnail": ""}

    @staticmethod
    def parse_episode_url(episode_url: str) -> Dict:
        """
        Extract info from episode URL
        Example: /episode/مسلسل-tulsa-king-الموسم-الثالث-الحلقة-10-مترجمة/
        """
        # Decode URL
        decoded = unquote(episode_url)
        
        # Extract parts
        parts = decoded.split('/')[-1].replace('.html', '').split('-')
        
        # Try to find season and episode numbers
        season = None
        episode = None
        
        for i, part in enumerate(parts):
            if 'الموسم' in part or 'season' in part.lower():
                # Next part might be the season number
                if i + 1 < len(parts):
                    season_match = re.search(r'\d+', parts[i + 1])
                    if season_match:
                        season = season_match.group()
            
            if 'الحلقة' in part or 'episode' in part.lower():
                # Next part might be the episode number
                if i + 1 < len(parts):
                    episode_match = re.search(r'\d+', parts[i + 1])
                    if episode_match:
                        episode = episode_match.group()
        
        # Extract series name (first few parts before season/episode)
        series_parts = []
        for part in parts:
            if any(keyword in part for keyword in ['الموسم', 'الحلقة', 'season', 'episode', 'مترجم', 'مترجمة']):
                break
            series_parts.append(part)
        
        series_name = ' '.join(series_parts).strip()
        
        return {
            "episode_url": episode_url,
            "series_name": series_name,
            "season": season,
            "episode": episode,
            "title": decoded.split('/')[-1]
        }

    @staticmethod
    def parse_video_url(video_url: str) -> Dict:
        """Parse video URL to extract info"""
        parsed = urlparse(video_url)
        
        return {
            "full_url": video_url,
            "domain": parsed.netloc,
            "path": parsed.path,
            "filename": parsed.path.split('/')[-1] if parsed.path else None
        }

    @staticmethod
    def extract_episode_number(title: str) -> int:
        """Extract episode number from title"""
        # Try to find episode number
        match = re.search(r'(?:الحلقة|episode|ep|e)\s*(\d+)', title, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        # Fallback: find any number
        match = re.search(r'\d+', title)
        if match:
            return int(match.group())
        
        return 0
