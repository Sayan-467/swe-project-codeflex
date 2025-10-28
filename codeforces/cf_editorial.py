# cf_editorial.py
import re
import requests
import time
import hashlib
import random
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from typing import Optional, Dict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables
load_dotenv()

CF_API_BASE = "https://codeforces.com/api"
CF_API_KEY = os.getenv("CODEFORCES_API_KEY")
CF_API_SECRET = os.getenv("CODEFORCES_API_SECRET")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

def generate_api_sig(method_name: str, params: dict) -> str:
    """
    Generate API signature for authenticated Codeforces API calls.
    Format: apiSig = sha512(123456/methodName?param1=value1&...&apiKey={key}#{secret})
    where 123456 is random 6-digit number
    """
    rand = str(random.randint(100000, 999999))
    
    # Sort params alphabetically
    sorted_params = sorted(params.items())
    param_str = "&".join([f"{k}={v}" for k, v in sorted_params])
    
    # Create signature string
    sig_str = f"{rand}/{method_name}?{param_str}#{CF_API_SECRET}"
    
    # Generate SHA-512 hash
    sig_hash = hashlib.sha512(sig_str.encode('utf-8')).hexdigest()
    
    return rand, sig_hash

def call_cf_api_authenticated(method: str, params: dict = None) -> dict:
    """
    Make an authenticated call to Codeforces API
    """
    if params is None:
        params = {}
    
    # Add API key
    params['apiKey'] = CF_API_KEY
    params['time'] = str(int(time.time()))
    
    # Generate signature
    rand, sig = generate_api_sig(method, params)
    params['apiSig'] = f"{rand}{sig}"
    
    url = f"{CF_API_BASE}/{method}"
    
    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json()
    except Exception as e:
        return {"status": "FAILED", "error": str(e)}

def search_blog_entries_for_contest(contest_id: str) -> list:
    """
    Search for blog entries that might contain editorial for the contest.
    Strategy: Get contest name, extract round number, search for editorials.
    """
    found_links = []
    
    # Step 1: Get the contest name to extract round number
    contest_name = None
    round_number = None
    
    try:
        # Use contest.standings to get contest info (lighter than contest.list)
        result = call_cf_api_authenticated("contest.standings", 
                                          {"contestId": contest_id, "from": "1", "count": "1"})
        if result.get("status") == "OK":
            contest_info = result.get("result", {}).get("contest", {})
            contest_name = contest_info.get("name", "")
            print(f"Contest: {contest_name}")
            
            # Extract round number (e.g., "Round 826" from "Codeforces Round 826 (Div. 3)")
            import re
            match = re.search(r'Round (\d+)', contest_name)
            if match:
                round_number = match.group(1)
                print(f"Round number: {round_number}")
    except Exception as e:
        print(f"Error getting contest info: {e}")
    
    # Step 2: Search for editorial using round number
    if round_number:
        editorial_authors = ["awoo", "BledDest", "Neon", "vovuh"]
        
        for author in editorial_authors:
            try:
                result = call_cf_api_authenticated("user.blogEntries", {"handle": author})
                
                if result.get("status") == "OK":
                    entries = result.get("result", [])
                    
                    # Only check recent entries (last 50)
                    for entry in entries[:50]:
                        import re
                        title = entry.get("title", "")
                        title_clean = re.sub(r'<.*?>', '', title).lower()
                        
                        # Check if title contains the round number and editorial/tutorial
                        if (round_number in title_clean and 
                            ("editorial" in title_clean or "tutorial" in title_clean or "разбор" in title_clean)):
                            
                            blog_id = entry.get("id")
                            blog_url = f"https://codeforces.com/blog/entry/{blog_id}"
                            print(f"Found editorial: {re.sub(r'<.*?>', '', title)}")
                            found_links.append(blog_url)
                            break  # Found it, no need to check more entries from this author
                            
                time.sleep(0.2)  # Rate limiting
            except Exception as e:
                print(f"Error checking {author}: {e}")
                continue
    
    return found_links

def get_tutorial_link_with_selenium(contest_id: str, index: str) -> Optional[str]:
    """
    Use Selenium to fetch the problem page and find the tutorial link.
    Returns the tutorial blog URL if found.
    """
    try:
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Try both contest and problemset URLs
        urls_to_try = [
            f"https://codeforces.com/contest/{contest_id}/problem/{index}",
            f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
        ]
        
        tutorial_url = None
        
        for url in urls_to_try:
            try:
                print(f"Fetching with Selenium: {url}")
                driver.get(url)
                time.sleep(2)  # Wait for page to load
                
                # Look for tutorial link
                # Common patterns: text="Tutorial", text="Editorial", contains "blog/entry"
                try:
                    # Try to find link with text "Tutorial"
                    tutorial_link = driver.find_element(By.LINK_TEXT, "Tutorial")
                    tutorial_url = tutorial_link.get_attribute("href")
                    print(f"Found tutorial link: {tutorial_url}")
                    break
                except:
                    pass
                
                try:
                    # Try partial link text
                    tutorial_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Tutorial")
                    tutorial_url = tutorial_link.get_attribute("href")
                    print(f"Found tutorial link: {tutorial_url}")
                    break
                except:
                    pass
                
                # If not found, look for any link with "blog/entry" or "blog/" in page
                try:
                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, "html.parser")
                    
                    for a in soup.find_all("a", href=True):
                        text = a.get_text(strip=True).lower()
                        href = a.get("href", "")
                        
                        # Look for tutorial/editorial links that point to blog
                        if ("tutorial" in text or "editorial" in text) and ("/blog/" in href):
                            if href.startswith("/"):
                                tutorial_url = "https://codeforces.com" + href
                            else:
                                tutorial_url = href
                            print(f"Found tutorial link in page source: {tutorial_url}")
                            break
                    
                    if tutorial_url:
                        break
                except Exception as e:
                    print(f"Error parsing page source: {e}")
                
            except Exception as e:
                print(f"Error loading {url}: {e}")
                continue
        
        driver.quit()
        return tutorial_url
        
    except Exception as e:
        print(f"Selenium error: {e}")
        return None

def fetch_blog_text_with_selenium(blog_url: str) -> str:
    """
    Use Selenium to fetch blog content (since direct requests are blocked).
    """
    driver = None
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Suppress logs
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print(f"Fetching blog with Selenium: {blog_url}")
        driver.get(blog_url)
        time.sleep(4)  # Wait for content to load (increased wait time)
        
        page_source = driver.page_source
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")
        
        # Look for blog content - try multiple possible containers
        content_div = soup.find("div", class_="ttypography")
        if content_div:
            text = content_div.get_text(separator="\n").strip()
            driver.quit()
            return clean_editorial_text(text)
        
        # Try finding the main content area
        content_div = soup.find("div", class_="topic")
        if content_div:
            text = content_div.get_text(separator="\n").strip()
            driver.quit()
            return clean_editorial_text(text)
        
        # Try blog entry container
        content_div = soup.find("div", class_="content")
        if content_div:
            text = content_div.get_text(separator="\n").strip()
            driver.quit()
            return clean_editorial_text(text)
        
        # Fallback: get all text
        text = soup.get_text(separator="\n").strip()
        driver.quit()
        return clean_editorial_text(text[:20000])  # Limit to 20k chars
        
    except Exception as e:
        if driver:
            try:
                driver.quit()
            except:
                pass
        return f"Error fetching blog with Selenium: {e}"

def clean_editorial_text(text: str) -> str:
    """
    Clean up the editorial text to make it more readable.
    Removes excessive newlines, cleans up LaTeX artifacts, etc.
    """
    import re
    
    # First pass: replace multiple consecutive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Clean up isolated variables and LaTeX artifacts
    # Pattern: word \n single_char \n word -> word single_char word
    text = re.sub(r'(\w)\s*\n\s*([A-Za-z])\s*\n\s*(\w)', r'\1 \2 \3', text)
    
    # Pattern: \n single_char \n -> remove the character if it's likely LaTeX variable
    # But be careful not to remove problem indices (A, B, C at start of lines)
    text = re.sub(r'(?<!^)(?<!\n)\n([a-z])\n(?!\n)', r' ', text, flags=re.MULTILINE)
    
    # Clean up code blocks and excessive whitespace in code
    # Replace patterns like "(\n)" with "()" in code contexts
    text = re.sub(r'\(\s*\n\s*\)', '()', text)
    text = re.sub(r'\[\s*\n\s*\]', '[]', text)
    text = re.sub(r'{\s*\n\s*}', '{}', text)
    
    # Clean up spaces before punctuation
    text = re.sub(r'\s+([,.])', r'\1', text)
    
    # Remove literal \n strings
    text = text.replace('\\n', ' ')
    
    # Clean up mathematical symbols
    text = re.sub(r'\s*⋅\s*', ' * ', text)
    text = re.sub(r'\s*≠\s*', ' != ', text)
    text = re.sub(r'\s*≤\s*', ' <= ', text)
    text = re.sub(r'\s*≥\s*', ' >= ', text)
    text = re.sub(r'\s*→\s*', ' -> ', text)
    
    # Clean up lines with only single characters or short fragments
    lines = text.split('\n')
    cleaned_lines = []
    skip_next = False
    
    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue
            
        stripped = line.strip()
        
        # Keep empty lines for paragraph breaks
        if not stripped:
            # Only add empty line if previous line wasn't empty
            if cleaned_lines and cleaned_lines[-1].strip():
                cleaned_lines.append('')
            continue
        
        # Check if this is a problem header (like "1741A - Problem Name")
        if re.match(r'^\d+[A-Z]\s*-', stripped):
            # Add extra line break before problem headers for readability
            if cleaned_lines and cleaned_lines[-1].strip():
                cleaned_lines.append('')
            cleaned_lines.append(line)
            continue
        
        # Skip lines with only 1-2 characters that are likely LaTeX artifacts
        # Exception: Keep lines that look like they're part of a list or important markers
        if len(stripped) <= 2 and not re.match(r'^[A-Z]$|^\d+$|^-$|^\*$', stripped):
            # Check if next line or previous line has content - if so, try to merge
            if i < len(lines) - 1:
                next_stripped = lines[i + 1].strip()
                if next_stripped and len(next_stripped) > 3:
                    # Merge with next line
                    lines[i + 1] = stripped + ' ' + next_stripped
                    continue
            # Otherwise skip
            continue
        
        cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)
    
    # Replace multiple spaces with single space
    text = re.sub(r' {2,}', ' ', text)
    
    # Normalize paragraph breaks (max 2 newlines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    # Final cleanup
    text = re.sub(r' {2,}', ' ', text)
    
    return text.strip()

def parse_problem_url(url: str) -> Optional[Dict[str,str]]:
    """
    Accepts:
      https://codeforces.com/contest/1741/problem/B
      https://codeforces.com/problemset/problem/1741/B
      https://codeforces.com/contest/1741/B
    Returns dict {contest_id: '1741', index: 'B'} or None
    """
    if not url:
        return None

    # Normalize url (strip query + trailing slash)
    url = url.split('?')[0].rstrip('/')

    # patterns to match:
    m = re.search(r'/contest/(\d+)(?:/problem/|/)([A-Za-z0-9]+)$', url)
    if not m:
        m = re.search(r'/problemset/problem/(\d+)/([A-Za-z0-9]+)$', url)
    if not m:
        # sometimes they use /problem/ path
        m = re.search(r'/problem/(\d+)/([A-Za-z0-9]+)$', url)
    if not m:
        return None

    return {"contest_id": m.group(1), "index": m.group(2)}

def fetch_problem_metadata(contest_id: str, index: str) -> dict:
    """
    Uses Codeforces API to fetch problem metadata (name, tags, statement snippets).
    """
    # We can call problemset.problems and filter or call contest.standings to get exact problem.
    url = f"{CF_API_BASE}/contest.standings?contestId={contest_id}&from=1&count=1"
    r = requests.get(url, headers=HEADERS, timeout=10)
    data = r.json()
    if data.get("status") != "OK":
        return {"error": "CF API failed", "raw": data}

    # find the problem by index
    problems = data["result"]["problems"]
    for p in problems:
        if p.get("index") == index:
            return {
                "contestId": contest_id,
                "index": index,
                "name": p.get("name"),
                "tags": p.get("tags"),
                "problem_api_object": p
            }

    return {"error": "Problem not found in contest.standings response", "raw_problems": problems}

def find_tutorial_links_for_problem(contest_id: str, index: str) -> list:
    """
    Find tutorial/editorial links for a problem using multiple methods:
    1. Use Selenium to scrape problem page for tutorial link (primary method)
    2. Search blog entries via authenticated API (backup)
    """
    found = set()
    
    # Method 1: Use Selenium to get tutorial link from problem page
    print(f"Using Selenium to find tutorial link for {contest_id}/{index}...")
    selenium_link = get_tutorial_link_with_selenium(contest_id, index)
    if selenium_link:
        found.add(selenium_link)
        print(f"✓ Found tutorial via Selenium: {selenium_link}")
        # Return immediately since we found the direct link
        return sorted(found)
    
    # Method 2: Fallback to API search
    print(f"Selenium didn't find tutorial, trying API search...")
    api_links = search_blog_entries_for_contest(contest_id)
    for link in api_links:
        found.add(link)
        print(f"Found via API: {link}")
    
    print(f"Total editorial links found: {len(found)}")
    return sorted(found)

def fetch_blog_text(blog_url: str) -> str:
    """
    Fetch blog content using Selenium (since direct requests are blocked).
    """
    return fetch_blog_text_with_selenium(blog_url)
