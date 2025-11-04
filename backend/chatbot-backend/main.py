# import google.generativeai as genai

# # === DIRECTLY USE YOUR API KEY HERE ===
# API_KEY = "AIzaSyAK0IOGO-DPoxlY3okjiaW47oAZUMTrqjA"
# genai.configure(api_key=API_KEY)

# def get_topic_summary(topic):
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     response = model.generate_content(f"Explain '{topic}' in 4-5 lines for beginners.")
#     return response.text.strip()

# def get_learning_resources(topic):
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     response = model.generate_content(f"Give 3 useful online resources (YouTube or articles) to learn '{topic}'.")
#     return response.text.strip()

# if __name__ == "__main__":
#     print("🤖 Welcome to the Coding Topic Chatbot!")
#     topic = input("Enter a topic (e.g., Binary Search, Graphs, DP): ")

#     try:
#         print("\n📘 Short Note:")
#         print(get_topic_summary(topic))

#         print("\n🔗 Online Resources:")
#         print(get_learning_resources(topic))
#     except Exception as e:
#         print("\n❌ Error communicating with Gemini API:")
#         print(e)


from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# -------------------- CONFIG --------------------
API_KEY = "AIzaSyAK0IOGO-DPoxlY3okjiaW47oAZUMTrqjA"
genai.configure(api_key=API_KEY)

app = Flask(__name__)
CORS(app)

# -------------------- CHATBOT ROUTE --------------------
@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    topic = data.get("topic")

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    # Prompt to generate short note
    note_prompt = f"Give a 4-5 line short note explaining the concept of {topic} in simple terms for a beginner."
    # Prompt to generate online learning resources
    resource_prompt = f"Provide 3-4 useful online resources (YouTube links or articles) to learn {topic}."

    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro")

        note_response = model.generate_content(note_prompt)
        resource_response = model.generate_content(resource_prompt)

        return jsonify({
            "topic": topic,
            "short_note": note_response.text,
            "resources": resource_response.text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------- MAIN ENTRY --------------------
if __name__ == "__main__":
    print("🤖 Chatbot Backend Running on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
