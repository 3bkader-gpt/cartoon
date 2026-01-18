"""Test episode 6 with detailed logging"""
import sys
import os
import logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from backend.core.browser import BrowserManager
from backend.sites.egydead.scraper import EgyDeadScraper
import json

episode_url = "https://x7k9f.sbs/episode/%d9%85%d8%b3%d9%84%d8%b3%d9%84-the-witcher-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%b1%d8%a7%d8%a8%d8%b9-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-6-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/"

scraper = EgyDeadScraper()

try:
    print("="*70)
    print("Testing Episode 6 with Detailed Logging")
    print("="*70)
    print(f"\nEpisode URL: {episode_url}\n")
    
    result = scraper.get_episode_video_url(episode_url, include_metadata=True)
    
    if result:
        print("\n" + "="*70)
        print("RESULTS")
        print("="*70)
        
        if isinstance(result, dict):
            sources = result.get('sources', [])
            
            print(f"\nTotal Sources Found: {len(sources)}")
            
            # Check for Multi Download
            multi_sources = [s for s in sources if 'Multi' in s.get('server', '') or 'hglink' in s.get('url', '')]
            
            if multi_sources:
                print(f"\n✅ Found {len(multi_sources)} Multi Download sources:")
                for s in multi_sources:
                    print(f"  - {s.get('server')} ({s.get('quality')})")
                    print(f"    URL: {s.get('url')[:70]}...")
            else:
                print("\n⚠ No Multi Download sources found")
                print("\nAll sources:")
                for i, s in enumerate(sources, 1):
                    print(f"  {i}. {s.get('server')} ({s.get('quality')}) - {s.get('url')[:60]}...")
        
        # Save to file
        with open('episode6_with_logs.json', 'w', encoding='utf-8') as f:
            if isinstance(result, dict):
                json.dump(result, f, ensure_ascii=False, indent=2)
            else:
                json.dump({"video_url": result}, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Saved to episode6_with_logs.json")
        
    else:
        print("\n✗ No result returned")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    scraper.browser_manager.close()

