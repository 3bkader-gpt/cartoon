<div align="center">

<img src="docs/images/home.png" width="800" style="border-radius: 20px; box-shadow: 0 0 20px rgba(0,0,0,0.5);" alt="Arabic Toons Downloader" />

<br/><br/>

# 🎬 Arabic Toons Downloader

### ⚡ The Ultimate High-Performance Media Downloader

<p align="center">
  <a href="#-quick-start">
    <img src="https://img.shields.io/badge/Download-v4.2.0-00d4ff?style=for-the-badge&logo=windows&logoColor=white&labelColor=1a1a2e" alt="Download" />
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-f7df1e?style=for-the-badge&logo=star&logoColor=black&labelColor=1a1a2e" alt="License" />
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776ab?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/React-18+-61dafb?style=flat-square&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Playwright-Supported-2EAD33?style=flat-square&logo=playwright&logoColor=white" />
</p>

---

### 🚀 **Download entire series with a single click.**
**Smart Caching • Personal Library • Plex-Ready Exports**

<br/>

</div>

## ✨ Why this downloader?

<div align="center">

| 🚀 **Performance** | ❤️ **Experience** | ⚙️ **Control** |
|:---:|:---:|:---:|
| **Batch Fetching**<br/>Grab 100+ episodes instantly | **My Library**<br/>Save & sync your favorites | **Plex Naming**<br/>Auto-rename for media servers |
| **Smart Caching**<br/>SQLite-backed 24h cache | **Dark Mode**<br/>Easy on your eyes | **Direct Export**<br/>For IDM / Aria2 |

</div>

---

## 📸 Visual Tour

<table align="center" style="border: none;">
  <tr>
    <td align="center" width="33%">
      <img src="docs/images/library.png" style="border-radius: 10px; width: 100%;" />
      <br/><b>📚 My Library</b>
    </td>
    <td align="center" width="33%">
      <img src="docs/images/settings.png" style="border-radius: 10px; width: 100%;" />
      <br/><b>⚙️ Settings</b>
    </td>
    <td align="center" width="33%">
      <img src="docs/images/home.png" style="border-radius: 10px; width: 100%;" />
      <br/><b>📥 Downloader</b>
    </td>
  </tr>
</table>

---

## 🚀 Quick Start

<div align="center">

```bash
# 1. Clone & Enter
git clone https://github.com/3bkader-gpt/cartoon.git
cd cartoon

# 2. Setup Backend
pip install -r requirements.txt
playwright install chromium

# 3. Setup Frontend
cd frontend && npm install
```

**Run the App**

```bash
# Terminal 1             # Terminal 2
python backend/main.py   npm run dev
```

### [Open App ↗](http://localhost:5173)

</div>

---

## 🏗️ Under the Hood

<details>
<summary><b>Click to see Architecture Diagram</b></summary>
<br/>

```mermaid
graph TD
    User[👤 User] -->|Interacts| UI[⚛️ React Frontend]
    UI -->|API Calls| API[⚡ FastAPI Backend]
    
    subgraph Backend Services
        API -->|Check Cache| DB[(🗄️ SQLite DB)]
        API -->|Fetch Live| Scraper[🔍 Web Scraper]
        Scraper -->|Render| Browser[🎭 Playwright]
        
        DB -->|Metadata| API
        Browser -->|HTML| Scraper
    end
    
    subgraph Data Stores
        DB -- Series Table --> Cache
        DB -- Favorites Table --> Library
    end
```

</details>

---

## 🗺️ Roadmap

- [x] **v3.0** - Core Downloader (IndexedDB)
- [x] **v4.0** - Backend Migration (SQLite)
- [x] **v4.1** - Library System
- [x] **v4.2** - Settings & Customization
- [ ] **v5.0** - **Internal Download Manager** 🏗️
- [ ] **v6.0** - Multi-Source Support 🔮

---

<div align="center">

### 👨‍💻 Created by

<a href="https://github.com/3bkader-gpt">
  <img src="https://img.shields.io/badge/Mohamed%20Omar-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="Mohamed Omar" />
</a>

<br/><br/>

If you enjoy this project, please give it a ⭐ **Star**!

<br/>

![Footer](https://capsule-render.vercel.app/api?type=waving&color=auto&height=100&section=footer)

</div>
