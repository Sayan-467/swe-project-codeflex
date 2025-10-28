# Codeforces Editorial Fetcher

A FastAPI-based service that fetches Codeforces problem editorials using Selenium web scraping (to bypass 403 blocks) and the Codeforces API.

## 📁 Project Structure

```
codeforces/
├── .env                    # Environment variables (API credentials)
├── .venv/                  # Virtual environment
├── main.py                 # FastAPI server with endpoints
├── cf_editorial.py         # Core scraping and editorial fetching logic
├── requirements.txt        # Python dependencies
├── test_preview.py         # Test script to preview editorials
└── README.md              # This file
```

## 🚀 Setup (First Time Only)

### 1. Install Dependencies

```powershell
# Make sure you're in the project directory
cd "C:\Users\syeds\Desktop\Code Empire\Placement Material\Projects\swe-project\codeforces"

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt
```

### 2. Configure API Credentials

Your `.env` file should contain:
```
CODEFORCES_API_KEY=your_api_key_here
CODEFORCES_API_SECRET=your_api_secret_here
```

## 🏃 How to Run (Every Time)

### Step 1: Start the Server

```powershell
# Open a PowerShell terminal in the project folder
cd "C:\Users\syeds\Desktop\Code Empire\Placement Material\Projects\swe-project\codeforces"

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Start the FastAPI server
uvicorn main:app --reload
```

The server will start at: `http://127.0.0.1:8000`

### Step 2: Use the API

#### Option A: Test with the Preview Script

Open a **new terminal** (keep the server running in the first one):

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run the test
python test_preview.py
```

#### Option B: Make API Requests

**Endpoint:** `GET /fetch/editorial`

**Query Parameter:** `problem_url` (the Codeforces problem URL)

**Example using browser:**
```
http://127.0.0.1:8000/fetch/editorial?problem_url=https://codeforces.com/contest/1741/problem/B
```

**Example using Python:**
```python
import requests

url = "http://127.0.0.1:8000/fetch/editorial"
params = {
    "problem_url": "https://codeforces.com/contest/1741/problem/B"
}

response = requests.get(url, params=params)
data = response.json()

print("Problem:", data["problem_metadata"]["name"])
print("Tutorial Links:", data["tutorial_links"])
print("Editorial:", data["editorials"][0]["text"])
```

**Example using curl:**
```powershell
curl "http://127.0.0.1:8000/fetch/editorial?problem_url=https://codeforces.com/contest/1741/problem/B"
```

## 📊 API Response Format

```json
{
  "problem_metadata": {
    "contestId": "1741",
    "index": "B",
    "name": "Funny Permutation",
    "tags": ["constructive algorithms", "math"],
    "problem_api_object": { ... }
  },
  "tutorial_links": [
    "https://codeforces.com/blog/entry/107908"
  ],
  "editorials": [
    {
      "url": "https://codeforces.com/blog/entry/107908",
      "text": "Full editorial content here..."
    }
  ]
}
```

## 🔧 How It Works

1. **Parse Problem URL** - Extracts contest ID and problem index
2. **Fetch Metadata** - Gets problem details from Codeforces API
3. **Find Tutorial Link** - Uses Selenium to scrape the problem page and find the "Tutorial" link
4. **Fetch Editorial** - Uses Selenium to fetch the blog content (bypasses 403 blocks)
5. **Clean Text** - Removes LaTeX artifacts and excessive newlines
6. **Return JSON** - Provides structured data with metadata, links, and editorial text

## 🛠️ Technologies Used

- **FastAPI** - Web framework for the API
- **Selenium** - Browser automation to bypass HTTP 403 blocks
- **BeautifulSoup4** - HTML parsing
- **ChromeDriver** - Automated Chrome browser (managed by webdriver-manager)
- **Codeforces API** - For problem metadata

## 📝 Notes

- The server uses Selenium in headless mode (no visible browser window)
- ChromeDriver is automatically downloaded and managed
- Editorial text is cleaned to remove LaTeX artifacts and formatting issues
- The API uses authenticated Codeforces API calls with SHA-512 signatures
- Tutorial links are found directly from problem pages (bottom right "Tutorial" button)

## 🐛 Troubleshooting

**Server won't start:**
- Make sure virtual environment is activated
- Check if port 8000 is already in use
- Run `pip install -r requirements.txt` again

**No editorial found:**
- Check if the problem actually has a tutorial link
- Verify the problem URL format is correct
- Some older problems might not have editorials

**ChromeDriver errors:**
- The driver is auto-managed, but ensure Chrome browser is installed
- Check your internet connection (downloads driver on first run)

## 📄 License

This project is for educational purposes.
