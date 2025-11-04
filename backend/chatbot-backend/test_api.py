import google.generativeai as genai

API_KEY = "AIzaSyAK0IOGO-DPoxlY3okjiaW47oAZUMTrqjA"

genai.configure(api_key=API_KEY)

# Check available models
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)

# Try generating content
model = genai.GenerativeModel("gemini-1.5-flash-latest")
response = model.generate_content("Say Hello from Gemini!")
print("\nResponse:", response.text)
