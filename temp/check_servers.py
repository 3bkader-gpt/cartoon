"""Quick script to check available servers on an episode page"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from core.browser import BrowserManager
from sites.egydead.scraper import EgyDeadScraper

# Test URL
episode_url = "https://x7k9f.sbs/episode/%d9%85%d8%b3%d9%84%d8%b3%d9%84-the-witcher-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%b1%d8%a7%d8%a8%d8%b9-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d9%87-1-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/"

scraper = EgyDeadScraper()
context = scraper.browser_manager.get_context()
page = context.new_page()

try:
    print(f"Opening: {episode_url}")
    page.goto(episode_url, wait_until="domcontentloaded", timeout=30000)
    
    # Check for download button
    download_btn = page.locator("div.watchNow button").first
    if download_btn.count() > 0:
        print("Found Watch Now button, clicking...")
        with page.expect_navigation(wait_until="domcontentloaded"):
            download_btn.click()
        
        page.wait_for_timeout(3000)
        
        # Check for DownloadList
        download_list = page.locator(".DownloadList li a")
        count = download_list.count()
        print(f"\nFound {count} download servers:")
        
        servers = []
        for i in range(count):
            link = download_list.nth(i)
            href = link.get_attribute("href")
            text = link.inner_text()
            if href:
                servers.append({"text": text.strip(), "url": href})
                print(f"  {i+1}. {text.strip()}")
                print(f"     URL: {href}")
        
        # Save to file
        import json
        with open('temp/servers_found.json', 'w', encoding='utf-8') as f:
            json.dump(servers, f, ensure_ascii=False, indent=2)
        print(f"\nSaved {len(servers)} servers to temp/servers_found.json")
    else:
        print("No Watch Now button found")
        # Save page HTML for inspection
        with open('temp/episode_after_click.html', 'w', encoding='utf-8') as f:
            f.write(page.content())
        print("Saved page HTML to temp/episode_after_click.html")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    page.close()
    scraper.browser_manager.close()

