from flask import Flask, request, jsonify
import google.generativeai as genai
from datasets import load_dataset
from config import GEMINI_API_KEY

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Load dataset
science_dataset = load_dataset("KadamParth/NCERT_Science_10th")["train"]
social_dataset= load_dataset("KadamParth/NCERT_Social_Studies_10th")["train"]


# Convert dataset into a dictionary for fast lookup
qa_dict = {entry["Question"].strip().lower(): entry["Answer"] for entry in science_dataset}
qa_dict.update({entry["Question"].strip().lower(): entry["Answer"] for entry in social_dataset})

# Initialize Flask app
app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").strip().lower()  # Normalize input
    
    # Check if an exact question exists in the dataset
    if user_input in qa_dict:
        return jsonify({"response": qa_dict[user_input]})

    # If no exact match, try using Gemini API
    response = model.generate_content(user_input)
    return jsonify({"response": response.text})

if __name__ == "__main__":
    app.run(debug=True)


