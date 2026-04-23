from flask import Flask, render_template, request
import json

app = Flask(__name__)

with open("intents.json", encoding="utf-8") as file:
    data = json.load(file)

# Detect language
def detect_language(text):
    for ch in text:
        if 'ಕ' <= ch <= 'ಹ':
            return "kn"
        elif 'अ' <= ch <= 'ह':
            return "hi"
        elif 'అ' <= ch <= 'హ':
            return "te"
    return "en"

# Get response
def get_response(user_input):
    lang = detect_language(user_input)
    user_input = user_input.lower()

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_input:
                return intent["responses"].get(lang, intent["responses"]["en"])

    return {
        "en": "Please ask about courses, placements, fees or admission.",
        "kn": "ದಯವಿಟ್ಟು ಕೋರ್ಸ್ ಅಥವಾ ಪ್ಲೇಸ್ಮೆಂಟ್ ಬಗ್ಗೆ ಕೇಳಿ.",
        "hi": "कृपया कोर्स या प्लेसमेंट के बारे में पूछें।",
        "te": "దయచేసి కోర్సులు లేదా ప్లేస్‌మెంట్ గురించి అడగండి."
    }.get(lang)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot():
    userText = request.form["msg"]
    return get_response(userText)

if __name__ == "__main__":
    app.run(debug=True)