
import logging
from backend.sites.egydead.scraper import EgyDeadScraper
from backend.core.browser import BrowserManager

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_witcher():
    browser_manager = BrowserManager()
    browser_manager.start()
    
    try:
        scraper = EgyDeadScraper(browser_manager)
        
        season_url = "https://x7k9f.sbs/season/%d9%85%d8%b3%d9%84%d8%b3%d9%84-the-witcher-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%b1%d8%a7%d8%a8%d8%b9-%d9%85%d8%aa%d8%b1%d8%ac%d9%85-%d9%83%d8%a7%d9%85%d9%84/"
        
        print(f"\n--- 1. Getting Episodes from Season: {season_url} ---")
        episodes = scraper.get_series_episodes(season_url)
        print(f"Found {len(episodes)} episodes.")
        
        if episodes:
            first_ep = episodes[0]
            print(f"\n--- 2. Extracting First Episode: {first_ep['title']} ---")
            print(f"URL: {first_ep['episode_url']}")
            
            result = scraper.get_episode_video_url(first_ep['episode_url'], include_metadata=True)
            
            print("\n--- 3. EXTRACTION RESULT ---")
            print(f"Primary Video URL: {result.get('video_url')}")
            
            error = result.get('error')
            if error:
                print(f"Error: {error}")
            
            sources = result.get('sources', [])
            print(f"Found {len(sources)} sources:")
            for s in sources:
                print(f" - [{s.get('server')}] {s.get('quality')} : {s.get('url')[:60]}...")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
    finally:
        browser_manager.close()

if __name__ == "__main__":
    test_witcher()
