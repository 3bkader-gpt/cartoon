"""Test cavanhabg.com page directly to see quality options"""
from playwright.sync_api import sync_playwright
import json

cavanhabg_url = "https://cavanhabg.com/f/setft11iyw7b"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    page = context.new_page()
    
    try:
        print(f"Opening: {cavanhabg_url}\n")
        page.goto(cavanhabg_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)
        
        print(f"Current URL: {page.url}\n")
        
        # Get page content
        page_text = page.evaluate("() => document.body.innerText")
        print("Page content preview:")
        print(page_text[:1000])
        print("\n" + "="*70)
        
        # Get all links
        all_links = page.evaluate("""
            () => {
                return Array.from(document.querySelectorAll('a')).map(a => ({
                    href: a.href,
                    text: a.innerText.trim(),
                    parentText: a.parentElement ? a.parentElement.innerText.trim() : '',
                    fullText: a.parentElement ? a.parentElement.innerText.trim() : a.innerText.trim()
                }));
            }
        """)
        
        print(f"\nFound {len(all_links)} total links\n")
        
        # Find quality-related links
        quality_links = []
        for link in all_links:
            full_text = link['fullText'].lower()
            if any(keyword in full_text for keyword in ['full hd', 'hd quality', 'normal quality', '1920', '1440', '960', 'click to download']):
                quality_links.append(link)
                print(f"Quality link found:")
                print(f"  Text: {link['text']}")
                print(f"  Full Text: {link['fullText'][:100]}...")
                print(f"  URL: {link['href']}")
                print()
        
        # Save results
        results = {
            "url": page.url,
            "total_links": len(all_links),
            "quality_links": quality_links,
            "page_text_preview": page_text[:500]
        }
        
        with open('cavanhabg_direct.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"✓ Saved to cavanhabg_direct.json")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        page.close()
        browser.close()

