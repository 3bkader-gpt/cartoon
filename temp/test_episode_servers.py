"""Test script to check available servers and qualities on episode page"""
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
        print(f"Opening: {episode_url}")
        page.goto(episode_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)
        
        # Check for download list BEFORE clicking Watch Now
        print("\n=== Checking for Download List (BEFORE Watch Now) ===")
        
        # Try multiple selectors
        selectors = [
            ".DownloadList li a",
            ".dls_table tbody tr a", 
            "ul.downloads li a",
            ".servers_list li a",
            "a.dlink"
        ]
        
        download_list = None
        for sel in selectors:
            elements = page.locator(sel)
            if elements.count() > 0:
                print(f"✓ Found download list using selector: {sel}")
                download_list = elements
                break
        
        if not download_list:
            # Try text-based search
            box = page.locator("div", has=page.locator("text=تحميل")).last
            if box.count() > 0:
                links = box.locator("a")
                if links.count() > 0:
                    print("✓ Found download links via text search")
                    download_list = links
        
        servers_found = []
        if download_list and download_list.count() > 0:
            count = download_list.count()
            print(f"\nFound {count} download servers/links:")
            
            for i in range(count):
                try:
                    link = download_list.nth(i)
                    href = link.get_attribute("href")
                    text = link.inner_text() or link.get_attribute("title") or "Server"
                    
                    if href and "javascript" not in href:
                        quality = "Unknown"
                        text_lower = text.lower()
                        if "1080" in text_lower: quality = "1080p"
                        elif "720" in text_lower: quality = "720p"
                        elif "480" in text_lower: quality = "480p"
                        elif "360" in text_lower: quality = "360p"
                        
                        server_name = text.strip()
                        for prefix in ["تحميل", "سيرفر", "Download", "Server"]:
                            server_name = server_name.replace(prefix, "").strip()
                        
                        server_info = {
                            "index": i + 1,
                            "text": text.strip(),
                            "url": href,
                            "quality": quality,
                            "server": server_name if server_name else "Server",
                            "is_multi": "Multi" in text or "haxloppd" in href or "premilkyway" in href
                        }
                        servers_found.append(server_info)
                        print(f"  {i+1}. {text.strip()[:50]}")
                        print(f"     Quality: {quality}, URL: {href[:60]}...")
                        print(f"     Is Multi: {server_info['is_multi']}")
                except Exception as e:
                    print(f"  Error reading link {i}: {e}")
        else:
            print("✗ No download list found before clicking Watch Now")
        
        # Now click Watch Now button
        print("\n=== Clicking Watch Now Button ===")
        download_btn = page.locator("div.watchNow button").first
        if download_btn.count() > 0:
            print("✓ Found Watch Now button, clicking...")
            try:
                with page.expect_navigation(wait_until="domcontentloaded", timeout=10000):
                    download_btn.click()
                print(f"✓ Navigated to: {page.url}")
                page.wait_for_timeout(3000)
            except Exception as nav_e:
                print(f"⚠ Navigation check failed: {nav_e}")
        else:
            print("✗ No Watch Now button found")
        
        # Check for download list AFTER clicking
        print("\n=== Checking for Download List (AFTER Watch Now) ===")
        download_list_after = None
        for sel in selectors:
            elements = page.locator(sel)
            if elements.count() > 0:
                print(f"✓ Found download list using selector: {sel}")
                download_list_after = elements
                break
        
        servers_after = []
        if download_list_after and download_list_after.count() > 0:
            count_after = download_list_after.count()
            print(f"\nFound {count_after} download servers after click:")
            
            for i in range(count_after):
                try:
                    link = download_list_after.nth(i)
                    href = link.get_attribute("href")
                    text = link.inner_text() or link.get_attribute("title") or "Server"
                    
                    if href and "javascript" not in href:
                        quality = "Unknown"
                        text_lower = text.lower()
                        if "1080" in text_lower: quality = "1080p"
                        elif "720" in text_lower: quality = "720p"
                        elif "480" in text_lower: quality = "480p"
                        elif "360" in text_lower: quality = "360p"
                        
                        server_name = text.strip()
                        for prefix in ["تحميل", "سيرفر", "Download", "Server"]:
                            server_name = server_name.replace(prefix, "").strip()
                        
                        server_info = {
                            "index": i + 1,
                            "text": text.strip(),
                            "url": href,
                            "quality": quality,
                            "server": server_name if server_name else "Server",
                            "is_multi": "Multi" in text or "haxloppd" in href or "premilkyway" in href or "تحميل متعدد" in text
                        }
                        servers_after.append(server_info)
                        print(f"  {i+1}. {text.strip()[:50]}")
                        print(f"     Quality: {quality}, URL: {href[:60]}...")
                        print(f"     Is Multi: {server_info['is_multi']}")
                except Exception as e:
                    print(f"  Error reading link {i}: {e}")
        
        # Also check page content for any server links
        print("\n=== Checking Page Content for Server Links ===")
        all_links = page.evaluate("""
            () => {
                return Array.from(document.querySelectorAll('a')).map(a => ({
                    href: a.href,
                    text: a.innerText.trim(),
                    title: a.title || ''
                })).filter(a => a.href && !a.href.startsWith('javascript:') && a.href !== '#');
            }
        """)
        
        server_keywords = ["forafile", "uqload", "doodstream", "vidbom", "vidoza", "foupix", "haxloppd", "premilkyway", "streamtape", "mixdrop", "uptobox"]
        found_in_content = []
        for link in all_links:
            href_lower = link['href'].lower()
            text_lower = (link['text'] + " " + link['title']).lower()
            
            for keyword in server_keywords:
                if keyword in href_lower or keyword in text_lower:
                    if not any(f['url'] == link['href'] for f in found_in_content):
                        found_in_content.append({
                            "text": link['text'],
                            "url": link['href'],
                            "matched_keyword": keyword
                        })
                        break
        
        if found_in_content:
            print(f"\nFound {len(found_in_content)} server links in page content:")
            for link in found_in_content:
                print(f"  - {link['text'][:40]} ({link['matched_keyword']})")
                print(f"    URL: {link['url'][:70]}...")
        
        # Save results
        results = {
            "episode_url": episode_url,
            "servers_before_click": servers_found,
            "page_url_after_click": page.url,
            "has_watch_now": download_btn.count() > 0 if 'download_btn' in locals() else False,
            "servers_after_click": servers_after if 'servers_after' in locals() else [],
            "servers_in_content": found_in_content if 'found_in_content' in locals() else []
        }
        
        with open('episode_servers_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Saved analysis to episode_servers_analysis.json")
        print(f"\n=== Summary ===")
        print(f"Servers found before click: {len(servers_found)}")
        print(f"Servers found after click: {len(servers_after) if 'servers_after' in locals() else 0}")
        print(f"Servers found in content: {len(found_in_content) if 'found_in_content' in locals() else 0}")
        
        all_servers = servers_found + (servers_after if 'servers_after' in locals() else [])
        if all_servers:
            multi_servers = [s for s in all_servers if s.get('is_multi', False)]
            print(f"\nMulti Download servers: {len(multi_servers)}")
            for s in multi_servers:
                print(f"  - {s['server']} ({s['quality']})")
        
        if found_in_content:
            print(f"\nServer links in page content:")
            for link in found_in_content:
                print(f"  - {link['text']} ({link['matched_keyword']})")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        page.close()
        browser.close()

