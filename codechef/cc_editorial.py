# cc_editorial.py
import re
import time
from typing import Optional, Dict, List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def setup_selenium_driver() -> webdriver.Chrome:
    """
    Setup and return a configured Chrome WebDriver for scraping CodeChef.
    CodeChef uses Cloudflare protection, so we need a proper browser setup.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Suppress unnecessary logs
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Remove webdriver property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def parse_problem_url(url: str) -> Optional[Dict[str, str]]:
    """
    Parse CodeChef problem URL and extract problem code and contest info.
    
    Supported formats:
    - https://www.codechef.com/problems/FLOW001
    - https://www.codechef.com/START159A/problems/MAXFUN
    - https://www.codechef.com/problems/FLOW001?tab=editorial
    
    Returns:
        dict: {
            "problem_code": "FLOW001",
            "contest_code": "START159A" (optional),
            "type": "practice" | "contest"
        }
    """
    if not url:
        return None
    
    # Clean URL
    url = url.split('?')[0].rstrip('/')
    
    # Pattern 1: Practice problem - /problems/PROBLEMCODE
    m = re.search(r'/problems/([A-Z0-9_]+)$', url, re.IGNORECASE)
    if m:
        return {
            "problem_code": m.group(1).upper(),
            "contest_code": None,
            "type": "practice"
        }
    
    # Pattern 2: Contest problem - /CONTESTCODE/problems/PROBLEMCODE
    m = re.search(r'/([A-Z0-9]+)/problems/([A-Z0-9_]+)$', url, re.IGNORECASE)
    if m:
        return {
            "problem_code": m.group(2).upper(),
            "contest_code": m.group(1).upper(),
            "type": "contest"
        }
    
    return None

def fetch_problem_page(problem_code: str, contest_code: Optional[str] = None) -> str:
    """
    Fetch the problem page HTML using Selenium to bypass Cloudflare.
    
    Returns:
        str: HTML content of the problem page
    """
    driver = None
    try:
        driver = setup_selenium_driver()
        
        # Construct URL
        if contest_code:
            url = f"https://www.codechef.com/{contest_code}/problems/{problem_code}"
        else:
            url = f"https://www.codechef.com/problems/{problem_code}"
        
        print(f"Fetching CodeChef problem page: {url}")
        driver.get(url)
        
        # Wait for page to load - look for problem title or content
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
        except:
            print("Warning: Timeout waiting for h1, continuing anyway...")
        
        time.sleep(3)  # Additional wait for dynamic content
        
        page_source = driver.page_source
        driver.quit()
        return page_source
        
    except Exception as e:
        if driver:
            try:
                driver.quit()
            except:
                pass
        raise Exception(f"Error fetching problem page: {e}")

def extract_problem_metadata(html: str, problem_code: str) -> Dict:
    """
    Extract problem metadata from the HTML.
    
    Returns:
        dict: {
            "problem_code": str,
            "name": str,
            "difficulty": str,
            "tags": List[str],
            "success_rate": str (optional)
        }
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    metadata = {
        "problem_code": problem_code,
        "name": None,
        "difficulty": None,
        "tags": [],
        "success_rate": None
    }
    
    # Extract title - usually in h1 or specific class
    title_elem = soup.find('h1')
    if title_elem:
        metadata["name"] = title_elem.get_text(strip=True)
    
    # Extract difficulty - look for difficulty badges/labels
    difficulty_patterns = [
        soup.find(text=re.compile(r'Difficulty:', re.IGNORECASE)),
        soup.find('span', class_=re.compile(r'difficulty', re.IGNORECASE)),
        soup.find('div', class_=re.compile(r'difficulty', re.IGNORECASE))
    ]
    
    for pattern in difficulty_patterns:
        if pattern:
            if hasattr(pattern, 'get_text'):
                diff_text = pattern.get_text(strip=True)
            else:
                diff_text = str(pattern)
            
            # Extract difficulty level (e.g., "Easy", "Medium", "Hard")
            match = re.search(r'(Simple|Easy|Medium|Hard|Challenge)', diff_text, re.IGNORECASE)
            if match:
                metadata["difficulty"] = match.group(1).capitalize()
                break
    
    # Extract tags - look for tag containers
    tag_container = soup.find('div', class_=re.compile(r'tags?', re.IGNORECASE))
    if tag_container:
        tag_links = tag_container.find_all('a')
        metadata["tags"] = [tag.get_text(strip=True) for tag in tag_links]
    
    # Success rate - if visible
    success_elem = soup.find(text=re.compile(r'Success Rate:', re.IGNORECASE))
    if success_elem:
        parent = success_elem.parent
        if parent:
            metadata["success_rate"] = parent.get_text(strip=True)
    
    return metadata

def extract_editorial_content(html: str, problem_code: str) -> Optional[str]:
    """
    Extract editorial content from the problem page HTML.
    
    CodeChef editorials can be in different locations:
    1. In a tab/section on the problem page itself
    2. In a separate editorial link/page
    3. Not available at all
    
    Returns:
        str: Editorial text or None if not found
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    editorial_text = None
    
    # Strategy 1: Look for editorial tab content
    editorial_section = soup.find('div', {'id': re.compile(r'editorial', re.IGNORECASE)})
    if editorial_section:
        editorial_text = editorial_section.get_text(separator="\n", strip=True)
        if editorial_text and len(editorial_text) > 100:
            print(f"✓ Found editorial in tab section")
            return clean_editorial_text(editorial_text)
    
    # Strategy 2: Look for editorial in problem body with specific markers
    # Sometimes editorials are in the same container as problem statement
    problem_body = soup.find('div', class_=re.compile(r'problem-statement|problem_description', re.IGNORECASE))
    if problem_body:
        # Look for "Editorial" or "Solution" headers
        headers = problem_body.find_all(['h2', 'h3', 'h4'])
        for header in headers:
            header_text = header.get_text(strip=True).lower()
            if 'editorial' in header_text or 'solution' in header_text or 'explanation' in header_text:
                # Extract all content after this header until next major section
                editorial_parts = []
                for sibling in header.find_next_siblings():
                    if sibling.name in ['h2', 'h3'] and sibling != header:
                        break
                    editorial_parts.append(sibling.get_text(separator="\n", strip=True))
                
                editorial_text = "\n".join(editorial_parts)
                if editorial_text and len(editorial_text) > 100:
                    print(f"✓ Found editorial after header: {header_text}")
                    return clean_editorial_text(editorial_text)
    
    # Strategy 3: Look for editorial link that we need to follow
    editorial_link = soup.find('a', href=re.compile(r'editorial|discuss', re.IGNORECASE))
    if editorial_link:
        href = editorial_link.get('href', '')
        print(f"Found editorial link: {href}")
        # This would require another Selenium fetch
        # For now, we'll note it but not follow (to avoid excessive requests)
        return f"Editorial available at link: {href}"
    
    # Strategy 4: Look for any section with substantial content containing solution keywords
    all_divs = soup.find_all('div')
    for div in all_divs:
        text = div.get_text(separator="\n", strip=True)
        # Check if this div contains solution-like content
        solution_keywords = ['approach', 'solution', 'algorithm', 'complexity', 'time complexity']
        if any(keyword in text.lower() for keyword in solution_keywords) and len(text) > 200:
            # Make sure this isn't just the problem statement
            if 'input format' not in text.lower() or text.count('\n') > 20:
                editorial_text = text
                print(f"✓ Found potential editorial content (heuristic match)")
                return clean_editorial_text(editorial_text)
    
    print("✗ No editorial content found")
    return None

def fetch_editorial_from_link(editorial_url: str) -> Optional[str]:
    """
    Fetch editorial content from a separate editorial page/link.
    Used when the editorial is not on the problem page itself.
    """
    driver = None
    try:
        driver = setup_selenium_driver()
        
        if not editorial_url.startswith('http'):
            editorial_url = f"https://www.codechef.com{editorial_url}"
        
        print(f"Fetching editorial from link: {editorial_url}")
        driver.get(editorial_url)
        
        time.sleep(4)  # Wait for content
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract main content
        content = soup.find('div', class_=re.compile(r'editorial|content|post', re.IGNORECASE))
        if content:
            text = content.get_text(separator="\n", strip=True)
            driver.quit()
            return clean_editorial_text(text)
        
        # Fallback: get all text
        text = soup.get_text(separator="\n", strip=True)
        driver.quit()
        return clean_editorial_text(text[:15000])
        
    except Exception as e:
        if driver:
            try:
                driver.quit()
            except:
                pass
        print(f"Error fetching editorial link: {e}")
        return None

def clean_editorial_text(text: str) -> str:
    """
    Clean up editorial text to make it more readable.
    Removes excessive whitespace, cleans up formatting artifacts, etc.
    """
    if not text:
        return ""
    
    # Remove excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove excessive spaces
    text = re.sub(r' {2,}', ' ', text)
    
    # Clean up common artifacts
    text = text.replace('\\n', ' ')
    text = re.sub(r'\s+([,.])', r'\1', text)
    
    # Remove lines with only special characters or very short lines that are likely artifacts
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # Keep empty lines for paragraph breaks
        if not stripped:
            if cleaned_lines and cleaned_lines[-1].strip():
                cleaned_lines.append('')
            continue
        
        # Skip very short lines that are likely artifacts (but keep single-letter problem labels)
        if len(stripped) <= 2 and not re.match(r'^[A-Z]$|^\d+$', stripped):
            continue
        
        cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)
    
    # Final cleanup
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    
    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    return text.strip()

def get_editorial(problem_url: str) -> Dict:
    """
    Main function to get editorial for a CodeChef problem.
    
    Args:
        problem_url: CodeChef problem URL
    
    Returns:
        dict: {
            "problem": metadata dict,
            "editorial_text": str or None,
            "error": str (if any)
        }
    """
    try:
        # Parse URL
        parsed = parse_problem_url(problem_url)
        if not parsed:
            return {"error": "Invalid CodeChef problem URL format"}
        
        problem_code = parsed["problem_code"]
        contest_code = parsed.get("contest_code")
        
        print(f"\n{'='*60}")
        print(f"Fetching editorial for: {problem_code}")
        if contest_code:
            print(f"Contest: {contest_code}")
        print(f"{'='*60}\n")
        
        # Fetch problem page
        html = fetch_problem_page(problem_code, contest_code)
        
        # Extract metadata
        metadata = extract_problem_metadata(html, problem_code)
        print(f"Problem: {metadata.get('name', 'Unknown')}")
        print(f"Difficulty: {metadata.get('difficulty', 'Unknown')}")
        
        # Extract editorial
        editorial_text = extract_editorial_content(html, problem_code)
        
        result = {
            "problem": metadata,
            "editorial_text": editorial_text,
            "editorial_available": editorial_text is not None and len(editorial_text) > 50
        }
        
        if not result["editorial_available"]:
            result["message"] = "Editorial not found or not yet published for this problem"
        
        return result
        
    except Exception as e:
        return {
            "error": f"Error fetching editorial: {str(e)}",
            "problem": {"problem_code": problem_url}
        }

# Test function
if __name__ == "__main__":
    # Test with a known problem
    test_url = "https://www.codechef.com/problems/FLOW001"
    result = get_editorial(test_url)
    
    print("\n" + "="*60)
    print("RESULT:")
    print("="*60)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Problem: {result['problem']}")
        print(f"\nEditorial Available: {result.get('editorial_available', False)}")
        if result.get('editorial_text'):
            print(f"\nEditorial Preview (first 500 chars):")
            print(result['editorial_text'][:500])
        else:
            print("\nNo editorial found")
