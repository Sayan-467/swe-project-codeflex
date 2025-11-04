"""
Test script for CodeChef editorial extraction
Tests with known problems to verify scraper functionality
"""
import cc_editorial as cce

def test_url_parsing():
    """Test URL parsing for different formats"""
    print("\n" + "="*60)
    print("TEST 1: URL Parsing")
    print("="*60)
    
    test_cases = [
        "https://www.codechef.com/problems/FLOW001",
        "https://www.codechef.com/START159A/problems/MAXFUN",
        "https://www.codechef.com/problems/TEST?tab=editorial",
    ]
    
    for url in test_cases:
        result = cce.parse_problem_url(url)
        print(f"\nURL: {url}")
        print(f"Parsed: {result}")
    
    print("\n✓ URL parsing test complete")

def test_editorial_extraction():
    """Test editorial extraction with a known problem"""
    print("\n" + "="*60)
    print("TEST 2: Editorial Extraction")
    print("="*60)
    
    # TEST is a simple problem that usually has an editorial
    test_url = "https://www.codechef.com/problems/TEST"
    
    print(f"\nTesting with: {test_url}")
    print("This may take 5-10 seconds (Selenium startup)...\n")
    
    try:
        result = cce.get_editorial(test_url)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return False
        
        print("✓ Successfully fetched problem!")
        print(f"\nProblem Details:")
        print(f"  Code: {result['problem'].get('problem_code')}")
        print(f"  Name: {result['problem'].get('name')}")
        print(f"  Difficulty: {result['problem'].get('difficulty')}")
        print(f"  Tags: {result['problem'].get('tags')}")
        
        if result.get('editorial_available'):
            print(f"\n✓ Editorial found!")
            editorial = result.get('editorial_text', '')
            print(f"  Length: {len(editorial)} characters")
            print(f"\n  Preview (first 300 chars):")
            print(f"  {editorial[:300]}...")
        else:
            print(f"\n⚠️  Editorial not found for this problem")
            print(f"  Message: {result.get('message', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Exception during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_metadata_only():
    """Test metadata extraction (faster, no editorial)"""
    print("\n" + "="*60)
    print("TEST 3: Metadata Extraction Only")
    print("="*60)
    
    test_url = "https://www.codechef.com/problems/FLOW001"
    
    print(f"\nTesting with: {test_url}")
    print("Extracting metadata only (faster)...\n")
    
    try:
        parsed = cce.parse_problem_url(test_url)
        if not parsed:
            print("❌ Failed to parse URL")
            return False
        
        problem_code = parsed["problem_code"]
        contest_code = parsed.get("contest_code")
        
        html = cce.fetch_problem_page(problem_code, contest_code)
        metadata = cce.extract_problem_metadata(html, problem_code)
        
        print("✓ Metadata extracted!")
        print(f"\nProblem Details:")
        print(f"  Code: {metadata.get('problem_code')}")
        print(f"  Name: {metadata.get('name')}")
        print(f"  Difficulty: {metadata.get('difficulty')}")
        print(f"  Tags: {metadata.get('tags')}")
        print(f"  Success Rate: {metadata.get('success_rate')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Exception during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 CodeChef Editorial Scraper - Test Suite")
    print("="*60)
    
    # Test 1: URL Parsing (fast, no network)
    test_url_parsing()
    
    # Test 2: Metadata Only (moderate speed)
    test_metadata_only()
    
    # Test 3: Full Editorial Extraction (slow, full Selenium)
    test_editorial_extraction()
    
    print("\n" + "="*60)
    print("✅ All tests complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Check if editorial was found successfully")
    print("2. If not, try adjusting extraction strategies in cc_editorial.py")
    print("3. Start the API server: python -m uvicorn main:app --reload --port 8001")
    print("4. Test the API: http://localhost:8001/docs")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
