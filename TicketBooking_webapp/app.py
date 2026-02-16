"""
Ticket Booking Web App (Terminal-Style UI)

A small Flask web application that recreates a terminal-like ticket booking flow
in the browser. The app is designed to be embed-friendly (e.g., in a WordPress
site via iframe) and uses session-based state to keep the interaction smooth.

What the app does:
- Displays a list of movies and lets the user select one.
- Shows a 5x5 seating layout represented as a list of lists.
- Lets the user choose how many tickets to book.
- Reserves seats step-by-step (row + seat) with validation:
  - seat coordinates must be within the 5x5 range
  - the seat must be available
- Updates the seating layout after each reservation.
- Finalizes the booking by marking reserved seats as purchased.

Implementation highlights:
- Single Flask route ("/") handling the full flow.
- Session state controls "screens" (phases), so the UI behaves like a
  cleared terminal between steps (no scrolling history needed).
- Simple, readable state model suitable for learning and portfolio demos.

Part of the "Python Foundations to Automation" learning path.
"""



from flask import Flask, request, render_template_string, session
from markupsafe import Markup


app = Flask(__name__)
app.secret_key = "change-me-to-a-random-secret"  # use a strong secret in production

# =========================
# CONFIG YOU CUSTOMIZE
# =========================
APP_TITLE = "Ticket Booking (Terminal Demo)"
APP_SUBTITLE = "Flask mini-app • terminal-style UI • session-based state • embed-friendly (WordPress iframe)"

# =========================
# UI (HTML/CSS/JS)
# =========================
HTML = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }}</title>

  <style>
    :root{
      --bg1:#0b1220;
      --bg2:#140d1a;
      --panel:#0f1a2a;
      --panel2:#0b1422;
      --line: rgba(255,255,255,.08);
      --txt: rgba(255,255,255,.90);
      --muted: rgba(255,255,255,.70);

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

    .seat { font-weight: 700; }
    .seat.av { color: var(--ok); }        /* Available */
    .seat.booked { color: var(--err); }   /* Booked */
    .seat.sel { color: #4dabff; }         /* Selected */
    .seat.bought { color: #c77dff; }      /* Bought */


    .wrap{ max-width: 980px; margin: 0 auto; padding: 28px 16px 40px; }
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

    h1{ margin:0 0 6px 0; font-size: 34px; letter-spacing: .5px; }
    .sub{ margin:0 0 18px 0; color: var(--muted); font-size: 13px; }

    .card{
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 14px 14px 12px;
      background: rgba(10,16,28,.55);
    }

    .hr{ margin: 16px 0; border: 0; border-top: 1px solid var(--line); }

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

    label{ color: var(--txt); font-weight: 700; font-size: 14px; }

    input[type="number"], select{
      margin-top: 8px;
      padding: 10px 12px;
      width: 280px;
      max-width: 100%;
      border-radius: 12px;
      border: 1px solid var(--line);
      background: rgba(0,0,0,.25);
      color: var(--txt);
      outline: none;
      font-size: 16px;
    }
    input:focus, select:focus{
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

    .actions{ display:flex; gap: 10px; align-items: center; flex-wrap: wrap; margin-top: 10px; }
    .alwaysbar{ display:flex; justify-content: flex-end; margin-top: 12px; }

    /* terminal-like block */
    pre.terminal{
      margin: 0;
      padding: 12px;
      border-radius: 12px;
      border: 1px solid var(--line);
      background: rgba(0,0,0,.22);
      overflow-x: auto;
      color: var(--txt);
      font-size: 14px;
      line-height: 1.5;
      white-space: pre;
    }

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

        <h1>{{ title }}</h1>
        <p class="sub">{{ subtitle }}</p>

        <button id="focusCatcher" type="button" aria-hidden="true" tabindex="-1">.</button>

        <div class="card">
          <pre class="terminal">{{ ui.screen_text }}</pre>

          <hr class="hr">

          {% if ui.finished %}
            <div class="msg ok"><strong>{{ ui.finished_message }}</strong></div>
          {% else %}
            <form method="post" autocomplete="off">
              <input type="hidden" name="action" value="step">
              <input type="hidden" name="phase" value="{{ ui.phase }}">

              {% if ui.phase == "movie" %}
                <label>Select a movie:</label><br>
                <div class="actions">
                  <select name="movie_id" required>
                    {% for mid, title in ui.movies %}
                      <option value="{{ mid }}">{{ mid }}. {{ title }}</option>
                    {% endfor %}
                  </select>
                  <button class="btn" type="submit">Continue</button>
                </div>

              {% elif ui.phase == "tickets" %}
                <label>How many tickets would you like to book?</label><br>
                <div class="actions">
                  <input name="ticket_count" type="number" min="1" max="25" required>
                  <button class="btn" type="submit">Continue</button>
                </div>

              {% elif ui.phase == "seat" %}
                <label>Choose row and seat:</label><br>
                <div class="actions">
                  <select name="row" required>
                    {% for n in ui.range_1_5 %}<option value="{{ n }}">Row {{ n }}</option>{% endfor %}
                  </select>
                  <select name="seat" required>
                    {% for n in ui.range_1_5 %}<option value="{{ n }}">Seat {{ n }}</option>{% endfor %}
                  </select>
                  <button class="btn" type="submit">Reserve</button>
                </div>

              {% endif %}
            </form>

            {% if error %}
              <div class="msg err"><strong>{{ error }}</strong></div>
            {% endif %}
            {% if message %}
              <div class="msg ok"><strong>{{ message }}</strong></div>
            {% endif %}
          {% endif %}
        </div>

        <div class="alwaysbar">
          <form method="post">
            <input type="hidden" name="action" value="reset">
            <button class="btn small" type="submit">Reset</button>
          </form>
        </div>

      </div>
    </div>
  </div>

  <script>
    // Prevent the "jump to top" + do NOT break <select> dropdowns.
    (function () {
      function safeBlur(el){
        try { el && el.blur && el.blur(); } catch(e) {}
      }

      document.addEventListener("click", function(e){
        const t = e.target;

        // If the user clicks an interactive control, DO NOT blur it.
        // Otherwise dropdowns close instantly.
        if (t && (t.closest("select") || t.closest("option") || t.closest("input") || t.closest("button") || t.closest("textarea") || t.closest("label"))) {
          return;
        }

        // Clicked outside inputs -> remove focus (helps iOS keyboard).
        safeBlur(document.activeElement);
      }, { passive: true });
    })();
  </script>
</body>
</html>
"""

# =========================
# DATA (static)
# =========================
MOVIES = {
    1: "Twilight",
    2: "The Vampire Diaries",
    3: "Only Lovers Left Alive",
    4: "Underworld",
    5: "Interview with the Vampire",
    6: "Queen of the Damned",
    7: "Warm Bodies",
    8: "Let the Right One In",
    9: "Jennifer’s Body",
    10: "The Craft",
}

# 0=available, 4=booked (preset), 2=selected (reserved), 3=bought (final)
DEFAULT_AUDITORIUM = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 4, 4],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 4, 4, 0, 0],
]


# =========================
# SESSION STATE
# =========================
def init_state():
    session["started"] = True            # we always show the app "running"
    session["finished"] = False

    session["phase"] = "movie"           # movie -> tickets -> seat -> summary
    session["movie_id"] = None
    session["ticket_count"] = None
    session["reserved_count"] = 0
    session["auditorium"] = [row[:] for row in DEFAULT_AUDITORIUM]


def state():
    return {
        "started": session.get("started", True),
        "finished": session.get("finished", False),
        "phase": session.get("phase", "movie"),
        "movie_id": session.get("movie_id"),
        "ticket_count": session.get("ticket_count"),
        "reserved_count": session.get("reserved_count", 0),
        "auditorium": session.get("auditorium", [row[:] for row in DEFAULT_AUDITORIUM]),
    }


@app.before_request
def ensure_session():
    if "phase" not in session:
        init_state()


# =========================
# RENDER HELPERS
# =========================
def seat_legend():
    return (
        "Legend: [ ] Available   [X] Booked   [~] Selected   [$] Bought\n"
    )


def seat_symbol(val: int) -> str:
    if val == 0:
        return '<span class="seat av">[ ]</span>'
    if val == 2:
        return '<span class="seat sel">[~]</span>'
    if val == 3:
        return '<span class="seat bought">[$]</span>'
    return '<span class="seat booked">[X]</span>'   # booked or other


def seating_text(auditorium):
    lines = []
    lines.append(seat_legend().rstrip())
    lines.append("")
    for r_idx, row in enumerate(auditorium, start=1):
        parts = [f"Row {r_idx}:"]
        for c_idx, seat in enumerate(row, start=1):
            parts.append(f"{c_idx}:{seat_symbol(seat)}")
        lines.append("  " + " ".join(parts))
    return "\n".join(lines)


def build_screen_text(st):
    phase = st["phase"]
    movie_id = st["movie_id"]
    movie_title = MOVIES.get(movie_id) if movie_id else None

    if phase == "movie":
        movie_lines = ["Hello!", "", "Welcome to the Ticket Booking Tool.", "", "Now showing in theaters today:"]
        for mid in sorted(MOVIES):
            movie_lines.append(f"  {mid}. {MOVIES[mid]}")
        movie_lines.append("")
        movie_lines.append("Please select the movie you would like to watch.")
        return "\n".join(movie_lines)

    if phase == "tickets":
        return (
            f'Thank you! Selected movie is "{movie_title}".\n\n'
            "Here is the seating layout:\n\n"
            f"{seating_text(st['auditorium'])}\n\n"
            "How many tickets would you like to book?"
        )

    if phase == "seat":
        total = st["ticket_count"]
        done = st["reserved_count"]
        return (
            f'Ticket booking for: "{movie_title}"\n'
            f"Progress: {done} / {total} reserved\n\n"
            f"{seating_text(st['auditorium'])}\n\n"
            f"Please enter the details for seat number {done + 1}."
        )

    # summary
    total = st["ticket_count"]
    return (
        "Thank you.\n"
        f"All {total} out of {total} seats have been successfully reserved for \"{movie_title}\":\n\n"
        f"{seating_text(st['auditorium'])}\n\n"
        "We look forward to seeing you again!"
    )


# =========================
# LOGIC
# =========================
def handle_step(form):
    st = state()
    phase = st["phase"]
    auditorium = st["auditorium"]

    if phase == "movie":
        raw = (form.get("movie_id") or "").strip()
        if not raw.isdigit():
            return None, "Please select a valid movie number."
        mid = int(raw)
        if mid not in MOVIES:
            return None, "Please select a movie from the list."
        session["movie_id"] = mid
        session["phase"] = "tickets"
        return f'Selected: "{MOVIES[mid]}"', None

    if phase == "tickets":
        raw = (form.get("ticket_count") or "").strip()
        if not raw.isdigit():
            return None, "Please enter a whole number for tickets."
        n = int(raw)
        if n < 1:
            return None, "Please book at least 1 ticket."
        session["ticket_count"] = n
        session["reserved_count"] = 0
        session["phase"] = "seat"
        return f"Booking {n} ticket(s).", None

    if phase == "seat":
        # row/seat are dropdowns -> should always be digits, still validate
        row_raw = (form.get("row") or "").strip()
        seat_raw = (form.get("seat") or "").strip()
        if not (row_raw.isdigit() and seat_raw.isdigit()):
            return None, "Please choose a valid row and seat."

        row = int(row_raw)
        seat = int(seat_raw)
        if row not in (1, 2, 3, 4, 5) or seat not in (1, 2, 3, 4, 5):
            return None, "Row and seat must be between 1 and 5."

        if auditorium[row - 1][seat - 1] != 0:
            return None, "That seat is already booked. Please choose another one."

        # reserve
        auditorium[row - 1][seat - 1] = 2
        session["auditorium"] = auditorium
        session["reserved_count"] = session.get("reserved_count", 0) + 1

        # finished?
        if session["reserved_count"] >= session.get("ticket_count", 0):
            # finalize: convert selected (2) to bought (3)
            for r_i, r in enumerate(auditorium):
                for c_i, v in enumerate(r):
                    if v == 2:
                        auditorium[r_i][c_i] = 3
            session["auditorium"] = auditorium
            session["phase"] = "summary"
            session["finished"] = True
            return "Reservation complete.", None

        return f"Reserved Row {row}, Seat {seat}.", None

    return None, None


def build_ui(error=None, message=None):
    st = state()
    ui = {
        "phase": st["phase"],
        "finished": st["finished"],
        "finished_message": "Done. You can start a new run with Reset.",
        "movies": [(mid, MOVIES[mid]) for mid in sorted(MOVIES)],
        "range_1_5": [1, 2, 3, 4, 5],
        "screen_text": Markup(build_screen_text(st)),
    }
    return ui


# =========================
# ROUTE
# =========================
@app.route("/", methods=["GET", "POST"])
def home():
    error = None
    message = None

    if request.method == "POST":
        action = (request.form.get("action") or "").strip().lower()

        if action == "reset":
            init_state()
            message = "Reset complete."

        elif action == "step":
            msg, err = handle_step(request.form)
            message = msg
            error = err

    ui = build_ui(error=error, message=message)
    return render_template_string(
        HTML,
        title=APP_TITLE,
        subtitle=APP_SUBTITLE,
        ui=ui,
        error=error,
        message=message,
    )


if __name__ == "__main__":
    app.run(debug=True)
