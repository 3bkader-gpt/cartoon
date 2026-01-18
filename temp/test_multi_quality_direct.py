"""Test Multi-Quality link directly to verify it works"""
from playwright.sync_api import sync_playwright
import json

# Test one quality link from It Welcome to Derry S01E03
quality_url = "https://cavanhabg.com/f/myb3dkhva628_h"  # 1080p

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    page = context.new_page()
    
    try:
        print(f"Testing Multi-Quality link: {quality_url}\n")
        print("This should redirect to the final video URL...\n")
        
        page.goto(quality_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)
        
        print(f"Current URL after redirect: {page.url}\n")
        
        # Check if we got a video URL
        if ".mp4" in page.url or ".m3u8" in page.url:
            print("✅ SUCCESS: Link redirects directly to video!")
            print(f"Video URL: {page.url}")
        else:
            print("⚠️ Link doesn't redirect directly to video")
            print("Checking for download button...")
            
            # Look for download button
            download_btn = page.locator("a:has-text('Download'), button:has-text('Download')").first
            if download_btn.count() > 0:
                print(f"Found download button: {download_btn.inner_text()}")
                href = download_btn.get_attribute("href")
                if href:
                    print(f"Download link: {href}")
            else:
                # Check page content
                content = page.evaluate("() => document.body.innerText")
                print(f"\nPage content preview:\n{content[:500]}")
        
        # Save screenshot
        page.screenshot(path="multi_quality_test.png")
        print("\n✓ Screenshot saved to multi_quality_test.png")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        page.close()
        browser.close()

