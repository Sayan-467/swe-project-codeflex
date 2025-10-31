"""
Quick test script for CodeChef API with START209A/P5209
Run this while the server is running in another terminal
"""
import requests
import json
import time

BASE_URL = "http://localhost:8001"
TEST_URL = "https://www.codechef.com/START209A/problems/P5209"

def test_health():
    """Test 1: Health check"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ Response: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_metadata():
    """Test 2: Metadata extraction"""
    print("\n" + "="*60)
    print("TEST 2: Metadata Extraction")
    print("="*60)
    print(f"Problem: {TEST_URL}")
    print("This may take 5-10 seconds (Selenium loading)...\n")
    
    try:
        start = time.time()
        response = requests.get(
            f"{BASE_URL}/metadata",
            params={"problem_url": TEST_URL},
            timeout=60
        )
        elapsed = time.time() - start
        
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ Response Time: {elapsed:.2f}s")
        print(f"\n📊 Response Data:")
        print(json.dumps(response.json(), indent=2))
        return True
    except requests.exceptions.Timeout:
        print("✗ Request timed out (>60s)")
        print("  This can happen on first run (downloading ChromeDriver)")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_fetch_editorial():
    """Test 3: Fetch editorial"""
    print("\n" + "="*60)
    print("TEST 3: Fetch Editorial")
    print("="*60)
    print(f"Problem: {TEST_URL}")
    print("This may take 8-10 seconds...\n")
    
    try:
        start = time.time()
        response = requests.get(
            f"{BASE_URL}/fetch/editorial",
            params={"problem_url": TEST_URL},
            timeout=60
        )
        elapsed = time.time() - start
        
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ Response Time: {elapsed:.2f}s")
        
        data = response.json()
        
        if "error" in data:
            print(f"\n⚠️  Error: {data['error']}")
            if "message" in data:
                print(f"   Message: {data['message']}")
        else:
            print(f"\n📊 Response Data:")
            print(f"Editorial Available: {data.get('editorial_available', False)}")
            if data.get('editorial_preview'):
                print(f"\nEditorial Preview (first 500 chars):")
                print(data['editorial_preview'][:500])
                print(f"\n... (total length: {data.get('editorial_length', 0)} chars)")
        
        return True
    except requests.exceptions.Timeout:
        print("✗ Request timed out (>60s)")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_generate_hints():
    """Test 4: Generate hints (requires .env with API key)"""
    print("\n" + "="*60)
    print("TEST 4: Generate Hints")
    print("="*60)
    print(f"Problem: {TEST_URL}")
    print("This may take 10-15 seconds (scraping + AI)...\n")
    
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/generate/hints",
            json={"problem_url": TEST_URL},
            timeout=90
        )
        elapsed = time.time() - start
        
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ Response Time: {elapsed:.2f}s")
        
        data = response.json()
        
        if "error" in data:
            print(f"\n⚠️  Error: {data['error']}")
            if "message" in data:
                print(f"   Message: {data['message']}")
        else:
            print(f"\n📊 Response Data:")
            print(f"Problem: {data.get('problem', {})}")
            print(f"\nGenerated Hints:")
            print(data.get('generated_hints', 'No hints'))
        
        return True
    except requests.exceptions.Timeout:
        print("✗ Request timed out (>90s)")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🧪 CodeChef API Test Suite")
    print("="*60)
    print(f"Server: {BASE_URL}")
    print(f"Test Problem: {TEST_URL}")
    print("="*60)
    
    # Run tests
    results = []
    
    results.append(("Health Check", test_health()))
    results.append(("Metadata Extraction", test_metadata()))
    results.append(("Fetch Editorial", test_fetch_editorial()))
    
    # Optional: Generate hints (requires API key in .env)
    print("\n" + "="*60)
    print("Optional: Test hint generation? (requires API key in .env)")
    print("="*60)
    user_input = input("Run hint generation test? (y/n): ").lower()
    if user_input == 'y':
        results.append(("Generate Hints", test_generate_hints()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*60)
    print("Next Steps:")
    print("="*60)
    print("1. Check results above")
    print("2. If editorial not found, try a different problem")
    print("3. Use Thunder Client in VS Code for interactive testing")
    print("4. See THUNDER_CLIENT_GUIDE.md for detailed instructions")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
