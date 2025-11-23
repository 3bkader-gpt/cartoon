# Arabic Toons Downloader

A modern web application for downloading episodes from arabic-toons.com with a beautiful React frontend and FastAPI backend.

## Features

✨ **Season Downloader**
- Fetch all episodes from a series with real-time progress tracking
- Select specific episodes or download all
- Export to IDM (.ef2 format) for batch downloading
- Copy links or download as text file
- Automatic history of recent searches

🎬 **Single Episode Player**
- Direct video URL extraction
- Built-in video player
- Episode information display

## Project Structure

```
cartoon/
├── api/                    # Core API for scraping arabic-toons.com
│   ├── __init__.py
│   └── arabic_toons_api.py
├── backend/                # FastAPI backend
│   └── main.py
├── frontend/               # React + Vite frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── HeroSection.jsx
│   │   │   ├── SeasonDownloader.jsx
│   │   │   └── VideoPlayer.jsx
│   │   ├── api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
├── discovery/              # Documentation and research
├── run_app.py             # Run both frontend and backend
└── start_backend.py       # Run backend only
```

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd cartoon
```

2. **Install Python dependencies**
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On Linux/Mac

pip install -r backend/requirements.txt
playwright install chromium
```

3. **Install Frontend dependencies**
```bash
cd frontend
npm install
cd ..
```

## Usage

### Option 1: Run Everything (Recommended)
```bash
python run_app.py
```
This will:
- Start the FastAPI backend on `http://127.0.0.1:8000`
- Start the Vite frontend on `http://localhost:5173`
- Open your browser automatically

### Option 2: Run Separately

**Terminal 1 - Backend:**
```bash
python start_backend.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then open `http://localhost:5173` in your browser.

## How to Use

### Season Downloader
1. Click "Season Downloader" button
2. Paste the series URL (e.g., `https://www.arabic-toons.com/series-name-123-anime-streaming.html`)
3. Click "Fetch Links"
4. Wait for all episodes to be processed (you'll see real-time progress)
5. Select episodes you want (all selected by default)
6. Choose export option:
   - **Copy Selected**: Copy video URLs to clipboard
   - **TXT**: Download as text file
   - **IDM Export**: Download .ef2 file for Internet Download Manager

### Single Episode
1. Paste an episode URL in the home page
2. Click "Get Video"
3. Watch directly in the browser or copy the video URL

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Playwright**: Browser automation for scraping
- **BeautifulSoup4**: HTML parsing
- **Uvicorn**: ASGI server

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Styling
- **Framer Motion**: Animations
- **Lucide React**: Icons
- **Axios**: HTTP client

## API Endpoints

- `GET /api/resolve?url=<episode_url>` - Get video URL for single episode
- `GET /api/series?url=<series_url>` - Get list of episodes
- `GET /api/season?url=<series_url>` - Get all video URLs (blocking)
- `GET /api/season/stream?url=<series_url>` - Stream progress updates (NDJSON)

## Performance

- Episode extraction: ~3-6 seconds per episode
- Full season (13 episodes): ~45-80 seconds
- Real-time progress updates via streaming

## Notes

- The application uses browser automation (Playwright) to extract video URLs
- Video URLs are temporary and contain time-based tokens
- URLs should be used immediately after extraction
- The application respects the source website's structure

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
