<div align="center">

# 🎬 Arabic Toons Downloader

<img src="docs/images/home.png" width="600" alt="Arabic Toons Downloader" />

### ⚡ Lightning-Fast Media Downloader for Arabic Cartoons

[![Version](https://img.shields.io/badge/version-4.2.0-00d4ff?style=for-the-badge&labelColor=1a1a2e)](https://github.com/3bkader-gpt/cartoon)
[![Python](https://img.shields.io/badge/Python-3.12+-3776ab?style=for-the-badge&logo=python&logoColor=white&labelColor=1a1a2e)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61dafb?style=for-the-badge&logo=react&logoColor=white&labelColor=1a1a2e)](https://react.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=1a1a2e)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-f7df1e?style=for-the-badge&labelColor=1a1a2e)](LICENSE)

<br/>

[✨ Features](#-features) •
[🚀 Quick Start](#-quick-start) •
[📸 Screenshots](#-screenshots) •
[🏗️ Architecture](#️-architecture) •
[📖 Documentation](#-documentation)

---

**Download entire cartoon series with a single click.**  
**Smart caching • Library management • Plex-ready exports**

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🚀 Core Power
```
✅ Batch episode fetching
✅ Parallel metadata retrieval
✅ Smart SQLite caching (24h freshness)
✅ IDM & Aria2 export formats
✅ Direct download links
```

</td>
<td width="50%">

### ❤️ Library Management
```
✅ Favorites system
✅ One-click series access
✅ Automatic metadata sync
✅ Thumbnail previews
✅ Episode count tracking
```

</td>
</tr>
<tr>
<td width="50%">

### ⚙️ Customization
```
✅ Dark / Light themes
✅ Plex/Kodi file naming
✅ Quick folder access
✅ Sorting & filtering
✅ Select all / Deselect all
```

</td>
<td width="50%">

### 🎯 Quality of Life
```
✅ Real-time progress
✅ Cache indicators
✅ Force refresh option
✅ Episode search
✅ Copy individual URLs
```

</td>
</tr>
</table>

---

## 📸 Screenshots

<div align="center">

| Home | Library | Settings |
|:---:|:---:|:---:|
| ![Home](docs/images/home.png) | ![Library](docs/images/library.png) | ![Settings](docs/images/settings.png) |
| *Main downloader interface* | *Your favorite series* | *Customize your experience* |

</div>

---

## 🚀 Quick Start

### Prerequisites

```bash
# Required
Python 3.12+
Node.js 18+
Git
```

### Installation

```bash
# 1️⃣ Clone the repository
git clone https://github.com/3bkader-gpt/cartoon.git
cd cartoon

# 2️⃣ Install Python dependencies
pip install -r requirements.txt
playwright install chromium

# 3️⃣ Install frontend dependencies
cd frontend
npm install
cd ..
```

### Running

<table>
<tr>
<td>

**🖥️ Terminal 1 - Backend**
```bash
python backend/main.py
```

</td>
<td>

**🌐 Terminal 2 - Frontend**
```bash
cd frontend
npm run dev
```

</td>
</tr>
</table>

<div align="center">

### 🎉 Open [http://localhost:5173](http://localhost:5173) and start downloading!

</div>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         🌐 FRONTEND (React + Vite)                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────────┐   │
│  │  📥 Downloader │    │  ❤️ Library   │    │      ⚙️ Settings          │   │
│  │   Component  │    │     Page     │    │         Page             │   │
│  └───────┬──────┘    └───────┬──────┘    └────────────┬─────────────┘   │
│          └───────────────────┼────────────────────────┘                 │
│                              │ API Requests                             │
└──────────────────────────────┼──────────────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      ⚡ BACKEND (FastAPI + Python)                      │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │                    🗄️ SQLite Database                           │     │
│  │  ┌─────────────┐      ┌─────────────┐      ┌─────────────────┐ │     │
│  │  │   series    │──────│  episodes   │      │    favorites    │ │     │
│  │  │ is_favorite │      │ UNIQUE key  │      │    (legacy)     │ │     │
│  │  └─────────────┘      └─────────────┘      └─────────────────┘ │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────────────────────────┐   │
│  │  🔍 Scraper  │  │ 🎭 Playwright │  │        📡 API Endpoints        │   │
│  │    Engine   │──│   Browser   │  │  /season/stream  /library/    │   │
│  └─────────────┘  └─────────────┘  │  /open-downloads /health      │   │
│                                    └────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📡 API Reference

| Method | Endpoint | Description |
|:------:|----------|-------------|
| `GET` | `/api/season/stream` | 📺 Stream episode data |
| `GET` | `/api/library/` | ❤️ Get favorites |
| `POST` | `/api/library/toggle` | 🔄 Toggle favorite |
| `GET` | `/api/library/check` | ✅ Check if favorited |
| `GET` | `/api/search` | 🔍 Search series |
| `POST` | `/api/open-downloads` | 📁 Open downloads folder |
| `GET` | `/api/health` | 💚 Health check |

---

## 🗂️ Project Structure

```
cartoon/
├── 🐍 backend/
│   ├── api/
│   │   ├── main_router.py      # Core API
│   │   └── library_router.py   # Favorites API
│   ├── scraper/
│   │   └── scraper.py          # Web scraper
│   ├── database.py             # SQLite operations
│   └── main.py                 # App entry
│
├── ⚛️ frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── api.js
│   └── package.json
│
├── 📚 docs/
│   ├── images/
│   ├── PROJECT_STATUS.md
│   └── ROADMAP.md
│
├── 📄 README.md
├── 📄 README_AR.md
└── 📄 LICENSE
```

---

## 🗺️ Roadmap

<div align="center">

| Version | Feature | Status |
|:-------:|---------|:------:|
| v3.0 | Basic downloader + IndexedDB | ✅ |
| v4.0 | SQLite backend migration | ✅ |
| v4.1 | My Library feature | ✅ |
| v4.2 | Settings + Plex naming | ✅ |
| **v5.0** | **Internal Download Manager** | 🔜 |
| v6.0 | Multi-source support | 📋 |

</div>

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### ⭐ Star this repo if you find it useful!

<br/>

---

### 👨‍💻 Created by

<a href="https://github.com/3bkader-gpt">
  <img src="https://img.shields.io/badge/Mohamed%20Omar-Developer-blueviolet?style=for-the-badge&logo=github&logoColor=white" alt="Mohamed Omar" />
</a>

<br/><br/>

**Built with ❤️ using [FastAPI](https://fastapi.tiangolo.com) • [React](https://react.dev) • [Playwright](https://playwright.dev)**

<br/>

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Made with React](https://img.shields.io/badge/Made%20with-React-61dafb?style=flat-square&logo=react&logoColor=white)](https://react.dev)
[![Powered by FastAPI](https://img.shields.io/badge/Powered%20by-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

<br/>

**© 2026 Mohamed Omar. All rights reserved.**

</div>
