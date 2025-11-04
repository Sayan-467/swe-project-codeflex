"""
Combined FastAPI server for Chatbot and CC_Editorial services
Deployed on Render - Port 8002
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
import os
import sys

# Get a life bitches
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Chatbot_Backend'))
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'CC_Editorial'))

from Chatbot_Backend.chatbot_core import chat_with_bot
from codechef.cc_editorial import fetch_discuss_explanations
from CC_Editorial.hint_generator import generate_hints

# Load environment variables
load_dotenv()

# --- FastAPI setup ---
app = FastAPI(
    title="Chatbot & CC Editorial Services API",
    description="Combined Chatbot and CodeChef Editorial/Hint generation services",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    context: list | None = None


@app.get("/")
def home():
    return {
        "ok": True,
        "message": "Chatbot & CC Editorial Services API is running 🚀",
        "services": ["Chatbot", "CC_Editorial"],
        "endpoints": {
            "chatbot": ["/chat"],
            "cc_editorial": ["/cc_editorial"]
        }
    }


# ==================== CHATBOT ENDPOINTS ====================
@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    """AI-powered chatbot for programming queries."""
    reply = chat_with_bot(req.message, req.context)
    return JSONResponse(
        status_code=200,
        content={"reply": reply, "service": "chatbot"})


# ==================== CC EDITORIAL ENDPOINTS ====================

@app.get("/cc_editorial")
def get_cc_editorial(problem_code: str, with_hints: bool = Query(False)):
    """
    Fetch CodeChef editorial or explanation posts for a given problem code.
    Example: /cc_editorial?problem_code=FLOW001&with_hints=true
    """
    data = fetch_discuss_explanations(problem_code)
    
    if with_hints and data.get("count", 0) > 0:
        editorial_text = data["posts"][0]["text"]
        hints = generate_hints(editorial_text, problem_code)
        data["hints"] = hints

    return data


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8002))
    uvicorn.run(app, host="0.0.0.0", port=port)
