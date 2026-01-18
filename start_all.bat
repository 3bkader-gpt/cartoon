@echo off
echo ========================================
echo   Cartoon Downloader - Starting All
echo ========================================
echo.

echo [1/2] Starting Backend...
start "Backend Server" cmd /k "cd backend && python main.py"
timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend...
start "Frontend Dev Server" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   Both servers started!
echo ========================================
echo   Backend:  http://127.0.0.1:8000
echo   Frontend: http://localhost:5173
echo ========================================
echo.
echo Press any key to exit this window...
pause >nul
