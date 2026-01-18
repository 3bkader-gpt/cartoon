# 🚀 Quick Start Guide

## Running the Application

### Option 1: Using Batch Scripts (Easiest)

#### Start Both (Backend + Frontend):
```bash
.\start_all.bat
```
This will open 2 separate windows for backend and frontend.

#### Start Backend Only:
```bash
.\start_backend.bat
```

---

### Option 2: Manual Start

#### Backend (Terminal 1):
```bash
cd backend
python main.py
```
Server runs on: http://127.0.0.1:8000

#### Frontend (Terminal 2):
```bash
cd frontend
npm run dev
```
Dev server runs on: http://localhost:5173

---

### Option 3: With Virtual Environment

#### Activate venv first:
```bash
.venv\Scripts\activate
```

#### Then start backend:
```bash
cd backend
python main.py
```

---

## Access the Application

Open your browser: **http://localhost:5173**

---

## Troubleshooting

### Backend won't start?
- Make sure you're in the `backend` directory when running `python main.py`
- Check that all dependencies are installed: `pip install -r backend/requirements.txt`
- Verify Playwright is installed: `playwright install chromium`

### Frontend won't start?
- Make sure you're in the `frontend` directory
- Install dependencies: `npm install`
- Try: `npm run dev`

### Port already in use?
- Backend (8000): Check if another process is using port 8000
- Frontend (5173): Check if another Vite server is running

---

## Testing

### Test Arabic Toons:
1. Go to http://localhost:5173
2. Paste a series URL from arabic-toons.com
3. Click "Fetch Episodes"
4. Wait for episodes to load
5. Download or export as needed

### Example URL:
```
https://www.arabic-toons.com/%D9%86%D8%A7%D8%B1%D9%88%D8%AA%D9%88-SD-1693251401-anime-streaming.html
```

---

**Made with ❤️ for the Arabic cartoon community**
