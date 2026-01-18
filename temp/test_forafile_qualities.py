"""Test Forafile link to see if it has multiple qualities"""
from playwright.sync_api import sync_playwright
import json

forafile_url = "https://forafile.com/wkpju6ulvnd3/The.Witcher.S04E01.EgyDead.CoM.mp4.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    page = context.new_page()
    
    try:
        print(f"Opening Forafile: {forafile_url}")
        page.goto(forafile_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)
        
        print(f"\nCurrent URL: {page.url}")
        
        # Check for download button and click
        download_btn = page.locator("#downloadbtn")
        if download_btn.count() > 0 and download_btn.is_visible():
            print("✓ Found #downloadbtn, clicking...")
            try:
                with page.expect_navigation(timeout=60000, wait_until="domcontentloaded"):
                    download_btn.click()
                print(f"✓ Navigated to: {page.url}")
                page.wait_for_timeout(2000)
            except Exception as e:
                print(f"⚠ Navigation error: {e}")
        
        # Check for quality options
        print("\n=== Checking for Quality Options ===")
        
        # Look for quality links
        quality_patterns = [
            "1080p", "720p", "480p", "360p", "240p",
            "Full HD", "HD", "SD", "Low Quality",
            "1080", "720", "480", "360"
        ]
        
        all_links = page.evaluate("""
            () => {
                return Array.from(document.querySelectorAll('a')).map(a => ({
                    href: a.href,
                    text: a.innerText.trim(),
                    title: a.title || ''
                }));
            }
        """)
        
        quality_links = []
        for link in all_links:
            text = (link['text'] + " " + link['title']).lower()
            for pattern in quality_patterns:
                if pattern.lower() in text:
                    if not any(q['url'] == link['href'] for q in quality_links):
                        quality_links.append({
                            "text": link['text'],
                            "url": link['href'],
                            "pattern": pattern
                        })
                        break
        
        if quality_links:
            print(f"\nFound {len(quality_links)} quality links:")
            for q in quality_links:
                print(f"  - {q['text']} ({q['pattern']})")
                print(f"    URL: {q['url'][:70]}...")
        else:
            print("✗ No quality links found")
        
        # Check for video tag
        video_url = page.evaluate("""
            () => {
                const video = document.querySelector('video');
                if (video) return video.src || video.currentSrc;
                return null;
            }
        """)
        
        if video_url:
            print(f"\n✓ Found direct video URL: {video_url[:70]}...")
        
        # Check for iframe
        iframe = page.locator('iframe').first
        if iframe.count() > 0:
            src = iframe.get_attribute("src")
            if src:
                print(f"\n✓ Found iframe: {src[:70]}...")
        
        results = {
            "forafile_url": forafile_url,
            "final_url": page.url,
            "quality_links": quality_links,
            "video_url": video_url,
            "has_video_tag": video_url is not None
        }
        
        with open('forafile_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Saved to forafile_analysis.json")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        page.close()
        browser.close()

