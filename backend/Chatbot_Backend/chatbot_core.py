# chatbot_core.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use Gemini model (you can switch to gemini-1.5-pro if supported)
model = genai.GenerativeModel("gemini-2.5-flash")

def chat_with_bot(user_message: str, context: list = None):
    """
    Handles chatbot conversation and returns a response.
    """
    if context is None:
        context = []

    conversation = "\n".join([f"User: {msg['user']}\nBot: {msg['assistant']}" for msg in context])

    prompt = f"""
    You are Codemitra — a friendly AI coding tutor that helps students 
    understand programming concepts, debugging issues, and algorithmic logic.
    Conversation so far:
    {conversation}

    User: {user_message}
    Bot:
    
    Only provide plain text without markdown notations"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Sorry, I encountered an error: {str(e)}"
