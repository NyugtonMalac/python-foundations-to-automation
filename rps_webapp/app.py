from flask import Flask, request, render_template_string, session

app = Flask(__name__)
app.secret_key = "change-me-to-a-random-secret"

OPTIONS = ["rock", "paper", "scissors"]
WINS_P2 = {"rock_paper", "paper_scissors", "scissors_rock"}

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Rock • Paper • Scissors</title>
</head>
<body style="font-family: system-ui; max-width: 760px; margin: 40px auto; line-height:1.5; padding: 0 14px;">
  <h1>Rock • Paper • Scissors</h1>

  {% if not game.started %}
    <p>
      Hello,<br><br>
      Welcome to the Rock-Paper-Scissors game.<br><br>
      To ensure that the game has a clear winner, an odd number of rounds must be played.<br>
      If both players choose the same move, the round is a tie and will be replayed.
    </p>

    <form method="post">
      <input type="hidden" name="action" value="start">
      <label><strong>How many rounds would you like to play?</strong> (odd number)</label><br>
      <input name="rounds" type="number" min="1" step="1" style="padding:8px; width:160px;" required>
      <button style="padding:8px 12px;">Start</button>
    </form>

    {% if error %}
      <p style="color:#b00020; margin-top:14px;"><strong>{{ error }}</strong></p>
    {% endif %}

  {% else %}
    <p>
      <strong>Rounds:</strong> {{ game.rounds }} |
      <strong>Score:</strong> Player 1: {{ game.p1 }} — Player 2: {{ game.p2 }} |
      <strong>Valid round:</strong> {{ game.turn }} / {{ game.rounds }}
    </p>

    {% if game.finished %}
      <hr>
      <h2>>>>> And the winner is: {{ game.winner }}. <<<<<</h2>
      <p>Congratulations!<br>See you next time!</p>

      <form method="post">
        <input type="hidden" name="action" value="reset">
        <button style="padding:8px 12px;">New game</button>
      </form>

    {% else %}
      <hr>
      {% if game.awaiting_p2 %}
        <h3>Player 2, choose your move:</h3>
        <p><em>(Player 1 has already chosen.)</em></p>
      {% else %}
        <h3>Player 1, choose your move:</h3>
      {% endif %}

      <form method="post">
        <input type="hidden" name="action" value="move">
        <button name="move" value="rock" style="padding:10px 14px;">🪨 Rock</button>
        <button name="move" value="paper" style="padding:10px 14px;">📄 Paper</button>
        <button name="move" value="scissors" style="padding:10px 14px;">✂️ Scissors</button>
      </form>

      {% if message %}
        <p style="margin-top:16px;"><strong>{{ message }}</strong></p>
      {% endif %}
    {% endif %}
  {% endif %}
</body>
</html>
"""

def new_game():
    session["started"] = False
    session["rounds"] = 0
    session["turn"] = 1
    session["p1"] = 0
    session["p2"] = 0
    session["awaiting_p2"] = False
    session["p1_move"] = None
    session["finished"] = False
    session["winner"] = None

def get_state():
    return {
        "started": session.get("started", False),
        "rounds": session.get("rounds", 0),
        "turn": session.get("turn", 1),
        "p1": session.get("p1", 0),
        "p2": session.get("p2", 0),
        "awaiting_p2": session.get("awaiting_p2", False),
        "p1_move": session.get("p1_move"),
        "finished": session.get("finished", False),
        "winner": session.get("winner"),
    }

@app.before_request
def ensure_session():
    if "started" not in session:
        new_game()

@app.route("/", methods=["GET", "POST"])
def home():
    error = None
    message = None

    if request.method == "POST":
        action = (request.form.get("action") or "").strip().lower()

        # RESET
        if action == "reset":
            new_game()
            message = "New game started."

        # START GAME
        elif action == "start" and not session.get("started", False):
            try:
                rounds_num = int(request.form.get("rounds", "0"))
            except ValueError:
                rounds_num = 0

            if rounds_num <= 0:
                error = "Please enter a positive number of rounds."

            elif rounds_num % 2 == 0:
                error = "Please enter an ODD number of rounds (e.g., 3, 5, 7)."

            else:
                session["started"] = True
                session["rounds"] = rounds_num
                session["turn"] = 1
                session["p1"] = 0
                session["p2"] = 0
                session["awaiting_p2"] = False
                session["p1_move"] = None
                session["finished"] = False
                session["winner"] = None
                message = "Game started! Player 1, choose your move."

        # MOVE
        elif action == "move" and session.get("started", False) and not session.get("finished", False):
            mv = (request.form.get("move") or "").strip().lower()
            if mv not in OPTIONS:
                message = "Invalid choice. Please try again."
            else:
                # Player 1 move
                if not session.get("awaiting_p2", False):
                    session["p1_move"] = mv
                    session["awaiting_p2"] = True
                    message = "Player 1 has chosen. Player 2, your turn."

                # Player 2 move
                else:
                    p1 = session.get("p1_move")
                    p2 = mv

                    if p1 == p2:
                        session["p1_move"] = None
                        session["awaiting_p2"] = False
                        message = "It's a tie! The round will be replayed."
                    else:
                        key = f"{p1}_{p2}"
                        if key in WINS_P2:
                            session["p2"] += 1
                            point_to = "Player 2"
                        else:
                            session["p1"] += 1
                            point_to = "Player 1"

                        message = f"Player 1 chose: {p1} | Player 2 chose: {p2} | Point goes to: {point_to}"

                        session["turn"] += 1
                        session["p1_move"] = None
                        session["awaiting_p2"] = False

                        if session["turn"] > session["rounds"]:
                            session["finished"] = True
                            session["winner"] = (
                                "Player 2"
                                if session["p2"] > session["p1"]
                                else "Player 1"
                            )

    return render_template_string(HTML, game=get_state(), error=error, message=message)
