"""Test Multi-Quality extraction with final URL resolution"""
import sys
import os
import logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

from backend.core.browser import BrowserManager
from backend.extractors.factory import ExtractorFactory

# Test URL from It Welcome to Derry S01E03
hglink_url = "https://hglink.to/myb3dkhva628"

browser_manager = BrowserManager()

try:
    print("="*70)
    print("Testing Multi-Quality Extraction with Final URL Resolution")
    print("="*70)
    print(f"\nURL: {hglink_url}\n")
    
    context = browser_manager.get_context()
    
    # Get extractor
    extractor = ExtractorFactory.get_extractor(hglink_url, context)
    print(f"Extractor: {extractor.__class__.__name__}\n")
    
    # Extract
    print("Extracting...")
    results = extractor.extract(hglink_url)
    
    if results:
        print(f"\n✓ Found {len(results)} quality options:\n")
        
        for i, result in enumerate(results, 1):
            if hasattr(result, 'to_dict'):
                res_dict = result.to_dict()
            else:
                res_dict = result
            
            print(f"{i}. Quality: {res_dict.get('quality', 'Unknown')}")
            print(f"   Server: {res_dict.get('server', 'Unknown')}")
            video_url = res_dict.get('video_url', 'None')
            print(f"   URL: {video_url[:70]}...")
            
            # Check if it's a direct video URL
            if video_url and (".mp4" in video_url or ".m3u8" in video_url):
                print(f"   ✅ Direct video URL!")
            elif res_dict.get('metadata', {}).get('needs_resolution'):
                print(f"   ⚠️ Needs resolution")
            else:
                print(f"   ⚠️ May need resolution")
            
            if res_dict.get('metadata'):
                print(f"   Metadata: {res_dict.get('metadata')}")
            print()
    else:
        print("\n✗ No results returned")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    browser_manager.close()

