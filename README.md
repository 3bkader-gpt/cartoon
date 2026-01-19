# Arabic Toons Downloader 📺

> A high-performance media downloader for Arabic Toons content with smart caching, library management, and Plex-compatible exports.

![Version](https://img.shields.io/badge/version-4.2.0-blue)
![Python](https://img.shields.io/badge/python-3.12+-green)
![React](https://img.shields.io/badge/react-18+-61DAFB)
![License](https://img.shields.io/badge/license-MIT-yellow)

---

## ✨ Features

### 🚀 Core Features
- **Batch Episode Fetching** - Scrape entire series with one click
- **High-Speed Metadata Retrieval** - Parallel processing for fast results
- **Smart Backend Caching (SQLite)** - Episodes cached server-side with 24-hour freshness
- **IDM/Aria2 Export** - Generate download lists in `.ef2` and `.txt` formats

### ❤️ My Library
- **Favorites System** - Save your favorite series for quick access
- **One-Click Access** - Return to any series instantly from the library
- **Synced Metadata** - Thumbnails and episode counts stored automatically

### ⚙️ Settings & Customization
- **Dark/Light Mode** - Toggle theme to your preference
- **Plex/Kodi Naming** - Export files as `Series - S01E01 - Title.mp4`
- **One-Click Folder Access** - Open Downloads folder directly from the app

### 🎯 Quality of Life
- **Select All / Deselect All** - Quickly manage episode selection
- **Episode Filtering** - Search within fetched episodes
- **Sorting Options** - Sort by episode number or title
- **Real-time Progress** - Watch episodes load with progress indicators

---

## 📸 Screenshots

![Home - Season Downloader](docs/images/home.png)
*Main downloader interface with episode grid*

![Library View](docs/images/library.png)
*My Library with favorite series*

![Settings Page](docs/images/settings.png)
*Application settings and preferences*

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + Vite)                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Downloader  │  │   Library   │  │      Settings       │  │
│  │  Component  │  │    Page     │  │        Page         │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                     │            │
│         └────────────────┼─────────────────────┘            │
│                          │                                  │
│                    API Requests                             │
└──────────────────────────┼──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI + Python)                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    SQLite Database                    │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │   │
│  │  │   series    │  │  episodes   │  │  favorites   │  │   │
│  │  │  (cached)   │──│  (cached)   │  │   (legacy)   │  │   │
│  │  │ is_favorite │  │ UNIQUE key  │  └──────────────┘  │   │
│  │  └─────────────┘  └─────────────┘                    │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Scraper    │  │  Playwright │  │    API Endpoints    │  │
│  │   Engine    │──│   Browser   │  │  /season/stream     │  │
│  │             │  │   Manager   │  │  /library/          │  │
│  └─────────────┘  └─────────────┘  │  /open-downloads    │  │
│                                    └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### SQLite Caching Strategy
- **`series` table**: Stores series URL, title, thumbnail, episode count, and `is_favorite` flag
- **`episodes` table**: Stores individual episode data with `UNIQUE(series_url, episode_number)` constraint
- **24-Hour Freshness**: Cache is considered fresh for 24 hours before requiring a re-fetch
- **Upsert Pattern**: Uses SQLite's `ON CONFLICT` clause to update or insert seamlessly

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cartoon.git
cd cartoon

# Install Python dependencies
pip install -r requirements.txt
playwright install chromium

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Running the Application

**Terminal 1 - Backend:**
```bash
python backend/main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 📦 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/season/stream` | Stream episode data (with caching) |
| `GET` | `/api/library/` | Get all favorite series |
| `POST` | `/api/library/toggle` | Toggle favorite status |
| `GET` | `/api/library/check` | Check if URL is favorited |
| `GET` | `/api/search` | Search for series |
| `POST` | `/api/open-downloads` | Open Downloads folder |
| `GET` | `/api/health` | Health check |

---

## 🔧 Configuration

Settings are stored in the browser's `localStorage`:

| Key | Values | Description |
|-----|--------|-------------|
| `theme` | `dark` / `light` | UI theme preference |
| `plex_naming` | `true` / `false` | Enable Plex-style file naming |

---

## 📁 Project Structure

```
cartoon/
├── backend/
│   ├── api/
│   │   ├── main_router.py      # Main API endpoints
│   │   └── library_router.py   # Library/favorites API
│   ├── scraper/
│   │   └── scraper.py          # Web scraper
│   ├── core/
│   │   └── browser.py          # Playwright manager
│   ├── database.py             # SQLite operations
│   └── main.py                 # FastAPI app entry
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── SeasonDownloader.jsx
│   │   ├── pages/
│   │   │   ├── Library.jsx
│   │   │   └── Settings.jsx
│   │   ├── App.jsx
│   │   └── api.js
│   └── package.json
├── docs/
│   ├── PROJECT_STATUS.md
│   └── ROADMAP.md
└── README.md
```

---

## 🗺️ Roadmap

- [x] **v3.0** - Basic downloader with IndexedDB caching
- [x] **v4.0** - SQLite backend migration
- [x] **v4.1** - My Library feature
- [x] **v4.2** - Settings page with Plex naming
- [ ] **v5.0** - Internal Download Manager (no IDM required)
- [ ] **v6.0** - Multi-source support

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/), [React](https://react.dev/), and [Playwright](https://playwright.dev/)
- Optimized for [arabic-toons.com](https://arabic-toons.com) content
