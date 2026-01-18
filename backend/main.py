import sys
from pathlib import Path

# Add parent directory to path so imports work
backend_dir = Path(__file__).parent
project_root = backend_dir.parent
sys.path.insert(0, str(project_root))

print("=" * 60, flush=True)
print("🚀 STARTING BACKEND SERVER", flush=True)
print("=" * 60, flush=True)

# Fix for Windows: Set event loop policy to support subprocesses (required for Playwright)
import asyncio
import platform
if platform.system() == "Windows":
    print("🪟 Setting Windows event loop policy for Playwright support...", flush=True)
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.main_router import router as api_router
import uvicorn
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

print("📦 Creating FastAPI app...", flush=True)
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Router
print("🔗 Including API router...", flush=True)
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    print("📍 Root endpoint called", flush=True)
    return {"status": "ok", "message": "Cartoon Downloader API v2 (Modular)"}

@app.get("/debug")
def debug_endpoint():
    print("🔍 Debug endpoint called!", flush=True)
    return {"status": "debug", "message": "Debug endpoint working!"}

print("✅ Server setup complete", flush=True)

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

