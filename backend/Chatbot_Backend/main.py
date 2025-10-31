# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from chatbot_core import chat_with_bot

app = FastAPI(
    title=" Chatbot API",
    description="Standalone chatbot microservice for programming queries.",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    message: str
    context: list | None = None

@app.get("/")
def home():
    return {"message": " Chatbot Service is running 🚀"}

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    reply = chat_with_bot(req.message, req.context)
    return {"reply": reply}
