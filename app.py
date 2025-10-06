@@ -1,447 +1,453 @@
import os
from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify
from textblob import TextBlob
import random
import difflib

app = Flask(__name__)

# Response database
RESPONSES = {
    # --- JOY CLUSTER ---
    "joy": [
        "I love hearing that! 🌸 Happiness looks good on you.",
        "That’s wonderful 💫. Hold onto this moment and let it fuel you forward.",
        "Your joy is contagious ✨—thank you for sharing it!"
    ],
    "happy": [
        "I love hearing that! 🌸 Happiness looks good on you.",
        "That’s wonderful 💫. Hold onto this moment and let it fuel you forward.",
        "Your joy is contagious ✨—thank you for sharing it!"
    ],
    "cheerfulness": [
        "Your lightheartedness brightens the day 🌞.",
        "It feels good to be playful and free 🌸.",
        "Moments of cheer are worth savoring ✨."
    ],
    "amused": [
        "Laughter really is the best medicine 😂.",
        "Your sense of humor shines 🌟.",
        "That giggle says it all 💕."
    ],
    "excited": [
        "Your excitement is contagious 🎉.",
        "Hold onto that spark—it fuels great things 🔥.",
        "Something amazing must be on the horizon 🌈."
    ],
    "delighted": [
        "Delight makes the heart feel lighter 🌸.",
        "So glad you’re enjoying this moment ✨.",
        "Little joys often bring the biggest smiles 💫."
    ],
    "optimism": [
        "Looking forward with hope is powerful 🌟.",
        "Your positive outlook inspires others 🌸.",
        "The future feels brighter when you believe 🌞."
    ],
    "hope": [
        "Hope lights the path ahead 💫.",
        "Even a little hope can move mountains 🌄.",
        "Keep that spark alive—it guides you forward 🌟."
    ],
    "pride": [
        "You’ve worked hard—be proud 🌿.",
        "Your achievements matter 💫.",
        "Pride in yourself fuels confidence ✨."
    ],
    "calm": [
    "Calmness brings clarity and peace 🌿.",
    "Take a deep breath—your inner peace is powerful 🌸.",
    "Moments of calm allow your mind to recharge 💙."
    ],
    "contentment": [
        "Contentment is peace in its purest form 🌸.",
        "This calm joy is so valuable 🌿.",
        "Sometimes ‘enough’ is the most beautiful feeling 💙."
    ],
    "love": [
        "Love is such a powerful feeling 💕. Cherish it.",
        "The love you give is never wasted 🌸.",
        "Your heart shines bright with love 💫."
    ],
    "affection": [
        "Affection makes bonds stronger 🌷.",
        "Your warmth touches others deeply 💕.",
        "Small gestures of care mean everything ✨."
    ],
    "compassion": [
        "Compassion shows your strength 💙.",
        "Your kindness creates ripples 🌊.",
        "Being gentle with others is a gift 🌿."
    ],
    "longing": [
        "Longing means you care deeply 🌸.",
        "It’s okay to miss what matters 💙.",
        "Sometimes longing points us toward our true desires 🌟."
    ],

    # --- SADNESS CLUSTER ---
    "sadness": [
        "I’m sorry you feel this way 💙. Even in dark clouds, there’s light waiting to shine on you.",
        "You matter more than you know. Your feelings are valid, and you’re not alone. 🌼",
        "Sadness comes and goes like waves. You are the ocean—bigger than the waves 🌊."
    ],
    "loneliness": [
        "Loneliness is tough 💙. Remember, you’re not invisible.",
        "Even when you feel alone, connection is possible 🌸.",
        "Reaching out can make the weight feel lighter 🌿."
    ],
    "isolated": [
        "Feeling isolated doesn’t mean you’re forgotten 💙.",
        "Your presence matters more than you know 🌸.",
        "Even distance can’t erase your worth 🌟."
    ],
    "guilt": [
        "Guilt shows you care about your actions 💙.",
        "Everyone makes mistakes—what matters is how we grow 🌱.",
        "Be gentle with yourself—you deserve compassion too 🌸."
    ],
    "ashamed": [
        "Shame can feel heavy, but it doesn’t define you 🌙.",
        "You are worthy of kindness, even when you stumble 💙.",
        "Your mistakes do not erase your value 🌸."
    ],
    "despair": [
        "Despair feels endless, but it can shift 🌿.",
        "Even in the darkest night, the stars still shine 🌌.",
        "Hold on—you are stronger than this storm 💙."
    ],
    "disappointment": [
        "Disappointment means you cared deeply 🌸.",
        "It’s okay to feel let down—healing takes time 🌿.",
        "What didn’t work out can make space for something better ✨."
    ],
    "neglect": [
        "Feeling neglected hurts 💙. You deserve to be seen.",
        "You are valuable, even if others don’t notice right now 🌟.",
        "Sometimes neglect from others teaches us to nurture ourselves 🌿."
    ],

    # --- ANGER CLUSTER ---
    "anger": [
        "It’s okay to feel angry 😡. It means you care deeply. Your feelings are valid.",
        "Anger shows passion 💥. Use it to create, not destroy—you’re in control.",
        "Even strong emotions can pass like clouds. You are bigger than your anger 🌤️."
    ],
    "irritation": [
        "Irritation is a signal—something needs your attention 🌿.",
        "It’s okay to step back and breathe before reacting 💙.",
        "Small frustrations don’t define your whole day 🌸."
    ],
    "agitation": [
        "Feeling agitated shows your energy is strong 💥.",
        "A pause can help you regain calm 🌿.",
        "Your mind and body deserve peace 💫."
    ],
    "frustration": [
        "Frustration means you’re striving for something important 🌟.",
        "It’s okay to feel stuck sometimes 💙.",
        "Every setback is a step toward growth 🌱."
    ],
    "resentment": [
        "Resentment is heavy—acknowledge it with compassion 💙.",
        "Your feelings are valid, but don’t let them trap you 🌿.",
        "Letting go can free your energy 🌸."
    ],
    "rage": [
        "Rage burns hot—find a safe way to release it 🔥.",
        "Strong emotions show you care deeply 💙.",
        "You are stronger than this moment 🌟."
    ],
    "exasperated": [
        "Being exasperated shows you’ve been carrying too much 💙.",
        "It’s okay to step back and reset 🌿.",
        "You deserve calm after the storm 🌸."
    ],

    # --- FEAR CLUSTER ---
    "fear": [
        "Fear feels heavy, but it doesn’t define you 🌙.",
        "You are safe right now 💙. Fear passes when you shine light on it.",
        "Take one step at a time. You’re braver than you think 🌟."
    ],
    "insecurity": [
        "Insecurity means you care about belonging 💙.",
        "You are enough, just as you are 🌸.",
        "Your worth is not up for debate 🌟."
    ],
    "nervousness": [
        "Nervousness is your body preparing you 🌿.",
        "It’s okay to feel butterflies—it means you care 💫.",
        "Breathe—you’ve got this 🌸."
    ],
    "anxiety": [
        "I get that anxiety feels heavy 😟. But remember—you are safe right now, and you’ve got this.",
        "Anxiety is loud, but your calm voice is still there, waiting to be heard 💫.",
        "One step at a time. You don’t need to solve everything today 💙."
    ],
    "horror": [
        "That sounds terrifying 💙. You are safe now.",
        "Even fear this strong will pass 🌌.",
        "Your courage will guide you through 🌟."
    ],
    "helplessness": [
        "Feeling helpless doesn’t mean you’re powerless 💙.",
        "Asking for support is a sign of strength 🌿.",
        "Even small steps forward matter 🌸."
    ],
    "panic": [
        "Panic can feel overwhelming—breathe slowly 💙.",
        "Ground yourself: you are here, and you are safe 🌿.",
        "This moment will pass 🌟."
    ],

    # --- SURPRISE CLUSTER ---
    "surprise": [
        "Wow! That sounds exciting 🎉.",
        "Life is full of little surprises 🌟.",
        "Unexpected moments can bring new joy 🌼."
    ],
    "amazed": [
        "Amazement brings wonder 🌠.",
        "Let the beauty of the moment sink in ✨.",
        "Life can surprise us in magical ways 🌸."
    ],
    "astonished": [
        "That’s truly astonishing 🌟.",
        "Your sense of wonder is alive 🌈.",
        "The unexpected can spark growth 🌿."
    ],
    "confused": [
        "It’s okay to feel confused—clarity will come 💫.",
        "Confusion means you’re learning 🌱.",
        "Sometimes not knowing opens new doors 🌸."
    ],
    "startled": [
        "Being startled is natural—your body is protecting you 🌙.",
        "Breathe and ground yourself 💙.",
        "The surprise has passed, you are safe 🌿."
    ],

    # --- TRUST CLUSTER ---
    "trust": [
        "Trust builds strong connections 🌿. It’s a gift you share wisely.",
        "It’s okay to lean on people you trust 💙.",
        "Trust is the bridge that makes love and friendship grow 🌸."
    ],
    "acceptance": [
        "Acceptance brings peace 🌸.",
        "You don’t need to change everything to feel whole 💙.",
        "Letting go of control can bring calm 🌿."
    ],
    "admiration": [
        "Admiration reflects the beauty you see in others 🌟.",
        "It’s inspiring to notice the good around you 💫.",
        "Your appreciation uplifts others 🌸."
    ],
    "loyalty": [
        "Loyalty strengthens bonds 🌿.",
        "Your faithfulness is a gift 💙.",
        "True loyalty is rare and beautiful 🌸."
    ],

    # --- ANTICIPATION CLUSTER ---
    "anticipation": [
        "It’s exciting to look forward to what’s coming 🌟.",
        "Good things often take time—your patience will be rewarded 🌿.",
        "The unknown can be scary, but it also brings new possibilities ✨."
    ],
    "interest": [
        "Your curiosity opens new doors 🌱.",
        "Interest means you’re engaged with life 🌟.",
        "Exploring new things can be rewarding ✨."
    ],
    "curiosity": [
        "Curiosity keeps the mind alive 🌿.",
        "Every question leads to discovery 🌟.",
        "Your wonder is a gift 🌸."
    ],
    "hope": [
        "Hope is the anchor of the soul 💙.",
        "Even a little hope carries great power 🌸.",
        "Keep believing in brighter days 🌞."
    ],

    # --- DISGUST CLUSTER ---
    "disgust": [
        "It’s okay to feel disgust—it shows your values and boundaries 🌱.",
        "Discomfort often guides us toward healthier choices 💙.",
        "Even unpleasant feelings can teach us something important 🌸."
    ],
    "revulsion": [
        "Revulsion means your instincts are protecting you 🌿.",
        "It’s okay to step back from what feels wrong 💙.",
        "Your reactions matter 🌸."
    ],
    "contempt": [
        "Contempt signals something misaligned with your values 🌱.",
        "It’s okay to reject what doesn’t feel right 💙.",
        "Noticing what you disapprove of helps define your path 🌟."
    ],
    "loathing": [
        "Loathing is strong—let it pass without clinging 🌿.",
        "Even intense disgust doesn’t define you 💙.",
        "Your energy is better spent on what you love 🌸."
    ],
}

# Optional mapping for polarity -> general emotion cluster
def detect_emotion(user_message):

    blob = TextBlob(user_message)
    polarity = blob.sentiment.polarity  # -1 to 1

    # Basic heuristic based on polarity
    if polarity > 0.5:
        # Positive emotions
        possible_emotions = ["joy", "happy", "cheerfulness", "amused", "excited", "delighted", "optimism", "hopeful", "pride", "contentment", "love", "affection", "compassion", "longing"]
    elif polarity < -0.5:
        # Negative emotions
        possible_emotions = ["sadness","sad" "loneliness", "guilt", "ashamed", "despair", "disappointment", "neglect", "anger", "irritation", "frustration", "resentment", "rage", "exasperated", "fear", "insecurity", "nervousness", "anxiety", "helplessness", "panic"]
    else:
        # Neutral / mixed emotions
        possible_emotions = ["trust", "acceptance", "admiration", "loyalty", "anticipation", "interest", "curiosity", "hope", "surprise", "amazed", "astonished", "confused", "startled", "disgust", "revulsion", "contempt", "loathing"]

    # Check if any keywords match in message to refine
    for word in user_message.lower().split():
        if word in RESPONSES:
            return word  # direct match with response category

    words = user_message.lower().split()
    all_categories = list(RESPONSES.keys())
    for word in words:
        match = difflib.get_close_matches(word, all_categories, n=1, cutoff=0.60)
        if match:
            return match[0]  # closest match found


    # If no keyword matches, pick a random one from the cluster
    ans ="Don't afraid feel free to talk to me"
    #return random.choice(possible_emotions)
    return ans


def best_match(user_message):
    category = detect_emotion(user_message)
    # Pick a random response from that category
    response_list = RESPONSES.get(category, ["Don't afraid feel free to talk to me! 💙"])
    return random.choice(response_list)

# Home Page
@app.route("/")
def index():
    return render_template("index.html")

# Exercises Menu
@app.route("/exercises")
def exercises():
    return render_template("exercises.html")

# Individual Exercises
@app.route("/exercise/breathing")
def exercise_breathing():
    return render_template("exercise_breathing.html")

@app.route("/exercise/body_scan")
def exercise_body_scan():
    return render_template("exercise_body_scan.html")

@app.route("/exercise/visualization")
def exercise_visualization():
    return render_template("exercise_visualization.html")

# Relax Game (color puzzle example)
@app.route("/game")
def game():
    return render_template("game.html")

# Chat (simple chatbot page)
@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.json.get("message", "")
    reply = best_match(user_message)
    return jsonify({"reply": reply})

@app.route("/relaxing_games")
def relaxing_games():
    return render_template("relaxing_games.html")

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

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=8000)
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
    port = int(os.environ.get("PORT", 8000))  # default 8000 locally
    app.run(debug=True, host="0.0.0.0", port=port)




# from flask import Flask, render_template

# app = Flask(__name__)

# # Home Page
# @app.route("/")
# def index():
#     return render_template("index.html")

# # Exercises Menu
# @app.route("/exercises")
# def exercises():
#     return render_template("exercises.html")

# # Individual Exercises
# @app.route("/exercise/breathing")
# def exercise_breathing():
#     return render_template("exercise_breathing.html")

# @app.route("/exercise/body_scan")
# def exercise_body_scan():
#     return render_template("exercise_body_scan.html")

# @app.route("/exercise/visualization")
# def exercise_visualization():
#     return render_template("exercise_visualization.html")

# # Relax Game (color puzzle example)
# @app.route("/game")
# def game():
#     return render_template("game.html")

# # Chat (simple chatbot page)
# @app.route("/chat")
# def chat():
#     return render_template("chat.html")


# if __name__ == "__main__":
#     app.run(debug=True)
