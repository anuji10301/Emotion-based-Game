from flask import Flask, render_template_string, request

app = Flask(__name__)

# Homepage with Bootstrap cards
@app.route('/')
def home():
    return render_template_string('''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Mind Relax App</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: linear-gradient(-45deg, #a8edea, #fed6e3, #fbc2eb, #a6c1ee);
                background-size: 400% 400%;
                animation: gradientBG 15s ease infinite;
            }
            @keyframes gradientBG {
                0% {background-position: 0% 50%;}
                50% {background-position: 100% 50%;}
                100% {background-position: 0% 50%;}
            }
            .card:hover {transform: scale(1.05); transition: 0.3s;}
            .breathing-circle {
                width: 150px; height: 150px;
                border-radius: 50%;
                background: rgba(255,255,255,0.6);
                margin: 20px auto;
                animation: breathe 8s ease-in-out infinite;
            }
            @keyframes breathe {
                0% {transform: scale(1);}
                50% {transform: scale(1.3);}
                100% {transform: scale(1);}
            }
        </style>
    </head>
    <body class="bg-light">
        <audio autoplay loop>
            <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
        </audio>
        <div class="container py-5">
            <h1 class="text-center mb-4">🌸 Mind Relax App 🌸</h1>
            <div class="breathing-circle"></div>
            <div class="row g-4">
                <div class="col-md-4">
                    <div class="card shadow-lg h-100">
                        <div class="card-body text-center">
                            <h5 class="card-title">🎮 Relax Game</h5>
                            <p class="card-text">Play a simple calming focus game to relax your mind.</p>
                            <a href="{{ url_for('game') }}" class="btn btn-primary">Play</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card shadow-lg h-100">
                        <div class="card-body text-center">
                            <h5 class="card-title">🧘 Relax Exercises</h5>
                            <p class="card-text">Guided breathing and mindfulness exercises.</p>
                            <a href="{{ url_for('exercise') }}" class="btn btn-success">Start</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card shadow-lg h-100">
                        <div class="card-body text-center">
                            <h5 class="card-title">💬 Calm Chat</h5>
                            <p class="card-text">Chat with a supportive bot to relax and reflect.</p>
                            <a href="{{ url_for('chat') }}" class="btn btn-info">Chat</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''')

# Relax Game Page
@app.route('/game')
def game():
    return render_template_string('''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Relax Game</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .circle {
                width: 80px; height: 80px;
                border-radius: 50%;
                display: inline-block;
                margin: 10px;
                cursor: pointer;
            }
            #message {font-size: 1.2em; margin-top: 15px;}
        </style>
    </head>
    <body class="text-center p-5">
        <h2>🎮 Relax Game</h2>
        <p>Click only the <b>blue circles</b> to relax and focus 💙</p>
        <div id="game"></div>
        <div id="message"></div>
        <a href="/" class="btn btn-secondary mt-3">Back</a>

        <script>
            const gameDiv = document.getElementById('game');
            const message = document.getElementById('message');
            let score = 0;

            function startGame() {
                gameDiv.innerHTML = '';
                const colors = ['red','blue','green','yellow','pink','blue','purple','blue'];
                colors.sort(() => Math.random() - 0.5);
                colors.forEach(c => {
                    let circle = document.createElement('div');
                    circle.className = 'circle';
                    circle.style.background = c;
                    circle.onclick = () => checkColor(c);
                    gameDiv.appendChild(circle);
                });
            }

            function checkColor(color) {
                if(color === 'blue') {
                    score++;
                    message.innerHTML = "✅ Great! Keep calm. Score: " + score;
                } else {
                    message.innerHTML = "❌ Oops! Focus only on blue. Score: " + score;
                }
                setTimeout(startGame, 1000);
            }

            startGame();
        </script>
    </body>
    </html>
    ''')

# Relax Exercise Page
@app.route('/exercise')
def exercise():
    return render_template_string('''
    <div class="container py-5">
        <h2>🧘 Relax Exercises</h2>
        <ul>
            <li><b>Box Breathing:</b> Inhale 4s → Hold 4s → Exhale 4s → Hold 4s</li>
            <li><b>4-7-8 Breathing:</b> Inhale 4s → Hold 7s → Exhale 8s</li>
            <li><b>Visualization:</b> Imagine a peaceful place 🌅</li>
        </ul>
        <a href="/" class="btn btn-secondary">Back</a>
    </div>
    ''')

# Calm Chat Page
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    response = ""
    if request.method == 'POST':
        user_msg = request.form.get('message')
        if any(word in user_msg.lower() for word in ["stress", "anxiety", "angry"]):
            response = "I hear you. Let's take a deep breath together 🌬️ Inhale… Exhale…"
        elif "happy" in user_msg.lower():
            response = "That's wonderful! Keep embracing positivity 🌸"
        else:
            response = "I'm here to listen. You’re not alone 💙"
    return render_template_string('''
    <div class="container py-5">
        <h2>💬 Calm Chat</h2>
        <form method="POST">
            <textarea name="message" class="form-control mb-2" placeholder="Type your feelings here..."></textarea>
            <button type="submit" class="btn btn-info">Send</button>
        </form>
        {% if response %}
        <div class="alert alert-primary mt-3">{{ response }}</div>
        {% endif %}
        <a href="/" class="btn btn-secondary mt-3">Back</a>
    </div>
    ''', response=response)

if __name__ == '__main__':
    app.run(debug=True)
