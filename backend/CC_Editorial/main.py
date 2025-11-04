from fastapi import FastAPI, Query
from cc_editorial import fetch_discuss_explanations
from hint_generator import generate_hints

app = FastAPI(
    title="CodeChef Discuss Scraper API",
    description="Fetches editorials and generates AI-based hints.",
    version="1.1.0"
)

@app.get("/")
def home():
    return {"message": "CodeChef Discuss Scraper + Gemini Hint Generator is running."}

@app.get("/cc_editorial")
def get_cc_editorial(problem_code: str, with_hints: bool = Query(False)):
    """
    Fetch CodeChef editorial or explanation posts for a given problem code.
    Example: /cc_editorial?problem_code=FLOW001&with_hints=true
    """
    data = fetch_discuss_explanations(problem_code)
    
    if with_hints and data.get("count", 0) > 0:
        # Take the first editorial text
        editorial_text = data["posts"][0]["text"]
        hints = generate_hints(editorial_text, problem_code)
        data["hints"] = hints

    return data
