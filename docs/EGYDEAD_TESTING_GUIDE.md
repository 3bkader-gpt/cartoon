# 🧪 EgyDead Testing Guide

## Manual Testing Steps

Since the browser subagent is currently unavailable, follow these steps to test and debug the EgyDead scraper:

### 1. Open Season Page
```
https://egydead.skin/season/مسلسل-tulsa-king-الموسم-الثالث-مترجم-كامل-ا/
```

### 2. Inspect Episode Links
- Open DevTools (F12)
- Look for episode links in the HTML
- **Current finding**: Links are in format:
  ```
  <a href="https://egydead.skin/episode/...">حلقه 10</a>
  ```
- **Selector to use**: `a[href*='/episode/']`

### 3. Open an Episode Page
```
https://egydead.skin/episode/مسلسل-tulsa-king-الموسم-الثالث-الحلقة-10-مترجمة/
```

### 4. Find Video Player
- Look for:
  - `<iframe>` tags (most likely)
  - `<video>` tags
  - Download buttons with `.mp4` links
- **Inspect the iframe src** - it might be:
  - Embedded player (e.g., `vidstream`, `vidbom`, etc.)
  - Direct video URL

### 5. Extract Video URL
- If iframe: Navigate to iframe src and inspect
- If video tag: Get `src` or `currentSrc` attribute
- If download link: Get `href` attribute

### 6. Update Selectors in `config.py`
Based on your findings, update:
```python
SELECTORS = {
    "episode_links": "YOUR_SELECTOR_HERE",  # e.g., "a[href*='/episode/']"
    "video_iframe": "YOUR_SELECTOR_HERE",   # e.g., "iframe.player"
    "download_links": "YOUR_SELECTOR_HERE", # e.g., "a.download-btn"
    "poster": "YOUR_SELECTOR_HERE",         # e.g., "meta[property='og:image']"
}
```

### 7. Test with Python
```python
from backend.sites.egydead.scraper import EgyDeadScraper
from backend.core.browser import BrowserManager

browser_manager = BrowserManager()
scraper = EgyDeadScraper(browser_manager)

# Test getting episodes
episodes = scraper.get_season_episodes("https://egydead.skin/season/...")
print(f"Found {len(episodes)} episodes")

# Test getting video URL
video_url = scraper.get_episode_video_url(episodes[0]["episode_url"])
print(f"Video URL: {video_url}")
```

### 8. Common Issues & Solutions

#### Issue: No episodes found
- **Solution**: Update `SELECTORS["episode_links"]` in `config.py`
- Check if links are loaded dynamically (wait longer)

#### Issue: No video URL found
- **Solution**: 
  - Check if video is in iframe (navigate to iframe.src)
  - Check if there's a "Watch" or "Download" button to click first
  - Look for JavaScript-loaded content (increase wait time)

#### Issue: 403 Forbidden
- **Solution**: Add proper headers in `get_video_metadata()`:
  ```python
  headers = {
      "User-Agent": "Mozilla/5.0...",
      "Referer": BASE_URL,
      "Origin": BASE_URL
  }
  ```

### 9. Debugging Tips
- Use `page.screenshot(path="debug.png")` to see what Playwright sees
- Use `page.content()` to inspect the full HTML
- Use `page.wait_for_selector("YOUR_SELECTOR", timeout=10000)` to wait for elements

### 10. Expected Results
- **Season page**: Should find 10 episodes
- **Episode page**: Should extract video URL (iframe or direct link)
- **Video metadata**: Should get file size (if available)

---

## Next Steps
Once you've identified the correct selectors:
1. Update `backend/sites/egydead/config.py`
2. Test with the frontend
3. Verify cache system works with EgyDead
4. Commit the working version

---

**Note**: EgyDead might have anti-scraping measures (Cloudflare, CAPTCHA). If so, you may need to:
- Add delays between requests
- Use residential proxies
- Implement CAPTCHA solving
