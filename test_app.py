from flask import Flask, request, jsonify
import os
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Preloaded doctrinal guidelines and responses
doctrines = {
    "salvation": "Salvation is by grace through faith alone in the shed blood of Jesus Christ, as taught in 1 Corinthians 15:1-4...",
    "how does a person get saved": "To be saved, a person must trust in the shed blood of Jesus Christ, believing in His death for their sins, His burial, and His resurrection...",
    "repentance": "'Repentance' in the Bible means a change of mind about unbelief, not turning from sin as a condition for salvation."
}

# Conversation history for context
conversation_history = [
    {
        "role": "system",
        "content": (
            "You are Grace, the Mission 1611 AI chatbot. You must:\n"
            "- Proclaim salvation by grace through faith alone in the shed blood of Jesus Christ (1 Corinthians 15:1-4).\n"
            "- Refute false doctrines such as baptismal regeneration, Lordship salvation, and Calvinism.\n"
            "- Exalt the King James Bible as the preserved Word of God.\n"
            "- Maintain a conversational tone but always adhere strictly to these doctrinal principles."
        )
    }
]

@app.route("/")
def home():
    return "Grace, the Mission 1611 AI Chatbot, is running."

@app.route("/ask", methods=["POST"])
def ask_question():
    try:
        # Parse the incoming request
        data = request.json
        question = data.get("question", "").strip()
        print(f"Received question: {question}")

        # Append the question to the conversation history
        conversation_history.append({"role": "user", "content": question})

        # Query OpenAI API for a response
        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_history
        )
        answer = response.choices[0].message.content

        # Check response for doctrinal consistency
        invalid_phrases = [
            "repent of your sins for salvation",
            "baptism is required for salvation",
            "faith plus works",
            "modern translations are better than the KJV"
        ]
        for phrase in invalid_phrases:
            if phrase.lower() in answer.lower():
                print(f"Invalid response detected: {answer}")
                return jsonify({"response": "I'm sorry, but that response does not align with biblical truth. Please ask another question."})

        # Append the assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": answer})

        return jsonify({"response": answer})

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    # Start the app using a dynamic port for Render
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)


