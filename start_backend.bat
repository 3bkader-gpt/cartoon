@echo off
echo ========================================
echo   Cartoon Downloader - Starting Backend
echo ========================================
echo.

cd backend
echo Starting FastAPI server...
echo Server will run on: http://127.0.0.1:8000
echo API endpoint: http://127.0.0.1:8000/api
echo.
python main.py
