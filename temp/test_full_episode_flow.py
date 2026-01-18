"""Full test of episode page to find all servers and qualities"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from core.browser import BrowserManager
from sites.egydead.scraper import EgyDeadScraper
import json

episode_url = "https://x7k9f.sbs/episode/%d9%85%d8%b3%d9%84%d8%b3%d9%84-the-witcher-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%b1%d8%a7%d8%a8%d8%b9-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/"

scraper = EgyDeadScraper()

try:
    print(f"Testing episode: {episode_url}\n")
    result = scraper.get_episode_video_url(episode_url, include_metadata=True)
    
    if result:
        print("\n=== RESULT ===")
        if isinstance(result, dict):
            print(f"Video URL: {result.get('video_url', 'None')}")
            print(f"Sources count: {len(result.get('sources', []))}")
            
            sources = result.get('sources', [])
            if sources:
                print(f"\n=== SOURCES ({len(sources)} total) ===")
                for i, source in enumerate(sources, 1):
                    print(f"\n{i}. {source.get('server', 'Unknown')}")
                    print(f"   Quality: {source.get('quality', 'Unknown')}")
                    print(f"   Type: {source.get('type', 'unknown')}")
                    print(f"   URL: {source.get('url', '')[:70]}...")
                    
                    # Check if it's a Multi server result
                    if source.get('type') == 'direct' and 'Multi' in source.get('server', ''):
                        print(f"   ⭐ MULTI SERVER - Multiple qualities available!")
            else:
                print("No sources found")
        else:
            print(f"Result: {result}")
        
        # Save to file
        with open('episode_result.json', 'w', encoding='utf-8') as f:
            if isinstance(result, dict):
                json.dump(result, f, ensure_ascii=False, indent=2)
            else:
                json.dump({"video_url": result}, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Saved to episode_result.json")
    else:
        print("✗ No result returned")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    scraper.browser_manager.close()

