"""Find Multi Download server in episode page"""
from playwright.sync_api import sync_playwright
import json

episode_url = "https://x7k9f.sbs/episode/%d9%85%d8%b3%d9%84%d8%b3%d9%84-the-witcher-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%b1%d8%a7%d8%a8%d8%b9-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    page = context.new_page()
    
    try:
        print(f"Opening: {episode_url}\n")
        page.goto(episode_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(2000)
        
        # First, click Watch Now button to reveal download list
        print("=== Step 1: Clicking Watch Now ===")
        download_btn = page.locator("div.watchNow button").first
        if download_btn.count() > 0:
            print("✓ Found Watch Now button, clicking...")
            try:
                with page.expect_navigation(wait_until="domcontentloaded", timeout=10000):
                    download_btn.click()
                print(f"✓ Navigated to: {page.url}")
                page.wait_for_timeout(3000)  # Wait for content to load
            except Exception as e:
                print(f"⚠ Navigation: {e}")
        else:
            print("✗ Watch Now button not found")
        
        # Look for "تحميل متعدد" using the specific selector
        print("\n=== Step 2: Looking for 'تحميل متعدد' ===")
        
        # Method 1: Find by span.ser-name
        ser_name_spans = page.locator("span.ser-name")
        count = ser_name_spans.count()
        print(f"Found {count} elements with class 'ser-name'")
        
        multi_download_found = False
        multi_download_url = None
        
        for i in range(count):
            try:
                span = ser_name_spans.nth(i)
                text = span.inner_text()
                print(f"  {i+1}. Text: {text}")
                
                if "تحميل متعدد" in text or "Multi" in text or "multi" in text.lower():
                    print(f"     ✓ FOUND 'تحميل متعدد'!")
                    multi_download_found = True
                    
                    # Find the parent element that contains the link
                    # Usually structure is: <li><span class="ser-name">...</span><em>...</em><a href="...">
                    parent = span.locator("..")  # Parent element
                    
                    # Try to find link in parent
                    link = parent.locator("a").first
                    if link.count() > 0:
                        href = link.get_attribute("href")
                        if href:
                            multi_download_url = href
                            print(f"     URL: {href}")
                            
                            # Also get quality if available
                            em = parent.locator("em").first
                            quality_text = em.inner_text() if em.count() > 0 else "Unknown"
                            print(f"     Quality: {quality_text}")
                    else:
                        # Try finding link in next sibling or parent's parent
                        grandparent = parent.locator("..")
                        link = grandparent.locator("a").first
                        if link.count() > 0:
                            href = link.get_attribute("href")
                            if href:
                                multi_download_url = href
                                print(f"     URL (from grandparent): {href}")
            except Exception as e:
                print(f"  Error reading span {i}: {e}")
        
        # Method 2: Find by text content
        if not multi_download_found:
            print("\n=== Trying text-based search ===")
            multi_link = page.locator("text=تحميل متعدد").first
            if multi_link.count() > 0:
                print("✓ Found by text search")
                # Find parent with link
                parent = multi_link.locator("..")
                link = parent.locator("a").first
                if link.count() == 0:
                    parent = parent.locator("..")
                    link = parent.locator("a").first
                if link.count() > 0:
                    multi_download_url = link.get_attribute("href")
                    print(f"URL: {multi_download_url}")
        
        # Method 3: Get all download links and check their structure
        print("\n=== Checking Download List Structure ===")
        download_list = page.locator(".DownloadList li, ul.downloads li, .dls_table tbody tr")
        if download_list.count() > 0:
            print(f"Found {download_list.count()} download list items")
            
            for i in range(min(download_list.count(), 10)):  # Check first 10
                try:
                    item = download_list.nth(i)
                    html = item.inner_html()
                    text = item.inner_text()
                    
                    # Check if contains "تحميل متعدد"
                    if "تحميل متعدد" in text or "تحميل متعدد" in html:
                        print(f"\n✓ Found 'تحميل متعدد' in item {i+1}")
                        print(f"  HTML: {html[:200]}...")
                        
                        # Extract link
                        link = item.locator("a").first
                        if link.count() > 0:
                            href = link.get_attribute("href")
                            print(f"  URL: {href}")
                            multi_download_url = href
                            
                            # Extract quality
                            em = item.locator("em").first
                            if em.count() > 0:
                                quality = em.inner_text()
                                print(f"  Quality: {quality}")
                except Exception as e:
                    print(f"  Error reading item {i}: {e}")
        
        # Method 4: Get all HTML and search
        if not multi_download_url:
            print("\n=== Searching in page HTML ===")
            content = page.content()
            if "تحميل متعدد" in content:
                print("✓ Found 'تحميل متعدد' in page HTML")
                # Extract using regex
                import re
                # Pattern: <span class="ser-name">تحميل متعدد</span>...<a href="...">
                pattern = r'<span[^>]*class="ser-name"[^>]*>تحميل متعدد</span>.*?<a[^>]*href="([^"]+)"'
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    multi_download_url = match.group(1)
                    print(f"  Extracted URL: {multi_download_url}")
        
        # Summary
        print("\n" + "="*60)
        print("=== SUMMARY ===")
        print("="*60)
        
        if multi_download_url:
            print(f"\n✓ FOUND Multi Download Server!")
            print(f"  URL: {multi_download_url}")
            print(f"\n  ⭐ This URL will be processed by MultiServerExtractor")
            print(f"  ⭐ Will extract multiple qualities: 1080p, 720p, 480p, 360p")
        else:
            print("\n✗ Multi Download server not found")
            print("  (May need to click Watch Now button first)")
        
        # Save results
        results = {
            "episode_url": episode_url,
            "multi_download_found": multi_download_url is not None,
            "multi_download_url": multi_download_url,
            "ser_name_count": count
        }
        
        with open('multi_download_found.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Saved to multi_download_found.json")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        page.close()
        browser.close()

