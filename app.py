from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Load OpenAI API Key securely
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    """Handles AI-powered legal queries"""
    user_query = request.json.get("query")

    if not user_query:
        return jsonify({"answer": "❌ Please enter a valid question about cyber law."}), 400

    try:
        # OpenAI API Request
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in cyber law. Provide concise and accurate answers."},
                {"role": "user", "content": user_query}
            ]
        )

        ai_answer = response["choices"][0]["message"]["content"]

    except openai.error.OpenAIError as e:
        ai_answer = f"⚠ OpenAI Error: {str(e)}"
    except Exception as e:
        ai_answer = "⚠ Error retrieving response. Please try again later."

    return jsonify({"answer": ai_answer})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
