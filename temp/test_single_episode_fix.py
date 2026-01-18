"""Test single episode to verify fixes"""
import sys
import os
import json
import logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

from backend.core.browser import BrowserManager
from backend.sites.egydead.scraper import EgyDeadScraper

# Test episode 1 which had multi-quality
episode_url = "https://x7k9f.sbs/episode/%d9%85%d8%b3%d9%84%d8%b3%d9%84-pluribus-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/"

scraper = EgyDeadScraper()

try:
    print("Testing Episode 1 with fixes...")
    result = scraper.get_episode_video_url(episode_url, include_metadata=True)
    
    if result:
        sources = result.get('sources', [])
        multi_sources = [s for s in sources if 'Multi' in s.get('server', '')]
        
        print(f"\nTotal sources: {len(sources)}")
        print(f"Multi-quality sources: {len(multi_sources)}")
        
        if multi_sources:
            print("\nMulti-quality sources found:")
            for s in multi_sources:
                print(f"  - {s.get('server')} ({s.get('quality')})")
        
        # Save result
        with open('episode1_fixed.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("\nSaved to episode1_fixed.json")
    else:
        print("No result returned")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    scraper.browser_manager.close()

