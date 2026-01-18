"""Manual check of episode 6 page structure"""
from playwright.sync_api import sync_playwright
import json

episode_url = "https://x7k9f.sbs/episode/%d9%85%d8%b3%d9%84%d8%b3%d9%84-the-witcher-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%b1%d8%a7%d8%a8%d8%b9-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-6-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/"

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
        
        # Step 1: Check BEFORE clicking Watch Now
        print("=== BEFORE Clicking Watch Now ===")
        ser_name_spans = page.locator("span.ser-name")
        count_before = ser_name_spans.count()
        print(f"Found {count_before} span.ser-name elements")
        
        if count_before > 0:
            print("\nServers found:")
            for i in range(count_before):
                try:
                    span = ser_name_spans.nth(i)
                    text = span.inner_text()
                    print(f"  {i+1}. {text}")
                    
                    # Try to find link
                    parent = span.locator("..")
                    link = parent.locator("a").first
                    if link.count() == 0:
                        grandparent = parent.locator("..")
                        link = grandparent.locator("a").first
                    
                    if link.count() > 0:
                        href = link.get_attribute("href")
                        print(f"     URL: {href[:60] if href else 'None'}...")
                except Exception as e:
                    print(f"  Error: {e}")
        
        # Step 2: Click Watch Now
        print("\n=== Clicking Watch Now ===")
        download_btn = page.locator("div.watchNow button").first
        if download_btn.count() > 0:
            print("✓ Found Watch Now button, clicking...")
            try:
                with page.expect_navigation(wait_until="domcontentloaded", timeout=10000):
                    download_btn.click()
                print(f"✓ Navigated to: {page.url}")
                page.wait_for_timeout(3000)
            except Exception as e:
                print(f"⚠ Navigation: {e}")
        else:
            print("✗ Watch Now button not found")
        
        # Step 3: Check AFTER clicking Watch Now
        print("\n=== AFTER Clicking Watch Now ===")
        ser_name_spans = page.locator("span.ser-name")
        count_after = ser_name_spans.count()
        print(f"Found {count_after} span.ser-name elements")
        
        servers_found = []
        if count_after > 0:
            print("\nServers found:")
            for i in range(count_after):
                try:
                    span = ser_name_spans.nth(i)
                    text = span.inner_text()
                    
                    # Find link
                    parent = span.locator("..")
                    link = parent.locator("a").first
                    if link.count() == 0:
                        grandparent = parent.locator("..")
                        link = grandparent.locator("a").first
                    
                    href = None
                    if link.count() > 0:
                        href = link.get_attribute("href")
                    
                    # Get quality from <em>
                    em = parent.locator("em").first
                    quality_text = em.inner_text() if em.count() > 0 else "Unknown"
                    
                    server_info = {
                        "index": i + 1,
                        "name": text,
                        "url": href,
                        "quality": quality_text,
                        "is_multi": "تحميل متعدد" in text or "Multi" in text
                    }
                    servers_found.append(server_info)
                    
                    marker = "⭐ MULTI" if server_info['is_multi'] else ""
                    print(f"  {i+1}. {text} ({quality_text}) {marker}")
                    if href:
                        print(f"     URL: {href[:70]}...")
                except Exception as e:
                    print(f"  Error reading server {i}: {e}")
        
        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"\nServers before click: {count_before}")
        print(f"Servers after click: {count_after}")
        
        multi_servers = [s for s in servers_found if s['is_multi']]
        print(f"\nMulti Download servers: {len(multi_servers)}")
        if multi_servers:
            print("  ⭐ These will be processed by MultiServerExtractor:")
            for s in multi_servers:
                print(f"    - {s['name']} ({s['quality']})")
                print(f"      URL: {s['url'][:70] if s['url'] else 'None'}...")
        else:
            print("  ✗ No Multi Download servers found")
        
        # Save results
        results = {
            "episode_url": episode_url,
            "servers_before_click": count_before,
            "servers_after_click": count_after,
            "servers_found": servers_found,
            "multi_servers": multi_servers
        }
        
        with open('episode6_manual_check.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Saved to episode6_manual_check.json")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        page.close()
        browser.close()

