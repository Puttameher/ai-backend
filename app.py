from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

# Optional: Load from environment variable or directly paste your key
openai.api_key = os.getenv("OPENAI_API_KEY") or "your-openai-key"

app = Flask(__name__)
CORS(app)  # Allows frontend to access backend

@app.route("/api/explain", methods=["POST"])
def explain_code():
    data = request.get_json()
    code = data.get("code", "")
    language = data.get("language", "python")

    if not code:
        return jsonify({"error": "Code is required"}), 400

    prompt = f"Explain the following {language} code in simple terms:\n\n{code}"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are an expert coding tutor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=600
        )
        explanation = response.choices[0].message.content.strip()
        return jsonify({"explanation": explanation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/generate-quiz", methods=["POST"])
def generate_quiz():
    data = request.get_json()
    code = data.get("code", "")
    language = data.get("language", "python")

    prompt = f"""
    Generate 3 multiple choice questions with 4 options and answers to test understanding of this {language} code:
    {code}
    Format the output as JSON in this structure:
    [
      {{
        "question": "...",
        "options": ["A", "B", "C", "D"],
        "answer": "A"
      }},
      ...
    ]
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who creates quizzes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        quiz_json = response.choices[0].message.content.strip()
        return jsonify({"quiz": quiz_json})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "AI Coding Mentor Backend is Live!"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
