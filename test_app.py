from flask import Flask, request, jsonify
from openai import OpenAI
import os

# Initialize OpenAI client with the API key from an environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return "Grace, the Mission 1611 AI Receptionist, is running."

@app.route("/ask", methods=["POST"])
def ask_question():
    try:
        data = request.json
        question = data.get("question", "No question provided.")
        return jsonify({"response": f"Received question: {question}"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


