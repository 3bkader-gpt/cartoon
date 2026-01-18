"""Full test of episode 6 to see all sources and qualities"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.core.browser import BrowserManager
from backend.sites.egydead.scraper import EgyDeadScraper
import json

episode_url = "https://x7k9f.sbs/episode/%d9%85%d8%b3%d9%84%d8%b3%d9%84-the-witcher-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%b1%d8%a7%d8%a8%d8%b9-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-6-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/"

scraper = EgyDeadScraper()

try:
    print("="*70)
    print("Testing Episode 6 - Full Extraction")
    print("="*70)
    print(f"\nEpisode URL: {episode_url}\n")
    
    result = scraper.get_episode_video_url(episode_url, include_metadata=True)
    
    if result:
        print("\n" + "="*70)
        print("RESULTS")
        print("="*70)
        
        if isinstance(result, dict):
            video_url = result.get('video_url')
            sources = result.get('sources', [])
            
            print(f"\nPrimary Video URL: {video_url[:80] if video_url else 'None'}...")
            print(f"\nTotal Sources Found: {len(sources)}")
            
            if sources:
                print("\n" + "-"*70)
                print("SOURCES BREAKDOWN")
                print("-"*70)
                
                multi_sources = []
                single_sources = []
                
                for i, source in enumerate(sources, 1):
                    server = source.get('server', 'Unknown')
                    quality = source.get('quality', 'Unknown')
                    source_type = source.get('type', 'unknown')
                    url = source.get('url', '')
                    
                    is_multi = 'Multi' in server or quality in ['1080p', '720p', '480p', '360p']
                    
                    print(f"\n{i}. {server}")
                    print(f"   Quality: {quality}")
                    print(f"   Type: {source_type}")
                    print(f"   URL: {url[:70]}...")
                    
                    if is_multi:
                        multi_sources.append(source)
                        print(f"   ⭐ MULTI SERVER - Multiple qualities available!")
                    else:
                        single_sources.append(source)
                
                print("\n" + "="*70)
                print("SUMMARY")
                print("="*70)
                print(f"\nMulti Server Sources: {len(multi_sources)}")
                if multi_sources:
                    print("  These sources provide multiple quality options:")
                    for s in multi_sources:
                        print(f"    - {s.get('server')} ({s.get('quality')})")
                
                print(f"\nSingle Quality Sources: {len(single_sources)}")
                if single_sources:
                    for s in single_sources:
                        print(f"    - {s.get('server')} ({s.get('quality')})")
                
                # Check if MultiServerExtractor was used
                multi_qualities = [s for s in sources if s.get('quality') in ['1080p', '720p', '480p', '360p']]
                if multi_qualities:
                    print(f"\n✅ SUCCESS: Found {len(multi_qualities)} quality options from Multi Server!")
                    print("   Qualities available:")
                    for q in ['1080p', '720p', '480p', '360p']:
                        found = [s for s in multi_qualities if s.get('quality') == q]
                        if found:
                            print(f"     ✓ {q} - {found[0].get('server', 'Unknown')}")
            else:
                print("\n⚠ No sources found")
        else:
            print(f"\nResult: {result}")
        
        # Save to file
        with open('episode6_result.json', 'w', encoding='utf-8') as f:
            if isinstance(result, dict):
                json.dump(result, f, ensure_ascii=False, indent=2)
            else:
                json.dump({"video_url": result}, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Saved full result to episode6_result.json")
        
    else:
        print("\n✗ No result returned")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    scraper.browser_manager.close()

