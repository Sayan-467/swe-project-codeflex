# main.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import cf_editorial as cfe

app = FastAPI(title="CF Editorial Fetcher")

# CORS for dev (change in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputURL(BaseModel):
    problem_url: str

@app.get("/fetch/editorial")
def fetch_editorial(problem_url: Optional[str] = Query(None)):
    """
    Example: /fetch/editorial?problem_url=https://codeforces.com/contest/1741/problem/B
    Returns JSON: problem metadata + list of tutorial links + editorial text (first found).
    """
    if not problem_url:
        return {"error": "Provide problem_url query parameter."}

    parsed = cfe.parse_problem_url(problem_url)
    if not parsed:
        return {"error": "Could not parse problem URL. Make sure it is a standard Codeforces problem link."}

    contest_id = parsed["contest_id"]
    index = parsed["index"]

    metadata = cfe.fetch_problem_metadata(contest_id, index)
    tutorial_links = cfe.find_tutorial_links_for_problem(contest_id, index)

    editorial_texts = []
    for link in tutorial_links:
        text = cfe.fetch_blog_text(link)
        editorial_texts.append({"url": link, "text": text})

    # If no tutorial links found, try searching for 'tutorial' in blog manually (not implemented: advanced)
    return {
        "problem_metadata": metadata,
        "tutorial_links": tutorial_links,
        "editorials": editorial_texts
    }

@app.get("/debug/page")
def debug_page(url: Optional[str] = Query(None)):
    """
    Debug endpoint to see what's on a page.
    """
    if not url:
        return {"error": "Provide url query parameter."}
    
    import requests
    from bs4 import BeautifulSoup
    
    try:
        r = requests.get(url, headers=cfe.HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Find all links
        links = []
        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True)
            href = a["href"]
            if text or "/blog/entry/" in href or "tutorial" in href.lower():
                links.append({"text": text, "href": href})
        
        return {
            "status_code": r.status_code,
            "url": url,
            "links_found": len(links),
            "interesting_links": links[:50]  # First 50 links
        }
    except Exception as e:
        return {"error": str(e)}

# simple health
@app.get("/")
def root():
    return {"ok": True}
