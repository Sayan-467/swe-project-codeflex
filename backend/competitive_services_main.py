"""
Combined FastAPI server for CodeChef and Codeforces editorial/hint generation services
Deployed on Render - Port 8001
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os
import sys

# Add paths to import from subdirectories
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'codechef'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'codeforces'))

import cc_editorial as cce
import cf_editorial as cfe

# Load environment variables
load_dotenv()

# --- Detect AI provider ---
USE_GEMINI = bool(os.getenv("GEMINI_API_KEY"))
USE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))

if not USE_GEMINI and not USE_OPENAI:
    raise Exception("No API key found. Please set GEMINI_API_KEY or OPENAI_API_KEY in your .env file.")

# --- Import respective SDKs ---
if USE_GEMINI:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
else:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- FastAPI setup ---
app = FastAPI(
    title="Competitive Programming Services API",
    description="Combined CodeChef and Codeforces editorial scraping and AI hint generation",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InputURL(BaseModel):
    problem_url: str


@app.get("/")
def root():
    return {
        "ok": True,
        "message": "Competitive Programming Services API is running 🚀",
        "services": ["CodeChef", "Codeforces"],
        "endpoints": {
            "codechef": ["/codechef/generate/hints", "/codechef/fetch/editorial", "/codechef/metadata"],
            "codeforces": ["/codeforces/generate/hints", "/codeforces/fetch/editorial"]
        }
    }


# ==================== CODECHEF ENDPOINTS ====================

@app.post("/codechef/generate/hints")
def codechef_generate_hints(input_data: InputURL):
    """
    Fetches CodeChef editorial from Discuss forum, then generates AI hints.
    """
    problem_url = input_data.problem_url
    
    parsed = cce.parse_problem_url(problem_url)
    if not parsed:
        return {"error": "Invalid CodeChef problem URL format"}
    
    problem_code = parsed["problem_code"]
    result = cce.fetch_discuss_explanations(problem_code)
    
    if "error" in result:
        return {"error": result["error"]}
    
    if result.get("count", 0) == 0:
        return {
            "error": "Editorial not available for this problem",
            "message": "No editorial found in CodeChef Discuss forum for this problem.",
            "problem_code": problem_code
        }
    
    first_post = result["posts"][0]
    editorial_text = first_post["text"]
    metadata = {
        "problem_code": problem_code,
        "name": first_post["title"],
        "editorial_url": first_post["url"]
    }
    
    prompt = f"""
You are an AI assistant that helps competitive programmers learn without revealing full solutions.
Given the following CodeChef editorial, generate 3–5 concise, progressively detailed hints that guide a student toward solving the problem logically.

Problem: {metadata.get('name', 'Unknown')}

Each hint should:
1. Be short and specific.
2. Avoid giving away the full solution.
3. Reveal just enough insight to push the user forward.

Editorial:
{editorial_text}

Now generate clear, structured hints:
"""

    try:
        if USE_GEMINI:
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            response = model.generate_content(prompt)
            hints = response.text.strip()
        else:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful AI tutor for competitive programming."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=700,
                temperature=0.7
            )
            hints = completion.choices[0].message.content.strip()

        return {
            "problem": metadata,
            "editorial_available": True,
            "generated_hints": hints,
            "platform": "CodeChef"
        }

    except Exception as e:
        return {"error": f"AI API error: {str(e)}"}


@app.get("/codechef/fetch/editorial")
def codechef_fetch_editorial(problem_url: Optional[str] = Query(None)):
    """Fetch editorial from CodeChef Discuss forum."""
    if not problem_url:
        return {"error": "Provide problem_url query parameter."}

    parsed = cce.parse_problem_url(problem_url)
    if not parsed:
        return {"error": "Invalid CodeChef problem URL format"}
    
    problem_code = parsed["problem_code"]
    result = cce.fetch_discuss_explanations(problem_code)
    
    return result


@app.get("/codechef/metadata")
def codechef_metadata(problem_url: Optional[str] = Query(None)):
    """Get CodeChef problem metadata without fetching editorial."""
    if not problem_url:
        return {"error": "Provide problem_url query parameter."}
    
    parsed = cce.parse_problem_url(problem_url)
    if not parsed:
        return {"error": "Invalid CodeChef problem URL format"}
    
    try:
        problem_code = parsed["problem_code"]
        contest_code = parsed.get("contest_code")
        html = cce.fetch_problem_page(problem_code, contest_code)
        metadata = cce.extract_problem_metadata(html, problem_code)
        
        return {
            "problem": metadata,
            "parsed_url": parsed,
            "platform": "CodeChef"
        }
    except Exception as e:
        return {"error": f"Error fetching metadata: {str(e)}"}


# ==================== CODEFORCES ENDPOINTS ====================

@app.post("/codeforces/generate/hints")
def codeforces_generate_hints(input_data: InputURL):
    """
    Fetches Codeforces editorial, then generates AI hints.
    """
    problem_url = input_data.problem_url
    parsed = cfe.parse_problem_url(problem_url)

    if not parsed:
        return {"error": "Invalid Codeforces problem URL format."}

    contest_id = parsed["contest_id"]
    index = parsed["index"]

    metadata = cfe.fetch_problem_metadata(contest_id, index)
    tutorial_links = cfe.find_tutorial_links_for_problem(contest_id, index)
    
    if not tutorial_links:
        return {"error": "No editorial or tutorial links found for this problem."}

    editorial_url = tutorial_links[0]
    editorial_text = cfe.fetch_blog_text(editorial_url)
    
    if "Error fetching" in editorial_text:
        return {"error": "Could not fetch editorial content. Please try again."}

    prompt = f"""
You are an AI assistant that helps competitive programmers learn without revealing full solutions.
Given the following Codeforces editorial, generate 3–5 concise, progressively detailed hints that guide a student toward solving the problem logically.

Each hint should:
1. Be short and specific.
2. Avoid giving away the full solution.
3. Reveal just enough insight to push the user forward.

Editorial:
{editorial_text}

Now generate clear, structured hints:
"""

    try:
        if USE_GEMINI:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            hints = response.text.strip()
        else:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful AI tutor for competitive programming."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=700,
                temperature=0.7
            )
            hints = completion.choices[0].message.content.strip()

        return {
            "problem": metadata,
            "editorial_url": editorial_url,
            "generated_hints": hints,
            "platform": "Codeforces"
        }

    except Exception as e:
        return {"error": f"AI API error: {str(e)}"}


@app.get("/codeforces/fetch/editorial")
def codeforces_fetch_editorial(problem_url: Optional[str] = Query(None)):
    """Fetch Codeforces editorial."""
    if not problem_url:
        return {"error": "Provide problem_url query parameter."}

    parsed = cfe.parse_problem_url(problem_url)
    if not parsed:
        return {"error": "Invalid problem URL format."}

    contest_id = parsed["contest_id"]

    
    index = parsed["index"]

    tutorial_links = cfe.find_tutorial_links_for_problem(contest_id, index)
    editorials = []
    for link in tutorial_links:
        text = cfe.fetch_blog_text(link)
        editorials.append({"url": link, "text": text[:1000]})

    return {"tutorial_links": tutorial_links, "editorials": editorials, "platform": "Codeforces"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
