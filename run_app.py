import subprocess
import sys
import os
import time
import webbrowser

def install_backend():
    print("Installing backend requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])

def install_frontend():
    print("Installing frontend requirements...")
    subprocess.check_call(["npm", "install"], cwd="frontend", shell=True)

def run_backend():
    print("Starting backend...")
    return subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.main:app", "--reload", "--port", "8000"])

def run_frontend():
    print("Starting frontend...")
    # Use shell=True for npm on Windows
    return subprocess.Popen(["npm", "run", "dev"], cwd="frontend", shell=True)

if __name__ == "__main__":
    print("Arabic Toons GUI Launcher")
    print("=========================")
    
    # Check if we need to install dependencies
    if len(sys.argv) > 1 and sys.argv[1] == "--install":
        install_backend()
        install_frontend()
    
    backend = run_backend()
    frontend = run_frontend()
    
    print("\nApp is running!")
    print("Backend: http://localhost:8000")
    print("Frontend: http://localhost:5173")
    print("\nPress Ctrl+C to stop.")
    
    # Open browser after a short delay
    time.sleep(5)
    webbrowser.open("http://localhost:5173")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
        backend.terminate()
        frontend.terminate()
