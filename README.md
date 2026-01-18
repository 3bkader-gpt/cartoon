# 🎬 Arabic Toons Downloader

**Version**: v3.0-specialized
**Status**: 🚀 Stable

A specialized, high-performance tool for downloading full cartoon series and episodes exclusively from **Arabic Toons**.

---

## ✨ Features

### Core Functionality
- ✅ **One-Click Fetch** - Paste any Arabic Toons URL (series or episode)
- ✅ **Full Season Support** - Detects and loads all episodes automatically
- ✅ **Metadata Extraction** - Gets high-quality thumbnails, file sizes, and titles
- ✅ **Smart Caching** - Remembers fetched seasons for instant reloading (IndexedDB)
- ✅ **Proxy Download** - Bypasses CORS/403 restrictions automatically

### Advanced Selection & Export
- ✅ **Smart Filtering** - Search by name or filename
- ✅ **Sorting** - Sort by Episode Number, Name, or Size
- ✅ **Export Options**:
  - 📝 **TXT List** - For batch downloaders
  - ⬇️ **IDM Export** - Native `.ef2` format for Internet Download Manager
  - 📋 **Copy URL** - Quick clipboard actions

### UI/UX
- 🎨 **Modern Interface** - Beautiful Glassmorphism design
- 🌙 **Dark Mode** - Optimized for night usage
- 📱 **Responsive** - Works perfectly on Desktop & Mobile
- ⚡ **Real-time Progress** - Visual feedback during fetching

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+

### 1. Installation

```bash
# Clone repository
git clone <repository-url>
cd cartoon

# Install Backend
pip install -r backend/requirements.txt
playwright install chromium

# Install Frontend
cd frontend
npm install
```

### 2. Running

**Using Batch Script (Windows):**
```bash
.\start_all.bat
```

**Or Manually:**
```bash
# Terminal 1 (Backend)
python backend/main.py

# Terminal 2 (Frontend)
cd frontend
npm run dev
```

### 3. Usage
1. Go to `http://localhost:5173`
2. Paste any link from `arabic-toons.com`
3. Click **Fetch**
4. Select episodes and click **Download** or **Export to IDM**

---

## 🔧 Technical Architecture

The project uses a streamlined architecture focused on performance:

```
cartoon/
├── backend/
│   ├── api/
│   │   └── main_router.py      # API Endpoints
│   ├── scraper/
│   │   ├── scraper.py          # Core Arabic Toons Logic
│   │   ├── parser.py           # HTML Parsing
│   │   └── config.py           # Site Selectors
│   ├── core/
│   │   └── browser.py          # Playwright Manager
│   └── main.py                 # Server Entry Point
│
└── frontend/                   # React + Vite + Tailwind
```

---

## 📞 Troubleshooting

- **Backend won't start?** Check `pip install -r backend/requirements.txt`
- **Fetching issues?** Check your internet connection or if site structure changed associated with `backend/scraper/config.py`
- **Browser Error?** Run `playwright install chromium`

---

**Made with ❤️ for the Arabic cartoon community**
