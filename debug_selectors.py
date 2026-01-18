
import logging
from backend.core.browser import BrowserManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_page():
    browser_manager = BrowserManager(headless=True)
    browser_manager.start()
    
    try:
        context = browser_manager.get_context()
        page = context.new_page()
        
        url = "https://x7k9f.sbs/episode/%d9%85%d8%b3%d9%84%d8%b3%d9%84-the-witcher-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%b1%d8%a7%d8%a8%d8%b9-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/"
        
        logger.info(f"Navigating to: {url}")
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        print("\n--- HTML DUMP (First 2000 chars of body) ---")
        print(page.inner_html("body")[:2000])

        print("\n--- FINDING 'تحميل متعدد' ---")
        try:
            elements = page.locator("text=تحميل متعدد")
            print(f"Found {elements.count()} elements with text 'تحميل متعدد'")
            if elements.count() > 0:
                parent = elements.first.locator("..").locator("..") # Go up
                print(f"Grandparent HTML: {parent.inner_html()}")
        except Exception as e:
            print(f"Error finding text: {e}")

        print("\n--- ALL LINKS WITH 'href' ---")
        links = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('a')).map(a => ({
                text: a.innerText,
                href: a.href,
                class: a.className
            })).filter(l => l.href && l.href.length > 5);
        }""")
        
        for l in links:
            if "watch" not in l['href'] and "episode" not in l['href'] and "season" not in l['href']:
                print(f"Link: {l['text'][:20]} | Class: {l['class']} | Href: {l['href']}")

            
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        browser_manager.close()

if __name__ == "__main__":
    debug_page()
