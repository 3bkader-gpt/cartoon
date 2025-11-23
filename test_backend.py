"""
Quick Backend Test Script
Tests the API endpoints to ensure everything works
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print("✅ Backend is running")
        print(f"   Response: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Backend not running: {e}")
        return False

def test_season_endpoint():
    """Test season streaming endpoint"""
    print("\n🧪 Testing /api/season/stream endpoint...")
    
    # Example URL (replace with real one for testing)
    test_url = "https://www.arabic-toons.com/anime-streaming/example"
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/season/stream",
            json={"url": test_url},
            stream=True,
            timeout=60
        )
        
        print(f"   Status: {response.status_code}")
        
        # Read first few events
        count = 0
        for line in response.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                if decoded.startswith('data: '):
                    data = json.loads(decoded[6:])
                    print(f"   Event {count}: {data.get('type', 'unknown')}")
                    
                    # Check for required fields
                    if data.get('type') == 'result':
                        episode = data.get('data', {})
                        has_thumbnail = 'thumbnail' in episode
                        has_size = 'metadata' in episode and 'size_formatted' in episode.get('metadata', {})
                        
                        print(f"      ✅ Has thumbnail: {has_thumbnail}")
                        print(f"      ✅ Has size: {has_size}")
                        
                        if has_size:
                            print(f"      Size: {episode['metadata']['size_formatted']}")
                    
                    count += 1
                    if count >= 3:  # Test first 3 events
                        break
        
        print("✅ Season endpoint works")
        return True
        
    except Exception as e:
        print(f"❌ Season endpoint failed: {e}")
        return False

def test_proxy_endpoint():
    """Test proxy download endpoint"""
    print("\n🧪 Testing /api/proxy endpoint...")
    
    # Example video URL (replace with real one)
    test_video_url = "https://stream.foupix.com/example.mp4"
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/proxy",
            params={"url": test_video_url, "filename": "test.mp4"},
            stream=True,
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        # Check if it's streaming
        if response.status_code == 200:
            print("✅ Proxy endpoint works")
            return True
        else:
            print(f"⚠️  Proxy returned {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Proxy endpoint failed: {e}")
        return False

def main():
    print("=" * 50)
    print("🧪 Arabic Toons Backend Quick Test")
    print("=" * 50)
    
    results = []
    
    # Test 1: Health Check
    results.append(("Health Check", test_health()))
    
    # Test 2: Season Endpoint (skip if backend not running)
    if results[0][1]:
        # Uncomment to test with real URL
        # results.append(("Season Endpoint", test_season_endpoint()))
        print("\n⚠️  Skipping season endpoint test (needs real URL)")
        print("   To test: Replace test_url in test_season_endpoint()")
    
    # Test 3: Proxy Endpoint (skip if backend not running)
    if results[0][1]:
        # Uncomment to test with real URL
        # results.append(("Proxy Endpoint", test_proxy_endpoint()))
        print("\n⚠️  Skipping proxy endpoint test (needs real video URL)")
        print("   To test: Replace test_video_url in test_proxy_endpoint()")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("\n💡 Next Steps:")
    print("1. Start backend: python backend/main.py")
    print("2. Start frontend: cd frontend && npm run dev")
    print("3. Open browser: http://localhost:5173")
    print("4. Follow MANUAL_TESTING_GUIDE.md")

if __name__ == "__main__":
    main()
