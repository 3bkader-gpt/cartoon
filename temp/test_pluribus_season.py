"""Test extracting all episodes from Pluribus season page"""
import sys
import os
import json
import logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from backend.core.browser import BrowserManager
from backend.sites.egydead.scraper import EgyDeadScraper

season_url = "https://x7k9f.sbs/season/%d9%85%d8%b3%d9%84%d8%b3%d9%84-pluribus-2025-%d9%85%d8%aa%d8%b1%d8%ac%d9%85-%d9%83%d8%a7%d9%85%d9%84/"

scraper = EgyDeadScraper()

try:
    print("="*70)
    print("Extracting All Episodes from Pluribus Season")
    print("="*70)
    print(f"\nSeason URL: {season_url}\n")
    
    # Get all episodes
    print("Step 1: Getting episode list...")
    episodes = scraper.get_series_episodes(season_url)
    
    print(f"\n✓ Found {len(episodes)} episodes\n")
    
    # Display episodes
    for i, ep in enumerate(episodes, 1):
        print(f"{i}. {ep.get('title', 'Unknown')}")
        print(f"   URL: {ep.get('episode_url', 'N/A')[:70]}...")
        print(f"   Season: {ep.get('season', 'N/A')}, Episode: {ep.get('episode', 'N/A')}")
        print()
    
    # Extract video URLs for all episodes
    print("\n" + "="*70)
    print("Step 2: Extracting video URLs for all episodes...")
    print("="*70)
    
    results = []
    for i, ep in enumerate(episodes, 1):
        ep_url = ep.get('episode_url')
        if not ep_url:
            continue
        
        print(f"\n[{i}/{len(episodes)}] Processing: {ep.get('title', 'Unknown')}")
        print(f"URL: {ep_url[:70]}...")
        
        try:
            result = scraper.get_episode_video_url(ep_url, include_metadata=True)
            
            if result:
                sources = result.get('sources', [])
                video_url = result.get('video_url')
                
                # Count multi-quality sources
                multi_sources = [s for s in sources if 'Multi' in s.get('server', '') or isinstance(s.get('metadata', {}).get('qualities'), list)]
                
                print(f"  ✓ Found {len(sources)} sources")
                if video_url:
                    print(f"  ✓ Primary video URL: {video_url[:60]}...")
                if multi_sources:
                    print(f"  ⭐ {len(multi_sources)} multi-quality source(s)")
                
                # Add episode info to result
                result['episode_info'] = ep
                results.append(result)
            else:
                print(f"  ✗ No result returned")
                results.append({
                    'episode_info': ep,
                    'video_url': None,
                    'sources': [],
                    'error': 'No result returned'
                })
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
            results.append({
                'episode_info': ep,
                'video_url': None,
                'sources': [],
                'error': str(e)
            })
    
    # Save results
    output_file = 'pluribus_season_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"\nTotal Episodes: {len(episodes)}")
    print(f"Successfully Extracted: {sum(1 for r in results if r.get('video_url'))}")
    print(f"Failed: {sum(1 for r in results if not r.get('video_url'))}")
    
    # Count multi-quality sources
    total_multi = 0
    for r in results:
        sources = r.get('sources', [])
        multi = [s for s in sources if 'Multi' in s.get('server', '')]
        total_multi += len(multi)
    
    if total_multi > 0:
        print(f"\n⭐ Total Multi-Quality Sources Found: {total_multi}")
    
    print(f"\n✓ Results saved to: {output_file}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    scraper.browser_manager.close()

