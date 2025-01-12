from flask import Flask, request, jsonify, render_template
import os

# Initialize Flask app
app = Flask(__name__)

# Preloaded doctrinal responses
doctrines = {
    "salvation": "Salvation is by grace through faith alone in the shed blood of Jesus Christ, as taught in 1 Corinthians 15:1-4. 'Christ died for our sins according to the scriptures; and that he was buried, and that he rose again the third day according to the scriptures.' Ephesians 2:8-9 further clarifies that salvation is 'not of works, lest any man should boast.' Trusting in anything other than Christ’s finished work, such as works, sacraments, or repentance of sins, is a false gospel (Galatians 1:8-9).",
    "how does a person get saved": "To be saved, a person must trust in the shed blood of Jesus Christ, believing in His death for their sins, His burial, and His resurrection (1 Corinthians 15:1-4). Salvation is by grace through faith, not by works, baptism, or following the law (Ephesians 2:8-9).",
    "repentance": "'Repentance' in the Bible means a change of mind about unbelief, not turning from sin as a condition for salvation. Acts 20:21 teaches repentance toward God and faith in our Lord Jesus Christ."
}

@app.route("/")
def home():
    # Serve the frontend HTML file
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask_question():
    try:
        # Parse the incoming request
        data = request.json
        question = data.get("question", "").strip().lower()  # Normalize input
        print(f"Received question: {question}")

        # Check for a matching doctrinal response
        response = doctrines.get(question, "I'm sorry, I don't have an answer for that question.")
        return jsonify({"response": response})

    except Exception as e:
        # Handle errors gracefully
        print(f"Error occurred: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    # Start the app using a dynamic port for Render
    port = int(os.environ.get("PORT", 5001))  # Default to port 5001 for local testing
    app.run(host="0.0.0.0", port=port, debug=True)

