<div align="center">

# ⚡ Arabic Toons Downloader (cartoon)

### Media Downloader Platform for Arabic Cartoons - Full-Stack Web Application

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)

**Download Full Series & Episodes • Library Management • High-Performance Scraping**

[Features](#-features) • [Architecture](#-architecture) • [Docker Deployment](#-docker-deployment) • [Local Development](#-local-development)

</div>

---

## 🎯 Overview

This project is a **full‑stack platform** for downloading and managing Arabic cartoon series from [Arabic-Toons](https://www.arabic-toons.com/). It allows you to:

- Paste a series/episode URL
- Fetch all episodes automatically via Playwright-based scraping
- Manage a local library of downloaded series
- Re-open the downloads folder directly from the UI

Backend is built with **FastAPI + Playwright** and frontend with **React + Vite + TailwindCSS**.

---

## 🌟 Features

- ⚡ **Full series downloader**: download entire seasons with a single click
- 🧠 **Smart caching**: avoid re-scraping the same series unnecessarily
- 📚 **Library view**: list of previously downloaded series with quick actions
- 🔍 **Search & filters** for library entries
- 🧱 **Robust scraping layer** using Playwright
- 🐳 **Docker Compose** setup for production-like deployment

---

## 🏗 Architecture

- `backend/` – FastAPI app, Playwright scraping, SQLite DB (`cartoon.db` / `anime_cache.db`)
- `frontend/` – React single-page app built with Vite & TailwindCSS
- `Dockerfile` (root) – legacy image (kept for backward compatibility)
- `backend/Dockerfile` – backend-only image for Docker Compose
- `frontend/Dockerfile` – nginx-based image serving built frontend and proxying `/api` to backend
- `docker-compose.yml` – runs `backend` + `frontend` services together

---

## 🐳 Docker Deployment

### Prerequisites

- Docker
- Docker Compose plugin (`docker compose`)

### Quick Start

```bash
# Clone repository
git clone https://github.com/3bkader-gpt/cartoon.git
cd cartoon

# Build and start in detached mode
docker compose up -d --build
```

This will start:

- **backend** on internal port `8000` (exposed as `8020` on host)
- **frontend** on internal port `80` (exposed as `8021` on host)

So you can access the UI at:

```text
http://<server-ip>:8021/
```

### Useful Commands

```bash
# View running containers
docker compose ps

# View logs
docker compose logs -f

# Stop and remove containers
docker compose down
```

---

## 💻 Local Development (without Docker)

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the API (FastAPI + Playwright)
uvicorn main:app --host 127.0.0.1 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 3000
```

By default the frontend reads `VITE_API_URL` from environment, and falls back to the **same origin** (or `http://127.0.0.1:8000` in development). For local dev, you can create `.env` in `frontend/`:

```bash
VITE_API_URL=http://127.0.0.1:8000
```

---

## 📁 Data & Persistence

The Docker Compose file mounts the following volumes:

- `./downloads` → `/app/downloads`
- `./anime_cache.db` → `/app/anime_cache.db`
- `./cartoon.db` → `/app/cartoon.db`

This keeps downloaded files and database files on the host machine so they survive container restarts.

---

## ⚠️ Disclaimer

This project is for **educational purposes only**. Please respect the terms of service and copyright policies of source sites (e.g. Arabic-Toons) and only download content you are legally allowed to.

---

## 📜 License

This project is open-source under the MIT License.
