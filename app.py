import os
from flask import Flask, render_template, request, jsonify
import random
import difflib

app = Flask(__name__)

# Predefined responses (same as before, trimmed for brevity)
RESPONSES = {
    "joy": [
        "I love hearing that! 🌸 Happiness looks good on you.",
        "That’s wonderful 💫. Hold onto this moment and let it fuel you forward.",
        "Your joy is contagious ✨—thank you for sharing it!"
    ],
    "sadness": [
        "I’m sorry you feel this way 💙. Even in dark clouds, there’s light waiting to shine on you.",
        "You matter more than you know. Your feelings are valid, and you’re not alone. 🌼",
        "Sadness comes and goes like waves. You are the ocean—bigger than the waves 🌊."
    ],
    # Add more categories as needed...
}

def detect_emotion(user_message: str) -> str:
    """
    A heuristic to choose an emotion. We do *not* import heavy libs at top.
    """
    # Lazy import here, only if needed
    from textblob import TextBlob

    blob = TextBlob(user_message)
    polarity = blob.sentiment.polarity  # -1 to +1

    if polarity > 0.5:
        possible = ["joy"]
    elif polarity < -0.5:
        possible = ["sadness"]
    else:
        possible = ["joy", "sadness"]

    # Try to match a keyword exactly
    for w in user_message.lower().split():
        if w in RESPONSES:
            return w

    # Fallback: return first of possible
    return possible[0]

def best_match(user_message: str) -> str:
    category = detect_emotion(user_message)
    responses = RESPONSES.get(category)
    if responses:
        return random.choice(responses)
    else:
        return "I'm here to listen. 💙"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.get_json(force=True)
    msg = data.get("message", "")
    try:
        reply = best_match(msg)
    except Exception as e:
        # Log the error
        print("Error in get_response:", e)
        reply = "Oops, something went wrong 😕"
    return jsonify({"reply": reply})

# Other routes for exercises / games
@app.route("/exercises")
def exercises():
    return render_template("exercises.html")

@app.route("/exercise/breathing")
def exercise_breathing():
    return render_template("exercise_breathing.html")

@app.route("/exercise/body_scan")
def exercise_body_scan():
    return render_template("exercise_body_scan.html")

@app.route("/exercise/visualization")
def exercise_visualization():
    return render_template("exercise_visualization.html")

@app.route("/relaxing_games")
def relaxing_games():
    return render_template("relaxing_games.html")

@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/game/bubble")
def bubble_game():
    return render_template("games/bubble.html")

@app.route("/game/mandala")
def mandala_game():
    return render_template("games/mandala.html")

@app.route("/game/zen")
def zen_game():
    return render_template("games/zen.html")

@app.route("/game/lanterns")
def lanterns_game():
    return render_template("games/lanterns.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting app on 0.0.0.0:{port}")
    app.run(debug=True, host="0.0.0.0", port=port)
