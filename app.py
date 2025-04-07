from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

# Use Render Secret
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["POST"])
def explain_code():
    data = request.get_json()
    code = data.get("code", "")
    language = data.get("language", "python")

    if not code.strip():
        return jsonify({"error": "No code provided"}), 400

    prompt = f"Explain the following {language} code in simple terms for a {data.get('expertise', 'beginner')} developer:\n\n{code}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                { "role": "system", "content": "You are an expert programming assistant." },
                { "role": "user", "content": prompt }
            ],
            max_tokens=1000,
            temperature=0.3
        )

        explanation = response['choices'][0]['message']['content']
        return jsonify({ "explanation": explanation })

    except Exception as e:
        return jsonify({ "error": str(e) }), 500

if __name__ == "__main__":
    app.run(debug=True)
