"""
auth_utils.py

Authentication helpers for Flask apps using a simple JSON user store.

Design goal:
- Keep this module reusable across multiple apps/domains.
- Therefore: the user database file path is provided by the caller.

User database format (users.json):
{
  "username": {
    "password_hash": "pbkdf2:sha256:...",
    "expires_at": "YYYY-MM-DD"   # optional
  }
}
"""

import os
import json
from datetime import datetime
from typing import Tuple, Dict, Any
from werkzeug.security import check_password_hash


def load_users(users_file: str) -> Dict[str, Any]:
    """
    Load the user database JSON from a given path.

    Args:
        users_file: Absolute (or relative) path to users.json.

    Returns:
        dict: Parsed JSON content. If file does not exist, returns {}.

    Raises:
        json.JSONDecodeError: If the JSON is malformed.
    """
    if not users_file:
        return {}

    if not os.path.exists(users_file):
        return {}

    with open(users_file, "r", encoding="utf-8") as f:
        return json.load(f)


def verify_user(username: str, password: str, users_file: str) -> Tuple[bool, str]:
    """
    Verify user credentials against the JSON user store.

    Checks:
      1) username exists
      2) password matches the stored werkzeug password hash
      3) optional expiration date (expires_at)

    Args:
        username: Username entered on the login form.
        password: Plaintext password entered on the login form.
        users_file: Path to the JSON user database.

    Returns:
        (True, "") if authentication is successful
        (False, "HU error message") if authentication fails
    """
    users = load_users(users_file)

    if username not in users:
        return False, "Ismeretlen felhasználónév."

    user_data = users[username]

    # Password check
    if not check_password_hash(user_data.get("password_hash", ""), password):
        return False, "Hibás jelszó."

    # Expiration check (optional)
    expires_at = user_data.get("expires_at")
    if expires_at:
        try:
            expiry_date = datetime.strptime(expires_at, "%Y-%m-%d")
        except ValueError:
            # If bad format in file, treat as invalid access (safe default)
            return False, "A hozzáférés lejárt."
        if datetime.now() > expiry_date:
            return False, "A hozzáférés lejárt."

    return True, ""