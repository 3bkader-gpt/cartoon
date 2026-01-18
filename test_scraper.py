"""Quick test script to debug the scraper directly"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import directly to avoid relative import issues
print("=" * 60)
print("Testing Browser and Scraper...")
print("=" * 60)

try:
    print("1. Importing BrowserManager...")
    from core.browser import BrowserManager
    print("   ✅ BrowserManager imported")
    
    print("\n2. Creating browser manager...")
    bm = BrowserManager()
    print("   ✅ BrowserManager created")
    
    print("\n3. Getting browser context...")
    ctx = bm.get_context()
    print(f"   ✅ Context: {ctx}")
    
    print("\n4. Creating page...")
    page = ctx.new_page()
    print("   ✅ Page created")
    
    url = "https://www.arabic-toons.com/%D8%A3%D9%85%D9%8A-%D9%86%D8%A8%D8%B9-%D8%A7%D9%84%D8%AD%D9%86%D8%A7%D9%86-1446454962-anime-streaming.html"
    print(f"\n5. Navigating to: {url[:60]}...")
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    print("   ✅ Navigation complete")
    
    print("\n6. Waiting 2 seconds...")
    page.wait_for_timeout(2000)
    
    print("\n7. Looking for links...")
    links = page.locator("a[href*='.html']")
    count = links.count()
    print(f"   📊 Found {count} links")
    
    print("\n8. First 10 links:")
    for i in range(min(10, count)):
        try:
            href = links.nth(i).get_attribute("href")
            text = links.nth(i).inner_text()
            has_streaming = "anime-streaming" in (href or "")
            print(f"   [{i}] streaming={has_streaming} | {text[:30]} | {href[:50] if href else 'None'}...")
        except Exception as e:
            print(f"   [{i}] ERROR: {e}")
    
    print("\n9. Filtering episode links (no 'anime-streaming', has '.html')...")
    episode_links = []
    for i in range(min(count, 100)):
        try:
            href = links.nth(i).get_attribute("href")
            if href and "anime-streaming" not in href and ".html" in href:
                text = links.nth(i).inner_text()
                episode_links.append((text, href))
        except:
            pass
    
    print(f"   📋 Found {len(episode_links)} episode links")
    for i, (text, href) in enumerate(episode_links[:5]):
        print(f"   Episode {i+1}: {text[:40]} -> {href[:50]}...")
    
    page.close()
    bm.close()
    print("\n✅ All tests passed!")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
