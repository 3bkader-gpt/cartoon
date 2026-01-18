"""Test MultiServerExtractor directly on hglink URL"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.core.browser import BrowserManager
from backend.extractors.factory import ExtractorFactory
import json

hglink_url = "https://hglink.to/setft11iyw7b"

browser_manager = BrowserManager()

try:
    print("="*70)
    print("Testing MultiServerExtractor directly on hglink URL")
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
            print(f"   URL: {res_dict.get('video_url', 'None')[:70]}...")
            if res_dict.get('metadata'):
                print(f"   Metadata: {res_dict.get('metadata')}")
            print()
        
        # Save results
        results_dict = [r.to_dict() if hasattr(r, 'to_dict') else r for r in results]
        with open('multi_direct_result.json', 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, ensure_ascii=False, indent=2)
        print(f"✓ Saved to multi_direct_result.json")
    else:
        print("\n✗ No results returned")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    browser_manager.close()

