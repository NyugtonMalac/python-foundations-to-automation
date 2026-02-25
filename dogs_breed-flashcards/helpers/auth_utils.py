import os
import json
from datetime import datetime
from werkzeug.security import check_password_hash


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_FILE = os.path.join(BASE_DIR, "data_private", "users.json")


def load_users():
    """
    Load the user database from `data_private/users.json`.

    The file is expected to contain a JSON object where keys are usernames and
    values are user records, e.g.:

        {
          "PomPom_Lili": {
            "password_hash": "...",
            "expires_at": "2026-12-31"
          }
        }

    Returns:
        dict: Parsed user data. If the file does not exist, returns an empty dict.

    Notes:
        - This function does not validate the schema beyond reading JSON.
        - If the JSON is malformed, `json.JSONDecodeError` will be raised.
    """
    if not os.path.exists(USERS_FILE):
        return {}

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def verify_user(username: str, password: str) -> tuple[bool, str]:
    """
    Verify a user's credentials against the local JSON user database.

    This is used by the Flask login route. It checks:
      1) username exists
      2) password matches the stored werkzeug password hash
      3) optional expiration date (`expires_at`)

    Args:
        username (str): The username entered on the login form.
        password (str): The plaintext password entered on the login form.

    Returns:
        tuple[bool, str]:
            - (True, "") if authentication is successful
            - (False, "error message") if authentication fails

    Possible error messages (HU):
        - "Ismeretlen felhasználónév."
        - "Hibás jelszó."
        - "A hozzáférés lejárt."
    """
    users = load_users()

    if username not in users:
        return False, "Ismeretlen felhasználónév."

    user_data = users[username]

    # jelszó ellenőrzés
    if not check_password_hash(user_data["password_hash"], password):
        return False, "Hibás jelszó."

    # lejárat ellenőrzés
    expires_at = user_data.get("expires_at")
    if expires_at:
        expiry_date = datetime.strptime(expires_at, "%Y-%m-%d")
        if datetime.now() > expiry_date:
            return False, "A hozzáférés lejárt."

    return True, ""