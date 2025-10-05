from flask import Flask, request, jsonify
from transformers import pipeline
import random

app = Flask(__name__)

# Load emotion classifier
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

# Generate friendly responses
def generate_response(user_message, emotion):
    responses = {
        "joy": ["😄 That's awesome! Tell me more!", "Yay! I love hearing that 😃", "So happy for you! Keep it going!"],
        "sadness": ["💙 I'm here for you. Want to talk about it?", "I'm sorry you're feeling down 😔. I'm listening.", "It's okay to feel sad sometimes. Share more if you want."],
        "anger": ["😤 I get why that would make you upset. Venting can help.", "Take a deep breath 😌. Do you want to explain what happened?", "Anger is normal. I'm here if you want to talk."],
        "fear": ["😟 It's okay to feel nervous. What's worrying you?", "Take your time, I'm listening and won't judge.", "I understand. Facing fear is tough, but you’re not alone."],
        "love": ["💖 That's heartwarming! Tell me more!", "Aw, that's sweet 😍", "Love is beautiful! What happened?"],
        "surprise": ["😲 Wow! That sounds surprising! What happened next?", "Oh really? That’s unexpected!", "I didn’t see that coming! Tell me more!"],
        "trust": ["👍 Sounds trustworthy! Can you explain more?", "I see! You seem confident about it.", "Good to know! What else happened?"],
        "anticipation": ["😃 Excited? Tell me more!", "Looking forward to it? That's awesome!", "I can feel your excitement! What’s next?"],
        "neutral": ["Interesting! 😃 Can you tell me more?", "Hmm, tell me more about that!", "Oh, I see! Go on…"]
    }
    return random.choice(responses.get(emotion, responses["neutral"]))

# Detect emotion
def detect_emotion(message):
    result = emotion_classifier(message)
    return result[0]['label'].lower()

# POST endpoint for frontend
@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"reply": "Please say something!"})
    
    emotion = detect_emotion(user_message)
    reply = generate_response(user_message, emotion)
    return jsonify({"reply": reply, "emotion": emotion})

if __name__ == "__main__":
    app.run(debug=True)
