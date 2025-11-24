# Scrapling Integration Notes

## Why Scrapling?

Scrapling is a modern web scraping library that offers several advantages over traditional Playwright:

### Key Benefits:
1. **Anti-Bot Bypass**: Automatic Cloudflare solving and better fingerprint spoofing
2. **Adaptive Scraping**: Automatically relocates elements after website changes
3. **Performance**: 698x faster parsing than BeautifulSoup, memory efficient
4. **Session Management**: Better cookie and state management
5. **HTTP3 Support**: Modern protocol support

## Installation

```bash
pip install "scrapling[fetchers]"
scrapling install
```

## Usage in EgyDead

We've created an alternative scraper (`scraper_scrapling.py`) that uses Scrapling instead of Playwright.

### To test it:

1. Install Scrapling:
   ```bash
   cd d:/projects/cartoon
   pip install "scrapling[fetchers]"
   scrapling install
   ```

2. Update `backend/core/selector.py` to use the Scrapling version:
   ```python
   from ..sites.egydead.scraper_scrapling import EgyDeadScraplerScraper
   
   # In get_scraper method:
   if any(pattern in url for pattern in EGYDEAD_PATTERNS):
       return EgyDeadScraplerScraper()  # No browser_manager needed
   ```

3. Test with the frontend

## Comparison: Playwright vs Scrapling

| Feature | Playwright | Scrapling |
|---------|-----------|-----------|
| **Anti-Bot** | Basic | Advanced (Cloudflare solving) |
| **Speed** | Good | Excellent |
| **Adaptive** | No | Yes |
| **Memory** | Heavy | Light |
| **Session** | Manual | Built-in |
| **Learning Curve** | Medium | Easy |

## Recommendation

**Current Strategy:**
- Keep **Playwright** for Arabic Toons (it's working perfectly)
- Try **Scrapling** for EgyDead (might solve video extraction issues)
- Use **Scrapling** for future sites with heavy anti-bot protection

**Future Strategy:**
- If Scrapling proves successful with EgyDead, consider it for new sites
- Keep both options available (Playwright for simple sites, Scrapling for complex ones)

## Code Examples

### Basic Fetching
```python
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch(
    'https://egydead.skin/episode/...',
    headless=True,
    solve_cloudflare=True,
    network_idle=True
)

video_url = page.css_first('iframe[src*="embed"]::attr(src)')
```

### Session Usage
```python
from scrapling.fetchers import StealthySession

with StealthySession(headless=True, solve_cloudflare=True) as session:
    season_page = session.fetch('https://egydead.skin/season/...')
    episodes = season_page.css('a[href*="/episode/"]')
    
    for ep in episodes:
        ep_page = session.fetch(ep.attrib['href'])
        video = ep_page.css_first('video::attr(src)')
```

### Adaptive Scraping
```python
# First time - save the selector pattern
episodes = page.css('.episode-list a', auto_save=True)

# Later, if website structure changes
episodes = page.css('.episode-list a', adaptive=True)
# Scrapling automatically finds them even if class names changed!
```

## Testing Checklist

- [ ] Install Scrapling dependencies
- [ ] Test basic fetching with EgyDead
- [ ] Test video URL extraction
- [ ] Test session management
- [ ] Compare performance with Playwright
- [ ] Test Cloudflare bypass (if applicable)
- [ ] Verify cache system compatibility
- [ ] Update documentation if successful

## Resources

- [Scrapling Documentation](https://scrapling.readthedocs.io/)
- [GitHub Repository](https://github.com/D4Vinci/Scrapling)
- [Migration Guide](https://scrapling.readthedocs.io/en/latest/tutorials/migrating_from_beautifulsoup/)
