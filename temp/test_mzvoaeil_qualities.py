"""Test the redirect link to see if it has multiple qualities"""
from playwright.sync_api import sync_playwright
import json
import time

redirect_url = "https://mzvoaeil.pro/?p=303ed4jer4keksk3jdfefgy6o8dje3jhyejrdkek3463fg8jfks73050&en=1087"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    page = context.new_page()
    
    try:
        print(f"Opening redirect URL: {redirect_url}")
        page.goto(redirect_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(5000)  # Wait for redirects
        
        print(f"\nCurrent URL after redirects: {page.url}")
        
        # Check for "Create Download Link" button
        create_link_btn = page.locator("button:has-text('Create Download Link'), a:has-text('Create Download Link')")
        if create_link_btn.count() > 0:
            print("✓ Found 'Create Download Link' button")
            try:
                with page.expect_navigation(timeout=15000, wait_until="domcontentloaded"):
                    create_link_btn.first.click()
                print(f"✓ Clicked, navigated to: {page.url}")
                page.wait_for_timeout(3000)
            except Exception as e:
                print(f"⚠ Navigation error: {e}")
        
        # Check for quality options
        print("\n=== Checking for Quality Options ===")
        
        # Get all links and check for quality indicators
        all_links = page.evaluate("""
            () => {
                return Array.from(document.querySelectorAll('a')).map(a => ({
                    href: a.href,
                    text: a.innerText.trim(),
                    title: a.title || ''
                }));
            }
        """)
        
        quality_keywords = ["1080p", "720p", "480p", "360p", "240p", "Full HD", "HD", "SD", "Low Quality", "1080", "720", "480", "360"]
        quality_links = []
        
        for link in all_links:
            text = (link['text'] + " " + link['title']).lower()
            for keyword in quality_keywords:
                if keyword.lower() in text:
                    if not any(q['url'] == link['href'] for q in quality_links):
                        quality_links.append({
                            "text": link['text'],
                            "url": link['href'],
                            "keyword": keyword
                        })
                        break
        
        if quality_links:
            print(f"\n✓ Found {len(quality_links)} quality links:")
            for q in quality_links:
                print(f"  - {q['text']} ({q['keyword']})")
                print(f"    URL: {q['url'][:70]}...")
        else:
            print("✗ No quality links found")
            print("\nAll links on page:")
            for i, link in enumerate(all_links[:20]):  # Show first 20
                if link['text']:
                    print(f"  {i+1}. {link['text'][:50]} - {link['href'][:50]}...")
        
        # Check page content for quality indicators
        page_text = page.evaluate("() => document.body.innerText")
        if any(kw in page_text.lower() for kw in ["1080", "720", "480", "quality", "جودة"]):
            print("\n✓ Page contains quality-related text")
        
        # Check for download buttons
        download_buttons = page.locator("button:has-text('Download'), a:has-text('Download')")
        if download_buttons.count() > 0:
            print(f"\n✓ Found {download_buttons.count()} download button(s)")
        
        results = {
            "redirect_url": redirect_url,
            "final_url": page.url,
            "quality_links": quality_links,
            "total_links": len(all_links),
            "has_quality_text": any(kw in page_text.lower() for kw in ["1080", "720", "480", "quality"])
        }
        
        with open('mzvoaeil_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Saved to mzvoaeil_analysis.json")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        page.close()
        browser.close()

