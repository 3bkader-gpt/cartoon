"""Test extraction from hglink.to (Multi Download server)"""
from playwright.sync_api import sync_playwright
import json

hglink_url = "https://hglink.to/9w2avl5498t3"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    page = context.new_page()
    
    try:
        print(f"Opening Multi Download: {hglink_url}\n")
        page.goto(hglink_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)
        
        print(f"Current URL: {page.url}")
        
        # Check for "Create Download Link" button
        print("\n=== Step 1: Checking for 'Create Download Link' button ===")
        create_link_btn = page.locator("button:has-text('Create Download Link'), a:has-text('Create Download Link'), input[value='Create Download Link']")
        
        if create_link_btn.count() > 0:
            print("✓ Found 'Create Download Link' button")
            
            # Check for countdown
            countdown = page.locator("#countdown")
            if countdown.count() > 0:
                print("  Waiting for countdown...")
                page.wait_for_timeout(5000)
            
            try:
                with page.expect_navigation(timeout=15000, wait_until="domcontentloaded"):
                    create_link_btn.first.click()
                print(f"✓ Clicked, navigated to: {page.url}")
                page.wait_for_timeout(3000)
            except Exception as e:
                print(f"⚠ Navigation: {e}")
        else:
            print("✗ No 'Create Download Link' button found")
        
        # Check for download link
        print("\n=== Step 2: Checking Download Link ===")
        download_link = page.locator("a[href*='/f/']").first
        if download_link.count() > 0:
            download_url = download_link.get_attribute("href")
            print(f"✓ Found download link: {download_url}")
            
            # Navigate to download page
            try:
                page.goto(download_url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(3000)
                print(f"✓ Navigated to download page: {page.url}")
            except Exception as e:
                print(f"⚠ Error navigating: {e}")
        
        # Also try clicking "Download Link" tab
        download_tab = page.locator("a[href*='#tab-download-link']").first
        if download_tab.count() > 0:
            print("✓ Found 'Download Link' tab")
            try:
                # Use JavaScript to click to avoid intercept issues
                page.evaluate("document.querySelector('a[href*=\"#tab-download-link\"]').click()")
                page.wait_for_timeout(2000)
                print("✓ Clicked download link tab")
            except Exception as e:
                print(f"⚠ Error clicking tab: {e}")
        
        # Get all links and check for quality indicators
        print("\n=== Step 3: Extracting Quality Links ===")
        all_links = page.evaluate("""
            () => {
                return Array.from(document.querySelectorAll('a')).map(a => ({
                    href: a.href,
                    text: a.innerText.trim(),
                    title: a.title || '',
                    innerHTML: a.innerHTML
                }));
            }
        """)
        
        # Also get all text content to check for quality indicators
        page_content = page.evaluate("() => document.body.innerText")
        print(f"\nPage content preview: {page_content[:500]}...")
        
        print(f"Found {len(all_links)} total links")
        
        quality_keywords = ["1080p", "720p", "480p", "360p", "240p", "1080", "720", "480", "360", "Full HD", "HD", "SD", "Low Quality"]
        quality_links = []
        
        for link in all_links:
            if not link['href'] or "javascript" in link['href']:
                continue
                
            text = (link['text'] + " " + link['title'] + " " + link.get('innerHTML', '')).lower()
            href_lower = link['href'].lower()
            
            # Check for quality in text or href
            for keyword in quality_keywords:
                if keyword.lower() in text or keyword.lower() in href_lower:
                    # Avoid duplicates
                    if not any(q['url'] == link['href'] for q in quality_links):
                        quality_links.append({
                            "text": link['text'],
                            "url": link['href'],
                            "keyword": keyword,
                            "html": link.get('innerHTML', '')[:100]
                        })
                        break
        
        # Also check for quality in page structure (divs, spans, etc.)
        print("\n=== Checking page structure for quality options ===")
        quality_elements = page.evaluate("""
            () => {
                const elements = [];
                const allElements = document.querySelectorAll('div, span, li, td');
                for (const el of allElements) {
                    const text = el.innerText.toLowerCase();
                    if (text.includes('1080') || text.includes('720') || text.includes('480') || 
                        text.includes('360') || text.includes('full hd') || text.includes('hd quality')) {
                        const link = el.querySelector('a');
                        if (link && link.href) {
                            elements.push({
                                text: el.innerText.trim(),
                                url: link.href,
                                html: el.innerHTML.substring(0, 200)
                            });
                        }
                    }
                }
                return elements;
            }
        """)
        
        if quality_elements:
            print(f"Found {len(quality_elements)} elements with quality indicators:")
            for elem in quality_elements[:10]:  # Show first 10
                print(f"  - {elem['text'][:50]}")
                print(f"    URL: {elem['url'][:70]}...")
                if not any(q['url'] == elem['url'] for q in quality_links):
                    quality_links.append({
                        "text": elem['text'],
                        "url": elem['url'],
                        "keyword": "Found in structure"
                    })
        
        if quality_links:
            print(f"\n✓ Found {len(quality_links)} quality links:")
            for q in quality_links:
                print(f"  - {q['text']} ({q['keyword']})")
                print(f"    URL: {q['url'][:70]}...")
        else:
            print("✗ No quality links found")
            print("\nShowing first 20 links:")
            for i, link in enumerate(all_links[:20]):
                if link['text']:
                    print(f"  {i+1}. {link['text'][:40]} - {link['href'][:50]}...")
        
        # Check page content
        page_text = page.evaluate("() => document.body.innerText")
        if any(kw in page_text.lower() for kw in ["1080", "720", "480", "quality", "جودة"]):
            print("\n✓ Page contains quality-related text")
        
        # Save results
        results = {
            "hglink_url": hglink_url,
            "final_url": page.url,
            "quality_links": quality_links,
            "total_links": len(all_links),
            "has_quality_text": any(kw in page_text.lower() for kw in ["1080", "720", "480", "quality"])
        }
        
        with open('hglink_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Saved to hglink_analysis.json")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        page.close()
        browser.close()

