from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os
import cc_editorial as cce

# Load environment variables from .env
load_dotenv()

# --- Detect provider ---
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
app = FastAPI(title="CodeChef AI Hint Generator")

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
    return {"ok": True, "message": "CodeChef AI Hint Generator is running 🚀"}


@app.post("/generate/hints")
def generate_hints(input_data: InputURL):
    """
    Fetches CodeChef editorial, then uses Gemini or OpenAI to generate step-by-step hints.
    """
    problem_url = input_data.problem_url
    
    # Fetch editorial using our custom scraper
    result = cce.get_editorial(problem_url)
    
    if "error" in result:
        return {"error": result["error"]}
    
    if not result.get("editorial_available") or not result.get("editorial_text"):
        return {
            "error": "Editorial not available for this problem",
            "message": "This problem may not have an editorial yet, or it's in a format we can't extract.",
            "problem": result.get("problem", {})
        }
    
    metadata = result["problem"]
    editorial_text = result["editorial_text"]
    
    # Prepare the AI prompt
    prompt = f"""
You are an AI assistant that helps competitive programmers learn without revealing full solutions.
Given the following CodeChef editorial, generate 3–5 concise, progressively detailed hints that guide a student toward solving the problem logically.

Problem: {metadata.get('name', 'Unknown')}
Difficulty: {metadata.get('difficulty', 'Unknown')}

Each hint should:
1. Be short and specific.
2. Avoid giving away the full solution.
3. Reveal just enough insight to push the user forward.

Editorial:
{editorial_text}

Now generate clear, structured hints:
"""

    # Generate hints using AI
    try:
        if USE_GEMINI:
            # --- Gemini Path ---
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            response = model.generate_content(prompt)
            hints = response.text.strip()

        else:
            # --- OpenAI Path ---
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
            "note": "Hints generated from scraped CodeChef editorial"
        }

    except Exception as e:
        return {"error": f"AI API error: {str(e)}"}


@app.get("/fetch/editorial")
def fetch_editorial(problem_url: Optional[str] = Query(None)):
    """
    Debug endpoint to fetch and view editorial text directly.
    """
    if not problem_url:
        return {"error": "Provide problem_url query parameter."}

    result = cce.get_editorial(problem_url)
    
    if "error" in result:
        return result
    
    # Limit preview for API response
    if result.get("editorial_text"):
        preview_length = 2000
        result["editorial_preview"] = result["editorial_text"][:preview_length]
        result["editorial_length"] = len(result["editorial_text"])
        if len(result["editorial_text"]) > preview_length:
            result["editorial_preview"] += "\n\n[... truncated for preview ...]"
        del result["editorial_text"]  # Remove full text from response
    
    return result


@app.get("/metadata")
def get_metadata(problem_url: Optional[str] = Query(None)):
    """
    Get problem metadata without fetching editorial.
    Faster endpoint for just getting problem info.
    """
    if not problem_url:
        return {"error": "Provide problem_url query parameter."}
    
    parsed = cce.parse_problem_url(problem_url)
    if not parsed:
        return {"error": "Invalid CodeChef problem URL format"}
    
    try:
        problem_code = parsed["problem_code"]
        contest_code = parsed.get("contest_code")
        
        # Fetch page
        html = cce.fetch_problem_page(problem_code, contest_code)
        
        # Extract only metadata
        metadata = cce.extract_problem_metadata(html, problem_code)
        
        return {
            "problem": metadata,
            "parsed_url": parsed
        }
    except Exception as e:
        return {"error": f"Error fetching metadata: {str(e)}"}
