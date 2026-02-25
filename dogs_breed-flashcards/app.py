"""
Dog Grooming Flashcard – Flask Web Application

This module provides the complete web interface layer for the
Dog Grooming Flashcard system.

Architecture
------------
Game Engine (game_engine_DBFG.py)
    ↓
Persistence Layer (helpers/save_manager.py)
    ↓
Authentication Layer (helpers/auth_utils.py)
    ↓
Flask Web Layer (this file)
    ↓
Jinja2 Templates

Core Responsibilities
---------------------
- Handle authentication and sessions
- Orchestrate FlashcardGame lifecycle
- Manage persistent user progress
- Render question / review / result / finish views
- Provide reset functionality

State Management
----------------
- Logged-in user stored in Flask session
- Current card ID stored in session
- Full game state persisted in saves/<username>.json

Routes Overview
---------------
/           → Redirect to login or play
/login      → Authentication
/logout     → End session
/play       → Show next question
/review     → Compare user answers
/result     → Apply round result & save state
/finish     → End-of-session summary
/reset      → Delete saved progress

This file intentionally contains no business logic.
All domain logic is delegated to FlashcardGame.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, session

from helpers.path_utils import set_base_dir
from helpers.auth_utils import verify_user
from helpers.save_manager import save_state, load_state, delete_state

from game_engine_DBFG import FlashcardGame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
set_base_dir(BASE_DIR)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")


# -------------------------
# Helpers
# -------------------------
def require_login():
    """
    Check whether a user is authenticated.

    Returns:
        True if a valid user is present in session,
        otherwise False.
    """

    return "user" in session and session["user"]


def build_game_for_user(username: str) -> FlashcardGame:
    """
    Create and initialize a FlashcardGame instance for a given user.

    Steps:
    1. Instantiate a fresh game engine
    2. Load base card dataset (dogs.json)
    3. Load previously saved state (if exists)
    4. Apply saved state to engine

    Args:
        username: Authenticated username

    Returns:
        Fully initialized FlashcardGame instance
    """

    game = FlashcardGame()
    game.load_cards(file_name="dogs")

    state = load_state(username)
    if state:
        game.apply_state(state)

    return game


# -------------------------
# Routes
# -------------------------
@app.route("/")
def index():
    """
    Entry point of the application.

    Redirect logic:
    - If not authenticated → login page
    - If authenticated → gameplay
    """

    if not require_login():
        return redirect(url_for("login"))
    return redirect(url_for("play"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Authentication endpoint.

    GET:
        Render login form.

    POST:
        Validate credentials using auth_utils.
        On success → store username in session.
        On failure → re-render with error message.
    """

    error = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        ok, msg = verify_user(username, password)
        if ok:
            session["user"] = username
            return redirect(url_for("play"))
        error = msg

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/play", methods=["GET"])
def play():
    """
    Display a new flashcard question.

    Flow:
    - Ensure authentication
    - Rebuild game from saved state
    - If deck empty → redirect to finish
    - Pick random card
    - Store current card ID in session
    - Render question template
    """

    if not require_login():
        return redirect(url_for("login"))

    username = session["user"]
    game = build_game_for_user(username)

    # if deck finished -> finish page
    if game.is_deck_empty():
        return redirect(url_for("finish"))

    game.pick_random_card()
    session["current_card_id"] = game.current_card.id
    q = game.question_view()

    # NOTE: image_path in your JSON is like: "img/xxx.jpg"
    image_url = url_for("static", filename=q["image_path"])

    return render_template(
        "question.html",
        card_id=q["card_id"],
        image_url=image_url,
        remaining_count=len(game.remaining_cards),
        learned_count=game.learned_count,
    )


@app.route("/review", methods=["POST"])
def review():
    """
    Process submitted answers and show comparison screen.

    Steps:
    - Restore game state
    - Restore current card from session
    - Compare user answers with correct answers
    - Render review page

    Note:
    No state is persisted at this stage.
    """

    if not require_login():
        return redirect(url_for("login"))

    username = session["user"]
    game = build_game_for_user(username)

    # Must have a current card; simplest: re-pick a new card if none.
    # Better: store current card id in session. We'll do that now:
    current_card_id = session.get("current_card_id")
    if not current_card_id or not game.set_current_card_by_id(current_card_id):
        # fallback: pick new and set
        game.pick_random_card()
        session["current_card_id"] = game.current_card.id

    user_breed = request.form.get("breed", "")
    user_coat = request.form.get("coat_type", "")
    user_groom = request.form.get("grooming", "")

    r = game.review_view(
        user_ans_breed=user_breed,
        user_ans_coat_type=user_coat,
        user_ans_grooming=user_groom,
    )

    image_url = url_for("static", filename=game.current_card.image)

    return render_template(
        "review.html",
        card_id=game.current_card.id,
        image_url=image_url,
        correct_answers=r["correct_answers"],
        user_answers=r["user_answers"],
        all_correct=r["all_correct"],
    )


@app.route("/result", methods=["POST"])
def result():
    """
    Apply final round decision and persist updated game state.

    Steps:
    - Restore game state
    - Apply user decision (correct / remove card)
    - Update statistics
    - Save new state to disk
    - Clear current card from session
    - Render result summary
    """

    if not require_login():
        return redirect(url_for("login"))

    username = session["user"]
    game = build_game_for_user(username)

    current_card_id = session.get("current_card_id")
    if not current_card_id or not game.set_current_card_by_id(current_card_id):
        return redirect(url_for("play"))

    # checkboxes: if checked -> present
    is_correct = request.form.get("is_correct") == "1"
    remove_from_deck = request.form.get("remove_from_deck") == "1"
    remain_card = not remove_from_deck

    res = game.get_result_view(is_correct=is_correct, remain_card=remain_card)

    # Save state after applying turn
    save_state(username, game.export_state())

    # Clean current card from session (optional)
    session.pop("current_card_id", None)

    return render_template(
        "result.html",
        total_seen=res["total_seen"],
        total_correct=res["total_correct"],
        total_wrong=res["total_wrong"],
        remaining_count=res["remaining_count"],
        learned_count=res["learned_count"],
        current_card_seen=res["current_card_seen"],
        current_card_correct=res["current_card_correct"],
        current_card_wrong=res["current_card_wrong"],
        is_deck_empty=res["is_deck_empty"],
    )


@app.route("/finish")
def finish():
    """
    End-of-session summary page.

    Displays current statistics without modifying state.
    """

    if not require_login():
        return redirect(url_for("login"))

    username = session["user"]
    game = build_game_for_user(username)

    return render_template(
        "finish.html",
        remaining_count=len(game.remaining_cards),
        learned_count=game.learned_count,
        total_seen=game.total_seen,
        total_correct=game.total_correct,
        total_wrong=game.total_wrong,
    )

@app.route("/reset", methods=["POST"])
def reset():
    """
    Reset user progress.

    Actions:
    - Delete user's saved JSON state
    - Clear session-related game data
    - Redirect to new session start
    """

    if "user" not in session:
        return redirect(url_for("login"))

    username = session["user"]
    delete_state(username)

    session.pop("pending_review", None)
    session.pop("current_card_id", None)

    return redirect(url_for("play"))


if __name__ == "__main__":
    # Development server only.
    # In production, Passenger or WSGI server runs the app.
    app.run(debug=True)