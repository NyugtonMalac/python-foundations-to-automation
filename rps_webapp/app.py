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
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Rock • Paper • Scissors</title>
  <style>
    :root{
      --bg1:#0b1220;
      --bg2:#140d1a;
      --panel:#0f1a2a;
      --panel2:#0b1422;
      --line: rgba(255,255,255,.08);
      --txt: rgba(255,255,255,.90);
      --muted: rgba(255,255,255,.70);

      --p1:#ff4d6d;   /* Player 1 color */
      --p2:#4dabff;   /* Player 2 color */

      --ok:#21c997;
      --warn:#ffb703;
      --err:#ff5c8a;
      --btn:#162236;
      --btn2:#1a2b45;
    }

    html, body { height: 100%; }
    body{
      margin:0;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      color: var(--txt);
      background:
        radial-gradient(1200px 600px at 20% 10%, rgba(45,138,255,.25), transparent 60%),
        radial-gradient(900px 500px at 85% 20%, rgba(255,0,128,.18), transparent 60%),
        linear-gradient(140deg, var(--bg1), var(--bg2));
    }

    .wrap{
      max-width: 980px;
      margin: 0 auto;
      padding: 28px 16px 40px;
    }

    .frame{
      border: 1px solid var(--line);
      border-radius: 18px;
      background: rgba(8,12,20,.55);
      box-shadow: 0 18px 60px rgba(0,0,0,.45);
      padding: 18px;
    }

    .app{
      border: 1px solid var(--line);
      border-radius: 16px;
      background: linear-gradient(180deg, rgba(15,26,42,.82), rgba(10,16,28,.72));
      padding: 20px;
    }

    h1{
      margin:0 0 6px 0;
      font-size: 36px;
      letter-spacing: .5px;
    }

    .sub{
      margin:0 0 18px 0;
      color: var(--muted);
      font-size: 13px;
    }

    .row{
      display:flex;
      gap: 16px;
      flex-wrap: wrap;
    }

    .card{
      flex: 1 1 280px;
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 14px 14px 12px;
      background: rgba(10,16,28,.55);
    }

    .hr{
      margin: 16px 0;
      border: 0;
      border-top: 1px solid var(--line);
    }

    .kbd{
      display:inline-block;
      padding: 2px 8px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: rgba(255,255,255,.04);
      font-size: 12px;
      color: var(--muted);
    }

    .p1{ color: var(--p1); font-weight: 700; }
    .p2{ color: var(--p2); font-weight: 700; }

    .scoreline{
      line-height: 1.6;
      color: var(--muted);
      font-size: 14px;
    }

    .scoreline b{
      color: var(--txt);
    }

    .msg{
      margin-top: 12px;
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 12px 12px;
      background: rgba(255,255,255,.04);
      color: var(--txt);
      font-size: 14px;
    }

    .msg.ok{ border-color: rgba(33,201,151,.35); background: rgba(33,201,151,.10); }
    .msg.err{ border-color: rgba(255,92,138,.40); background: rgba(255,92,138,.10); }

    label{
      color: var(--txt);
      font-weight: 700;
      font-size: 14px;
    }

    input[type="number"]{
      margin-top: 8px;
      padding: 10px 12px;
      width: 220px;
      max-width: 100%;
      border-radius: 12px;
      border: 1px solid var(--line);
      background: rgba(0,0,0,.25);
      color: var(--txt);
      outline: none;
      font-size: 16px;
    }

    input[type="number"]:focus{
      border-color: rgba(77,171,255,.55);
      box-shadow: 0 0 0 3px rgba(77,171,255,.18);
    }

    .btn{
      appearance:none;
      border: 1px solid var(--line);
      background: linear-gradient(180deg, rgba(22,34,54,.9), rgba(18,28,45,.9));
      color: var(--txt);
      padding: 10px 14px;
      border-radius: 12px;
      cursor: pointer;
      font-weight: 700;
    }

    .btn:hover{ background: linear-gradient(180deg, rgba(26,43,69,.95), rgba(18,28,45,.95)); }
    .btn:active{ transform: translateY(1px); }

    .btn.small{ padding: 8px 12px; font-size: 13px; border-radius: 10px; }

    .actions{
      display:flex;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
      margin-top: 10px;
    }

    .moves{
      display:flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 10px;
    }

    .movebtn{
      border: 1px solid var(--line);
      background: rgba(255,255,255,.04);
      color: var(--txt);
      padding: 12px 14px;
      border-radius: 12px;
      cursor: pointer;
      min-width: 140px;
      text-align: left;
      font-weight: 800;
      font-size: 14px;
      display:flex;
      align-items:center;
      gap: 10px;
    }
    .movebtn:hover{ background: rgba(255,255,255,.07); }
    .movebtn:active{ transform: translateY(1px); }

    .tip{
      color: var(--muted);
      font-size: 12px;
      margin-top: 10px;
    }

    .alwaysbar{
      display:flex;
      justify-content: flex-end;
      margin-top: 12px;
    }

    /* tiny focus-catcher to reduce iOS weird focusing */
    #focusCatcher{
      position: absolute;
      left: -10000px;
      top: -10000px;
      opacity: 0;
      height: 1px;
      width: 1px;
    }
  </style>
</head>

<body>
  <div class="wrap">
    <div class="frame">
      <div class="app">
        <h1>Rock • Paper • Scissors</h1>
        <p class="sub">Deployed Flask mini app (terminal-style UI) • session-based state • two-player mode.</p>

        <!-- focus-catcher: helps on some iOS cases -->
        <button id="focusCatcher" type="button" aria-hidden="true" tabindex="-1">.</button>

        {% if not game.started %}
          <div class="card">
            <p class="scoreline">
              To ensure a clear winner, the game must have an <b>odd</b> number of rounds.<br>
              If both players choose the same move, the round is a tie and will be replayed.
            </p>

            <form method="post" autocomplete="off">
              <input type="hidden" name="action" value="start">
              <label>How many rounds would you like to play? <span class="kbd">(odd number)</span></label><br>
              <div class="actions">
                <input name="rounds" type="number" min="1" step="1" inputmode="numeric" required>
                <button class="btn" type="submit">Start</button>
              </div>
            </form>

            {% if error %}
              <div class="msg err"><strong>{{ error }}</strong></div>
            {% endif %}

          </div>

          <div class="alwaysbar">
            <form method="post">
              <input type="hidden" name="action" value="reset">
              <button class="btn small" type="submit">New game</button>
            </form>
          </div>

        {% else %}
          <div class="row">
            <div class="card">
              <div class="scoreline">
                <div><b>Rounds:</b> {{ game.rounds }}</div>
                <div>
                  <b>Score:</b>
                  <span class="p1">Player 1</span>: {{ game.p1 }}
                  — <span class="p2">Player 2</span>: {{ game.p2 }}
                </div>
                <div><b>Valid round:</b> {{ game.turn }} / {{ game.rounds }}</div>
              </div>
            </div>
          </div>

          <hr class="hr">

          {% if game.finished %}
            <div class="card">
              <h2 style="margin:0 0 8px 0;">>>>>> And the winner is: <span class="{{ 'p2' if game.winner == 'Player 2' else 'p1' }}">{{ game.winner }}</span>. <<<<<</h2>
              <div class="msg ok">
                Congratulations!<br>
                See you next time!
              </div>

              <div class="actions" style="margin-top:12px;">
                <form method="post">
                  <input type="hidden" name="action" value="reset">
                  <button class="btn" type="submit">New game</button>
                </form>
              </div>
            </div>

          {% else %}
            <div class="card">
              {% if game.awaiting_p2 %}
                <h3 style="margin:0 0 6px 0;"><span class="p2">Player 2</span>, choose your move:</h3>
                <p class="sub" style="margin:0 0 8px 0;">(Player 1 has already chosen.)</p>
              {% else %}
                <h3 style="margin:0 0 10px 0;"><span class="p1">Player 1</span>, choose your move:</h3>
              {% endif %}

              <form id="moveForm" method="post" autocomplete="off">
                <input type="hidden" name="action" value="move">
                <input type="hidden" name="move" id="moveValue" value="">
                <div class="moves">
                  <!-- type=button so iOS won't treat as implicit submit/focus weirdness -->
                  <button class="movebtn" type="button" data-move="rock">🪨 Rock</button>
                  <button class="movebtn" type="button" data-move="paper">📄 Paper</button>
                  <button class="movebtn" type="button" data-move="scissors">✂️ Scissors</button>
                </div>
              </form>

              {% if message %}
                <div class="msg ok"><strong>{{ message }}</strong></div>
              {% endif %}

              <div class="tip">Tip: Use <b>New game</b> to reset the session.</div>
            </div>

            <div class="alwaysbar">
              <form method="post">
                <input type="hidden" name="action" value="reset">
                <button class="btn small" type="submit">New game</button>
              </form>
            </div>
          {% endif %}
        {% endif %}
      </div>
    </div>
  </div>

  <script>
    (function () {
      const form = document.getElementById("moveForm");
      if (!form) return;

      const moveValue = document.getElementById("moveValue");
      const focusCatcher = document.getElementById("focusCatcher");

      function safeBlur(el){
        try { el && el.blur && el.blur(); } catch(e) {}
      }

      form.addEventListener("click", function (e) {
        const btn = e.target.closest("button[data-move]");
        if (!btn) return;

        // set move and submit
        moveValue.value = btn.getAttribute("data-move");

        // prevent iOS from re-focusing inputs / popping keyboard
        safeBlur(btn);
        safeBlur(document.activeElement);
        if (focusCatcher) { try { focusCatcher.focus(); } catch(e) {} }

        form.submit();
      }, { passive: true });
    })();
  </script>
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
                            session["winner"] = "Player 2" if session["p2"] > session["p1"] else "Player 1"

    return render_template_string(HTML, game=get_state(), error=error, message=message)
