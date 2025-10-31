import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_hints(editorial_text: str, problem_code: str):
    """
    Generate 3 progressively detailed hints using Gemini.
    """
    prompt = f"""
You are an AI tutor helping a student solve CodeChef problem '{problem_code}'.
Based on the editorial below, generate three hints:

1️⃣ Hint 1: Give a subtle push — minimal guidance, no formulas.
2️⃣ Hint 2: Provide moderate conceptual insight without full solution.
3️⃣ Hint 3: Give the complete explanation or logic of the problem.

Editorial:
{editorial_text}
"""

    model = genai.GenerativeModel("gemini-2.5-flash")  # or gemini-1.5-pro
    response = model.generate_content(prompt)
    return response.text.strip()
