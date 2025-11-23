# Arabic Toons Downloader - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technical Discoveries](#technical-discoveries)
3. [API Reference](#api-reference)
4. [Architecture](#architecture)
5. [Development Notes](#development-notes)

---

## Project Overview

A modern web application for downloading episodes from arabic-toons.com with real-time progress tracking, episode selection, and IDM export functionality.

### Key Features
- **Season Downloader**: Fetch all episodes with real-time progress
- **Episode Selection**: Choose specific episodes or download all
- **IDM Export**: Generate .ef2 files for Internet Download Manager
- **History**: Automatic tracking of recent searches
- **Single Episode Player**: Direct video playback

---

## Technical Discoveries

### Video URL Structure
The site uses a direct MP4 streaming approach with the following URL pattern:
```
https://stream.foupix.com/animeios2_4/{series_id}/{filename}.mp4?tkn={token}&tms={timestamp}&ua={ua}&ips={ips}&_={random}
```

**URL Components:**
- `series_id`: Unique identifier for the series (e.g., "1740913480")
- `filename`: Video file name (e.g., "jonny_quest_01.mp4")
- `tkn`: Security token (dynamically generated)
- `tms`: Timestamp (Unix timestamp)
- `ua`: User agent hash
- `ips`: IP address hash
- `_`: Random number (Date.now())

### Token Generation
- Tokens are generated server-side and embedded in the page JavaScript
- No need to reverse-engineer token generation
- Direct extraction from DOM is the most reliable approach
- Tokens are time-sensitive and should be used immediately

### Page Structure
**Series Page:**
```
https://www.arabic-toons.com/{series-name}-{series-id}-anime-streaming.html
```

**Episode Page:**
```
https://www.arabic-toons.com/{series-name}-{series-id}-{episode-id}.html
```

### Video Player
- Uses Clappr Player (JavaScript-based)
- Video URL available in `<video>` element's `currentSrc` or `src` attribute
- Also embedded in JavaScript snippets on the page

---

## API Reference

### Core API Class: `ArabicToonsAPI`

#### Initialization
```python
from api.arabic_toons_api import ArabicToonsAPI

with ArabicToonsAPI(headless=True) as api:
    # Use API methods
    pass
```

#### Methods

**1. Get Episode Video URL**
```python
video_url = api.get_episode_video_url(episode_url)
```
- **Input**: Episode page URL
- **Output**: Direct video URL or None
- **Time**: ~3-6 seconds per episode

**2. Get Series Episodes**
```python
episodes = api.get_series_episodes(series_url)
```
- **Input**: Series page URL
- **Output**: List of episode dictionaries
- **Returns**: `[{episode_url, title, series_id, episode_id}, ...]`

**3. Download Season (Generator)**
```python
for event in api.download_season_generator(series_url):
    if event['type'] == 'start':
        print(f"Total episodes: {event['total']}")
    elif event['type'] == 'progress':
        print(f"Processing: {event['title']}")
    elif event['type'] == 'result':
        print(f"Video URL: {event['data']['video_url']}")
```
- **Input**: Series page URL
- **Output**: Generator yielding progress events
- **Event Types**: `start`, `progress`, `result`, `error`

**4. Parse Video URL**
```python
info = api.parse_video_url(video_url)
```
- **Input**: Video URL
- **Output**: Dictionary with parsed components (series_id, filename, tokens, etc.)

### REST API Endpoints

**Base URL**: `http://127.0.0.1:8000`

#### 1. Resolve Single Episode
```
GET /api/resolve?url={episode_url}
```
**Response:**
```json
{
  "video_url": "https://stream.foupix.com/...",
  "video_info": {
    "series_id": "1740913480",
    "filename": "jonny_quest_01.mp4",
    "parameters": {...}
  }
}
```

#### 2. Get Series Episodes
```
GET /api/series?url={series_url}
```
**Response:**
```json
[
  {
    "episode_url": "https://...",
    "title": "الحلقة 1",
    "series_id": "1740913480",
    "episode_id": "46523"
  }
]
```

#### 3. Download Season (Blocking)
```
GET /api/season?url={series_url}
```
**Response:**
```json
{
  "success": true,
  "total": 13,
  "episodes": [...]
}
```

#### 4. Stream Season Progress (NDJSON)
```
GET /api/season/stream?url={series_url}
```
**Response:** Newline-delimited JSON events
```json
{"type": "start", "total": 13}
{"type": "progress", "current": 1, "total": 13, "title": "الحلقة 1"}
{"type": "result", "data": {...}}
```

---

## Architecture

### Backend Stack
- **FastAPI**: Modern Python web framework
- **Playwright**: Browser automation (Chromium)
- **BeautifulSoup4**: HTML parsing
- **Uvicorn**: ASGI server

### Frontend Stack
- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first styling
- **Framer Motion**: Smooth animations
- **Lucide React**: Icon library
- **Axios**: HTTP client

### Data Flow
```
User Input (URL)
    ↓
Frontend (React)
    ↓
API Call (fetch/axios)
    ↓
Backend (FastAPI)
    ↓
Playwright (Browser Automation)
    ↓
arabic-toons.com
    ↓
Extract Video URL
    ↓
Stream Response (NDJSON)
    ↓
Frontend (Real-time Updates)
    ↓
Display Results
```

---

## Development Notes

### Performance Optimizations
1. **Reduced Timeouts**:
   - `page.goto`: 60s → 30s
   - `wait_until`: "networkidle" → "domcontentloaded"
   - `wait_for_timeout`: 5s → 3s

2. **Memory Management**:
   - Always close pages after use (`page.close()`)
   - Use context managers for browser lifecycle
   - Clear episodes state on new fetch

3. **Error Handling**:
   - Try-except around each episode
   - Continue processing on individual failures
   - Yield error events for failed episodes

### Episode URL Filtering
Handle URLs with hash fragments:
```python
if ".html" in href:
    clean_href = href.split('#')[0]  # Remove #sets, etc.
```

### IDM Export Format (.ef2)
```
<
{video_url}
filename={suggested_filename}
>
```

### Browser Automation Notes
- Playwright sync API is NOT thread-safe
- Sequential processing is more stable than parallel
- Each page should be in its own context for isolation
- Headless mode is faster but harder to debug

### Common Issues & Solutions

**Issue**: Episode links not found
- **Cause**: URL filter too strict
- **Solution**: Check for ".html" in href, not just endswith

**Issue**: Slow performance
- **Cause**: Long timeouts, networkidle wait
- **Solution**: Use domcontentloaded, reduce wait times

**Issue**: Memory leaks
- **Cause**: Pages not closed
- **Solution**: Always use try-finally with page.close()

**Issue**: Stream not updating in browser
- **Cause**: Proxy buffering or CORS
- **Solution**: Use direct backend URL or configure proxy correctly

### Testing Commands

**Test single episode:**
```bash
python -c "from api.arabic_toons_api import ArabicToonsAPI; \
with ArabicToonsAPI() as api: \
    print(api.get_episode_video_url('https://...'))"
```

**Test streaming endpoint:**
```bash
python test_stream.py
```

**Check episode count:**
```bash
python -c "from api.arabic_toons_api import ArabicToonsAPI; \
with ArabicToonsAPI() as api: \
    print(len(api.get_series_episodes('https://...')))"
```

---

## Future Enhancements

### Potential Features
- [ ] Search functionality
- [ ] Batch download multiple series
- [ ] Download progress tracking
- [ ] Quality selection (if available)
- [ ] Subtitle extraction
- [ ] Favorites/Bookmarks
- [ ] Dark/Light theme toggle
- [ ] Mobile responsive improvements

### Performance Improvements
- [ ] Implement async API with asyncio
- [ ] Add caching layer (Redis)
- [ ] Parallel episode processing (with async)
- [ ] CDN integration for faster delivery
- [ ] Database for history persistence

### Code Quality
- [ ] Add unit tests
- [ ] Add integration tests
- [ ] Set up CI/CD pipeline
- [ ] Add type hints throughout
- [ ] Implement logging levels
- [ ] Add monitoring/metrics

---

## License
MIT License - Free to use and modify

## Credits
Built with ❤️ using modern web technologies
