# 🍳 CodeChef Editorial Scraper & AI Hint Generator

A FastAPI-based service that scrapes CodeChef problem editorials and generates progressive learning hints using AI (Gemini or OpenAI).

## 🎯 Why This Solution?

**The Problem:**
- CodeChef **does NOT provide a public API** for accessing editorials
- Their website uses **Cloudflare protection**, blocking standard HTTP requests
- Editorials are embedded in web pages, not accessible via structured data

**The Solution:**
- **Selenium WebDriver** to bypass Cloudflare and render JavaScript content
- **BeautifulSoup** for intelligent HTML parsing
- **Multi-strategy extraction** to handle different editorial formats
- **AI-powered hint generation** that avoids spoiling the solution

---

## 🏗️ Architecture Overview

```
CodeChef Problem URL
        ↓
   [Selenium WebDriver] ← Bypasses Cloudflare protection
        ↓
   [HTML Content]
        ↓
   [BeautifulSoup Parser]
        ↓
   [Multi-Strategy Extraction]
     ├─ Strategy 1: Look for editorial tabs
     ├─ Strategy 2: Search for editorial headers
     ├─ Strategy 3: Follow editorial links
     └─ Strategy 4: Heuristic content detection
        ↓
   [Editorial Text + Metadata]
        ↓
   [AI (Gemini/OpenAI)] ← Generates progressive hints
        ↓
   [Structured Hints API Response]
```

---

## 📋 Features

### 1. **Editorial Extraction** (`cc_editorial.py`)
- ✅ Parses CodeChef problem URLs (practice + contest problems)
- ✅ Uses Selenium to bypass Cloudflare protection
- ✅ Extracts problem metadata (name, difficulty, tags)
- ✅ Multi-strategy editorial detection:
  - Editorial tabs on problem page
  - Editorial sections in problem description
  - Linked editorial pages
  - Heuristic-based content detection
- ✅ Intelligent text cleaning and formatting

### 2. **AI Hint Generation** (`main.py`)
- ✅ FastAPI REST endpoints
- ✅ Generates 3-5 progressive hints without spoiling solutions
- ✅ Supports both **Gemini** and **OpenAI** LLMs
- ✅ Metadata-only endpoint for quick problem info

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Chrome browser (for Selenium)
- API key for Gemini or OpenAI

### Installation

1. **Clone and navigate to the codechef folder:**
```powershell
cd codechef
```

2. **Install dependencies:**
```powershell
pip install -r requirements.txt
```

3. **Create a `.env` file:**
```env
# Choose one:
GEMINI_API_KEY=your_gemini_api_key_here
# OR
OPENAI_API_KEY=your_openai_api_key_here
```

4. **Run the server:**
```powershell
uvicorn main:app --reload --port 8001
```

The API will be available at: `http://localhost:8001`

---

## 📡 API Endpoints

### 1. **Root Check**
```http
GET /
```
Response:
```json
{
  "ok": true,
  "message": "CodeChef AI Hint Generator is running 🚀"
}
```

---

### 2. **Generate Hints** (Main Endpoint)
```http
POST /generate/hints
Content-Type: application/json

{
  "problem_url": "https://www.codechef.com/problems/FLOW001"
}
```

**Response:**
```json
{
  "problem": {
    "problem_code": "FLOW001",
    "name": "Add Two Numbers",
    "difficulty": "Easy",
    "tags": ["basic-math", "implementation"]
  },
  "editorial_available": true,
  "generated_hints": "**Hint 1**: Start by understanding what the problem is asking...\n\n**Hint 2**: Think about how you can read multiple test cases...\n\n**Hint 3**: Consider the most basic arithmetic operation...",
  "note": "Hints generated from scraped CodeChef editorial"
}
```

**Error Cases:**
```json
{
  "error": "Editorial not available for this problem",
  "message": "This problem may not have an editorial yet...",
  "problem": {...}
}
```

---

### 3. **Fetch Editorial** (Debug Endpoint)
```http
GET /fetch/editorial?problem_url=https://www.codechef.com/problems/FLOW001
```

Returns editorial preview (first 2000 chars) and metadata.

---

### 4. **Get Metadata Only** (Fast Endpoint)
```http
GET /metadata?problem_url=https://www.codechef.com/problems/FLOW001
```

Returns only problem metadata without extracting editorial (faster).

---

## 🔍 Supported URL Formats

| Format | Example | Type |
|--------|---------|------|
| Practice Problem | `https://www.codechef.com/problems/FLOW001` | Practice |
| Contest Problem | `https://www.codechef.com/START159A/problems/MAXFUN` | Contest |
| With Query Params | `https://www.codechef.com/problems/FLOW001?tab=editorial` | Any |

---

## 🛠️ How It Works: Editorial Extraction

### Challenge: No API Available
CodeChef doesn't provide an API for editorials. Here's how we solve it:

#### Step 1: **Selenium WebDriver Setup**
```python
# Configured to bypass Cloudflare
- Headless Chrome
- User-agent spoofing
- Automation detection removal
- Proper wait strategies
```

#### Step 2: **Multi-Strategy Extraction**

**Strategy 1: Editorial Tabs**
```python
# Look for <div id="editorial"> or similar
<div id="editorial">
  Editorial content here...
</div>
```

**Strategy 2: Editorial Headers**
```python
# Find headers like "Editorial", "Solution", "Explanation"
<h3>Editorial</h3>
<p>The approach is...</p>
```

**Strategy 3: Editorial Links**
```python
# Follow links to separate editorial pages
<a href="/editorial/FLOW001">View Editorial</a>
```

**Strategy 4: Heuristic Detection**
```python
# Search for solution-related keywords in content
Keywords: "approach", "algorithm", "complexity", "solution"
Min length: 200 characters
Filter out: input/output format sections
```

#### Step 3: **Text Cleaning**
- Remove excessive whitespace
- Clean formatting artifacts
- Normalize paragraph breaks
- Remove navigation/UI elements

---

## 🧪 Testing

### Test Editorial Extraction Directly
```powershell
cd codechef
python cc_editorial.py
```

This runs a test with a sample problem.

### Test API with curl
```powershell
# Test hints generation
curl -X POST http://localhost:8001/generate/hints `
  -H "Content-Type: application/json" `
  -d '{\"problem_url\": \"https://www.codechef.com/problems/FLOW001\"}'

# Test editorial fetch
curl "http://localhost:8001/fetch/editorial?problem_url=https://www.codechef.com/problems/FLOW001"

# Test metadata
curl "http://localhost:8001/metadata?problem_url=https://www.codechef.com/problems/FLOW001"
```

---

## 🎭 Differences from Codeforces Implementation

| Aspect | Codeforces | CodeChef |
|--------|-----------|----------|
| **API Available?** | ✅ Yes (authenticated) | ❌ No |
| **Primary Method** | API calls + Selenium fallback | Selenium only |
| **Editorial Location** | Separate blog posts | Embedded in problem pages |
| **URL Structure** | Contest + Index (e.g., 1741/B) | Problem code (e.g., FLOW001) |
| **Cloudflare Protection** | Moderate | Strong |
| **Extraction Complexity** | Medium | High |

---

## 🚧 Limitations & Known Issues

### 1. **Editorial Availability**
- Not all problems have editorials
- Some editorials are only in discuss forums (harder to extract)
- Contest editorials may be delayed

### 2. **Performance**
- Selenium adds 3-5 seconds per request (browser startup + page load)
- Cannot batch requests efficiently
- Rate limiting recommended

### 3. **Reliability**
- CodeChef may update their HTML structure (breaks scrapers)
- Cloudflare may detect and block automated access
- Network timeouts possible

### 4. **Editorial Quality**
- Extracted text may include non-editorial content
- Formatting may be inconsistent
- Code snippets may need better parsing

---

## 🔧 Configuration Options

### Environment Variables
```env
# AI Provider (choose one)
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Optional: Selenium Configuration
SELENIUM_TIMEOUT=15           # Page load timeout (seconds)
SELENIUM_HEADLESS=true        # Run browser in background
```

### Customizing AI Model
Edit `main.py`:
```python
# For Gemini
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# For OpenAI
model="gpt-4o-mini"  # or "gpt-4", "gpt-3.5-turbo"
```

---

## 📊 Performance Tips

### 1. **Optimize Selenium**
```python
# Already implemented in cc_editorial.py:
- Headless mode (no GUI)
- Minimal wait times
- Single driver instance per request
- Proper cleanup
```

### 2. **Cache Results**
Consider adding Redis/in-memory cache:
```python
# Pseudocode
if problem_code in cache:
    return cache[problem_code]
else:
    result = fetch_editorial(problem_code)
    cache[problem_code] = result
    return result
```

### 3. **Rate Limiting**
Add to `main.py`:
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/generate/hints")
@limiter.limit("10/minute")  # Max 10 requests per minute
def generate_hints(...):
    ...
```

---

## 🐛 Troubleshooting

### Issue: "Selenium driver not found"
**Solution:**
```powershell
pip install webdriver-manager --upgrade
```
The driver auto-downloads on first run.

---

### Issue: "Cloudflare blocking requests"
**Solution:**
- Already implemented anti-detection measures
- If still blocked, try:
  - Increase `time.sleep()` values
  - Add more human-like behavior (scrolling, etc.)
  - Use residential proxies (advanced)

---

### Issue: "Editorial not found"
**Possible causes:**
1. Problem has no editorial yet
2. Editorial is in a format we don't detect
3. Editorial is in discuss forums (not on problem page)

**Debug:**
```python
# Test extraction directly
result = get_editorial(problem_url)
print(result)
```

---

### Issue: "AI API errors"
**Check:**
- `.env` file has correct API key
- API key has proper permissions
- Not hitting rate limits
- API service is operational

---

## 📝 Code Structure

```
codechef/
├── cc_editorial.py          # Core editorial extraction logic
│   ├── setup_selenium_driver()
│   ├── parse_problem_url()
│   ├── fetch_problem_page()
│   ├── extract_problem_metadata()
│   ├── extract_editorial_content()  # Multi-strategy
│   ├── clean_editorial_text()
│   └── get_editorial()             # Main entry point
│
├── main.py                   # FastAPI server
│   ├── POST /generate/hints
│   ├── GET /fetch/editorial
│   └── GET /metadata
│
├── requirements.txt          # Python dependencies
├── .env                      # API keys (gitignored)
└── README.md                # This file
```

---

## 🤝 Contributing

Improvements welcome! Areas to contribute:
- Better editorial detection strategies
- Support for more editorial formats
- Caching layer implementation
- Error handling improvements
- Additional endpoints (e.g., similar problems)

---

## 📜 License

This project is for educational purposes. Respect CodeChef's terms of service when using this scraper.

---

## 🔗 Related Projects

- **Codeforces Editorial Scraper**: `../codeforces/` (sibling project)
- Uses API + Selenium hybrid approach

---

## 💡 Future Enhancements

- [ ] Support for discuss forum editorials
- [ ] Multi-language editorial support
- [ ] Video tutorial extraction
- [ ] Solution code extraction and analysis
- [ ] Difficulty prediction based on editorial complexity
- [ ] Similar problems recommendation
- [ ] Editorial quality scoring

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your `.env` configuration
3. Test with known problems (e.g., FLOW001)
4. Check Selenium logs for detailed errors

---

**Built with ❤️ for competitive programmers**

*Remember: Use hints to learn, not to cheat! 🎯*
