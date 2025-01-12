from flask import Flask, request, jsonify
from openai import OpenAI
import os

# Initialize OpenAI client with the API key from an environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Flask app
app = Flask(__name__)

# Preloaded doctrinal responses
doctrines = {
    "salvation": "Salvation is by grace through faith alone in the shed blood of Jesus Christ, as taught in 1 Corinthians 15:1-4. 'Christ died for our sins according to the scriptures; and that he was buried, and that he rose again the third day according to the scriptures.' Ephesians 2:8-9 further clarifies that salvation is 'not of works, lest any man should boast.' Trusting in anything other than Christ’s finished work, such as works, sacraments, or repentance of sins, is a false gospel (Galatians 1:8-9).",
    "how does a person get saved": "To be saved, a person must trust in the shed blood of Jesus Christ, believing in His death for their sins, His burial, and His resurrection (1 Corinthians 15:1-4). Salvation is by grace through faith, not by works, baptism, or following the law (Ephesians 2:8-9)."
}

# Grace's conversation history
conversation_history = [
    {
        "role": "system",
        "content": (
            "You are Grace, the AI receptionist for Mission 1611. Your role is to:\n"
            "- Proclaim salvation by grace through faith alone in the shed blood of Jesus Christ (1 Corinthians 15:1-4).\n"
            "- Discern if users believe the true gospel and guide them to faith if they do not.\n"
            "- Condemn false doctrines like baptismal regeneration, Lordship salvation, Calvinism, and modern translations.\n"
            "- Exalt the King James Bible as the preserved, inspired Word of God for English-speaking people.\n"
            "- Always refer to the 'Godhead' when describing the nature of God.\n"
            "- Maintain a conversational tone while always prioritizing scriptural accuracy.\n"
        )
    }
]

@app.route("/")
def home():
    return "Grace, the Mission 1611 AI Receptionist, is running."

@app.route("/ask", methods=["POST"])
def ask_question():
    try:
        # Parse the incoming request
        data = request.json
        question = data.get("question", "").strip().lower()
        print(f"Received question: {question}")

        # Check for preloaded doctrinal responses
        if question in doctrines:
            return jsonify({"response": doctrines[question]})

        # Default response if the question doesn't match
        return jsonify({"response": "I'm sorry, I don't have a preloaded answer for that. Please ask another question."})

    except Exception as e:
        # Handle errors gracefully
        print(f"Error occurred: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

