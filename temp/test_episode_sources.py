"""Test episode page to see what sources/qualities will be returned"""
from playwright.sync_api import sync_playwright
import json
import re

episode_url = "https://x7k9f.sbs/episode/%d9%85%d8%b3%d9%84%d8%b3%d9%84-the-witcher-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%b1%d8%a7%d8%a8%d8%b9-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    page = context.new_page()
    
    try:
        print(f"Opening episode: {episode_url}\n")
        page.goto(episode_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(2000)
        
        sources = []
        
        # Step 1: Check for DownloadList BEFORE clicking
        print("=== Step 1: Checking for DownloadList (BEFORE Watch Now) ===")
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
                print(f"✓ Found using: {sel}")
                download_list = elements
                break
        
        if download_list and download_list.count() > 0:
            count = download_list.count()
            print(f"Found {count} download servers:")
            
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
                        
                        source_info = {
                            "url": href,
                            "quality": quality,
                            "server": server_name if server_name else "Server",
                            "type": "server",
                            "is_multi": "Multi" in text or "haxloppd" in href or "premilkyway" in href or "تحميل متعدد" in text
                        }
                        sources.append(source_info)
                        print(f"  {i+1}. {text.strip()[:40]} ({quality}) - {'⭐ MULTI' if source_info['is_multi'] else ''}")
                except Exception as e:
                    print(f"  Error reading link {i}: {e}")
        else:
            print("✗ No DownloadList found")
        
        # Step 2: Click Watch Now
        print("\n=== Step 2: Clicking Watch Now ===")
        download_btn = page.locator("div.watchNow button").first
        if download_btn.count() > 0:
            print("✓ Found Watch Now button")
            try:
                with page.expect_navigation(wait_until="domcontentloaded", timeout=10000):
                    download_btn.click()
                print(f"✓ Navigated to: {page.url}")
                page.wait_for_timeout(3000)
            except Exception as e:
                print(f"⚠ Navigation: {e}")
        
        # Step 3: Check for provider links in content
        print("\n=== Step 3: Checking for Provider Links ===")
        provider_url = page.evaluate("""
            () => {
                const links = document.querySelectorAll('a[href*="forafile"], a[href*="foupix"], a[href*="uqload"], a[href*="haxloppd"], a[href*="premilkyway"]');
                for (const link of links) {
                    if (link.href) return link.href;
                }
                return null;
            }
        """)
        
        if provider_url:
            print(f"✓ Found provider URL: {provider_url}")
            
            # Check if it's a Multi server
            is_multi = "haxloppd" in provider_url or "premilkyway" in provider_url
            print(f"  Is Multi Server: {is_multi}")
            
            if is_multi:
                print("  ⭐ This is a MULTI SERVER - will extract multiple qualities!")
                sources.append({
                    "url": provider_url,
                    "quality": "Multiple",
                    "server": "Multi Download",
                    "type": "multi_server",
                    "will_extract_qualities": True
                })
            else:
                sources.append({
                    "url": provider_url,
                    "quality": "Auto",
                    "server": "Provider",
                    "type": "provider"
                })
        
        # Step 4: Check current page URL for extractors
        print("\n=== Step 4: Checking Current Page URL ===")
        current_url = page.url
        print(f"Current URL: {current_url}")
        
        server_keywords = ["forafile", "uqload", "doodstream", "vidbom", "vidoza", "foupix", "haxloppd", "premilkyway"]
        for keyword in server_keywords:
            if keyword in current_url.lower():
                print(f"✓ Detected {keyword} in URL - will use extractor")
                is_multi = keyword in ["haxloppd", "premilkyway"]
                if is_multi:
                    print(f"  ⭐ MULTI SERVER - will return multiple quality options!")
                break
        
        # Summary
        print("\n" + "="*60)
        print("=== SUMMARY: Sources that will be returned ===")
        print("="*60)
        
        if sources:
            print(f"\nTotal sources found: {len(sources)}")
            multi_count = sum(1 for s in sources if s.get('is_multi') or s.get('will_extract_qualities'))
            
            if multi_count > 0:
                print(f"\n⭐ MULTI SERVER SOURCES: {multi_count}")
                print("   These will be expanded into multiple quality options:")
                for s in sources:
                    if s.get('is_multi') or s.get('will_extract_qualities'):
                        print(f"   - {s['server']} → Will extract: 1080p, 720p, 480p, 360p")
            
            print(f"\nAll sources:")
            for i, s in enumerate(sources, 1):
                print(f"  {i}. {s['server']} ({s['quality']})")
                if s.get('is_multi') or s.get('will_extract_qualities'):
                    print(f"     ⭐ Will expand to multiple qualities")
        else:
            print("⚠ No sources found - may need to check video tag/iframe")
        
        # Save results
        results = {
            "episode_url": episode_url,
            "sources": sources,
            "current_url": current_url,
            "has_multi_server": any(s.get('is_multi') or s.get('will_extract_qualities') for s in sources)
        }
        
        with open('episode_sources_final.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Saved to episode_sources_final.json")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        page.close()
        browser.close()

