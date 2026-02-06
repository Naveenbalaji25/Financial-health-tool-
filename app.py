from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import openai

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Hello from Flask Backend!"

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    df = pd.read_csv(file)

    # Cast to Python int to avoid int64 serialization error
    revenue = int(df['Revenue'].sum())
    expenses = int(df['Expenses'].sum())
    profit = revenue - expenses
    score = int((profit / (revenue + 1)) * 100)

    return jsonify({
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit,
        "score": score
    })

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    score = data.get('score', 0)

    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = f"Financial health score is {score}. Give 3 suggestions."

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )

    return jsonify({"advice": response.choices[0].text.strip()})

if __name__ == "__main__":
    app.run(debug=True)