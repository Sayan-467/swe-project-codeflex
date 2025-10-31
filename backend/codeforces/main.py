from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os
import cf_editorial as cfe

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
app = FastAPI(title="Codeforces AI Hint Generator")

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
    return {"ok": True, "message": "CF AI Hint Generator is running 🚀"}


@app.post("/generate/hints")
def generate_hints(input_data: InputURL):
    """
    Fetches Codeforces editorial, then uses Gemini or OpenAI to generate step-by-step hints.
    """
    problem_url = input_data.problem_url
    parsed = cfe.parse_problem_url(problem_url)

    if not parsed:
        return {"error": "Invalid Codeforces problem URL format."}

    contest_id = parsed["contest_id"]
    index = parsed["index"]

    # Step 1: Fetch metadata
    metadata = cfe.fetch_problem_metadata(contest_id, index)

    # Step 2: Find editorial links
    tutorial_links = cfe.find_tutorial_links_for_problem(contest_id, index)
    if not tutorial_links:
        return {"error": "No editorial or tutorial links found for this problem."}

    editorial_url = tutorial_links[0]
    editorial_text = cfe.fetch_blog_text(editorial_url)
    if "Error fetching" in editorial_text:
        return {"error": "Could not fetch editorial content. Please try again."}

    # Step 3: Prepare the AI prompt
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

    # Step 4: Generate hints
    try:
        if USE_GEMINI:
            # --- Gemini Path ---
            model = genai.GenerativeModel("gemini-2.5-flash")
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
            "editorial_url": editorial_url,
            "generated_hints": hints
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

    parsed = cfe.parse_problem_url(problem_url)
    if not parsed:
        return {"error": "Invalid problem URL format."}

    contest_id = parsed["contest_id"]
    index = parsed["index"]

    tutorial_links = cfe.find_tutorial_links_for_problem(contest_id, index)
    editorials = []
    for link in tutorial_links:
        text = cfe.fetch_blog_text(link)
        editorials.append({"url": link, "text": text[:1000]})  # limit text preview

    return {"tutorial_links": tutorial_links, "editorials": editorials}

