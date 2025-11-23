# 🎬 Arabic Toons Downloader

**Version**: v1.0-stable  
**Status**: ✅ Production Ready  
**Last Updated**: 2025-11-23

A modern, feature-rich web application for downloading episodes from Arabic Toons with advanced selection, sorting, and export capabilities.

---

## ✨ Features

### Core Functionality
- ✅ **Episode Fetching** - Extract all episodes from series URLs
- ✅ **Progress Tracking** - Real-time progress bar during extraction
- ✅ **Metadata Display** - File size, thumbnails, and episode info
- ✅ **Proxy Download** - Bypass 403 Forbidden errors

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

---

## 📁 Project Structure

```
arabic-toons-downloader/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── arabic_toons_api.py    # Playwright scraper
│   ├── main.py                     # FastAPI server
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── SeasonDownloader.jsx   # Main component
│   │   │   └── ThemeToggle.jsx        # Dark mode toggle
│   │   ├── contexts/
│   │   │   └── ThemeContext.jsx       # Theme provider
│   │   ├── App.jsx
│   │   ├── api.js                     # API client
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── docs/
│   ├── DOCUMENTATION.md
│   ├── STABLE_VERSION.md
│   ├── GIT_BACKUP_STRATEGY.md
│   ├── TESTING.md
│   ├── TESTING_RESULTS.md
│   ├── TESTING_SUMMARY.md
│   └── MANUAL_TESTING_GUIDE.md
│
├── .gitignore
├── README.md
├── start_backend.py
├── run_app.py
└── test_backend.py
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
cd arabic-toons-downloader
```

#### 2. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
playwright install chromium
```

#### 3. Install Frontend Dependencies
```bash
cd frontend
npm install
```

### Running the Application

#### Option 1: Run Both (Recommended)
```bash
python run_app.py
```

#### Option 2: Run Separately

**Backend:**
```bash
python start_backend.py
# Server runs on http://127.0.0.1:8000
```

**Frontend:**
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
   - Copy a series URL from arabic-toons.com
   - Paste it into the input field
   - Click "Fetch"

2. **Wait for Episodes**
   - Progress bar shows extraction progress
   - Episodes appear one by one
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

## 🧪 Testing

### Run Backend Tests
```bash
python test_backend.py
```

### Manual Testing
See `docs/MANUAL_TESTING_GUIDE.md` for comprehensive testing instructions.

### Test Results
- ✅ 19/19 tests passed
- ✅ 0 bugs found
- ✅ 100% success rate

See `docs/TESTING_RESULTS.md` for detailed results.

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

## 📦 Git Branches

```
master          # Main stable branch
├── stable      # Protected backup (v1.0-stable)
└── ui-rework   # Active development branch
```

### Rollback to Stable
```bash
git checkout stable
```

See `docs/GIT_BACKUP_STRATEGY.md` for details.

---

## 🐛 Known Issues

Currently: **None** ✅

All features tested and working.

---

## 🚧 Roadmap

### Phase 2: UI Enhancements (In Progress)
- [ ] Season Header with series name
- [ ] Total size summary
- [ ] Grid/Card layout
- [ ] Enhanced animations
- [ ] Multiple themes

### Phase 3: Advanced Features
- [ ] Download history
- [ ] Batch download queue
- [ ] Resume/Pause support
- [ ] Auto-retry failed downloads

---

## 📝 Documentation

- **Full Documentation**: `docs/DOCUMENTATION.md`
- **Stable Version Info**: `docs/STABLE_VERSION.md`
- **Git Strategy**: `docs/GIT_BACKUP_STRATEGY.md`
- **Testing Guide**: `docs/MANUAL_TESTING_GUIDE.md`
- **Test Results**: `docs/TESTING_RESULTS.md`

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

**Made with ❤️ for the Arabic Toons community**

**Version**: v1.0-stable | **Status**: ✅ Production Ready
