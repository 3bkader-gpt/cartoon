"""Test the API directly"""
import requests

url = "http://127.0.0.1:8000/api/season/stream"
params = {"url": "https://www.arabic-toons.com/%D8%A3%D9%85%D9%8A-%D9%86%D8%A8%D8%B9-%D8%A7%D9%84%D8%AD%D9%86%D8%A7%D9%86-1446454962-anime-streaming.html"}

print("Testing API...")
print(f"URL: {url}")
print(f"Params: {params}")

try:
    response = requests.get(url, params=params, stream=True, timeout=60)
    print(f"Status: {response.status_code}")
    
    for line in response.iter_lines():
        if line:
            print(f"Response: {line.decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
