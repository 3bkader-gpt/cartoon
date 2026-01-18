# 🎬 Cartoon Downloader

**Version**: v2.2-multi-site  
**Status**: 🚧 In Development  
**Last Updated**: 2025-11-25

A modern, modular web application for downloading episodes from multiple Arabic cartoon streaming sites with advanced selection, sorting, and export capabilities.

## 🌐 Supported Sites

- ✅ **Arabic Toons** - Fully working
- 🚧 **EgyDead** - In development

---

## ✨ Features

### Core Functionality
- ✅ **Episode Fetching** - Extract all episodes from series URLs
- ✅ **Progress Tracking** - Real-time progress bar during extraction
- ✅ **Metadata Display** - File size, thumbnails, and episode info
- ✅ **Proxy Download** - Bypass 403 Forbidden errors
- ✅ **Download History** - Track last 10 downloads with stats

### Selection System
- ✅ **Individual Selection** - Checkbox for each episode
- ✅ **Select All** - Quick toggle for all episodes
- ✅ **Auto-Select** - All episodes selected by default
- ✅ **Selection Count** - Live count of selected episodes

### Sorting & Filtering
- ✅ **Search** - Filter by episode name or filename
- ✅ **Sort by Episode** - Numerical order
- ✅ **Sort by Name** - Alphabetical order
- ✅ **Sort by Size** - File size order
- ✅ **Asc/Desc Toggle** - Reverse sort direction

### Export Functions
- ✅ **TXT Export** - Plain text list of URLs
- ✅ **IDM Export** - .ef2 format for Internet Download Manager
- ✅ **Copy URL** - Quick clipboard copy

### UI/UX
- ✅ **Dark Mode** - Full dark theme support
- ✅ **Responsive Design** - Works on mobile and desktop
- ✅ **Smooth Animations** - Hover effects and transitions
- ✅ **Modern Design** - Clean, professional interface
- ✅ **Grid Layout** - Beautiful card-based episode display

---

## 📁 Project Structure

```
cartoon/
├── backend/
│   ├── main.py                     # FastAPI server entry point
│   ├── api/
│   │   └── main_router.py          # API routes (streaming endpoint)
│   ├── core/
│   │   ├── browser.py              # Playwright browser manager
│   │   └── selector.py             # Auto-selects scraper by URL
│   └── sites/
│       ├── arabic_toons/
│       │   ├── config.py           # Site configuration
│       │   ├── parser.py           # HTML/data parsing
│       │   └── scraper.py          # Main scraper logic
│       └── egydead/
│           ├── config.py
│           ├── parser.py
│           └── scraper.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── SeasonDownloader.jsx   # Main component
│   │   │   ├── ThemeToggle.jsx        # Dark mode toggle
│   │   │   └── HistoryItem.jsx        # Download history
│   │   ├── pages/
│   │   │   ├── Home.jsx               # Home page
│   │   │   └── History.jsx            # History page
│   │   ├── contexts/
│   │   │   └── ThemeContext.jsx       # Theme provider
│   │   ├── utils/
│   │   │   └── animations.js          # Animation utilities
│   │   ├── App.jsx
│   │   ├── api.js                     # API client
│   │   ├── index.css                  # Global styles
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── docs/
│   ├── DOCUMENTATION.md               # Technical documentation
│   ├── PROJECT_STATUS.md              # Current status
│   └── MANUAL_TESTING_GUIDE.md        # Testing guide
│
├── .gitignore
├── README.md
├── RELEASE_NOTES_V2.0.md
└── package.json                       # Root package.json
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

#### 1. Clone Repository
```bash
git clone <repository-url>
cd cartoon
```

#### 2. Install Backend Dependencies
```bash
pip install -r backend/requirements.txt
playwright install chromium
```

#### 3. Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

### Running the Application

#### Backend (Terminal 1):
```bash
python backend/main.py
# Server runs on http://127.0.0.1:8000
```

#### Frontend (Terminal 2):
```bash
cd frontend
npm run dev
# Dev server runs on http://localhost:5173
```

### Access the Application
Open your browser and navigate to: `http://localhost:5173`

---

## 📖 Usage

### Basic Workflow

1. **Paste URL**
   - Copy a series URL from supported sites
   - Paste it into the input field
   - Click "Fetch Episodes"

2. **Wait for Episodes**
   - Progress bar shows extraction progress
   - Episodes appear in real-time
   - All episodes auto-selected

3. **Select Episodes** (Optional)
   - Uncheck episodes you don't want
   - Use "Select All" to toggle all
   - Search to filter specific episodes

4. **Sort & Filter** (Optional)
   - Search by name or filename
   - Sort by episode number, name, or size
   - Toggle ascending/descending order

5. **Export or Download**
   - **Save List**: Download .txt file with URLs
   - **Export to IDM**: Download .ef2 file for IDM
   - **Direct Download**: Click download icon on episode
   - **Copy URL**: Click copy icon to copy URL

---

## 🔧 Configuration

### Backend (FastAPI)
- **Port**: 8000
- **Host**: 127.0.0.1
- **CORS**: Enabled for localhost:5173

### Frontend (Vite + React)
- **Port**: 5173
- **API Base**: http://127.0.0.1:8000/api

---

## 🚧 Roadmap

### Current Phase: Multi-Site Support
- ✅ Arabic Toons - Fully working
- 🚧 EgyDead - In development
  - ✅ Episode list extraction
  - 🚧 Video URL extraction (in progress)

### Future Enhancements
- [ ] More site support
- [ ] Batch download queue
- [ ] Resume/Pause support
- [ ] Auto-retry failed downloads
- [ ] Download speed tracking

---

## 📝 Documentation

- **Full Documentation**: `docs/DOCUMENTATION.md`
- **Project Status**: `docs/PROJECT_STATUS.md`
- **Testing Guide**: `docs/MANUAL_TESTING_GUIDE.md`

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is for educational purposes only.

---

## 🙏 Acknowledgments

- **Playwright** - Web scraping
- **FastAPI** - Backend framework
- **React** - Frontend framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling

---

## 📞 Support

For issues or questions:
1. Check `docs/MANUAL_TESTING_GUIDE.md`
2. Review console errors
3. Verify backend is running
4. Check network tab for API responses

---

**Made with ❤️ for the Arabic cartoon community**

**Version**: v2.2-multi-site | **Status**: 🚧 In Development
