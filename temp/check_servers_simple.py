"""Quick script to check available servers on an episode page using Playwright directly"""
from playwright.sync_api import sync_playwright
import json

episode_url = "https://x7k9f.sbs/episode/%d9%85%d8%b3%d9%84%d8%b3%d9%84-the-witcher-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%b1%d8%a7%d8%a8%d8%b9-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d9%87-1-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    page = context.new_page()
    
    try:
        print(f"Opening: {episode_url}")
        page.goto(episode_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(2000)
        
        # Check for download button
        download_btn = page.locator("div.watchNow button").first
        if download_btn.count() > 0:
            print("Found Watch Now button, clicking...")
            with page.expect_navigation(wait_until="domcontentloaded", timeout=60000):
                download_btn.click()
            
            page.wait_for_timeout(5000)  # Wait for page to load
            
            # Check for DownloadList
            download_list = page.locator(".DownloadList li a")
            count = download_list.count()
            print(f"\nFound {count} download servers:")
            
            servers = []
            for i in range(count):
                try:
                    link = download_list.nth(i)
                    href = link.get_attribute("href")
                    text = link.inner_text()
                    if href:
                        servers.append({"text": text.strip(), "url": href})
                        print(f"  {i+1}. {text.strip()}")
                        print(f"     URL: {href[:80]}...")
                except Exception as e:
                    print(f"  Error reading link {i}: {e}")
            
            # Also check page URL and content for server names
            print(f"\nCurrent page URL: {page.url}")
            
            # Save to file
            with open('servers_found.json', 'w', encoding='utf-8') as f:
                json.dump({
                    "servers": servers,
                    "page_url": page.url,
                    "count": len(servers)
                }, f, ensure_ascii=False, indent=2)
            print(f"\nSaved {len(servers)} servers to servers_found.json")
            
            # Save page HTML
            with open('episode_page.html', 'w', encoding='utf-8') as f:
                f.write(page.content())
            print("Saved page HTML to episode_page.html")
        else:
            print("No Watch Now button found")
            # Save page HTML for inspection
            with open('episode_before_click.html', 'w', encoding='utf-8') as f:
                f.write(page.content())
            print("Saved page HTML to episode_before_click.html")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        page.close()
        browser.close()

