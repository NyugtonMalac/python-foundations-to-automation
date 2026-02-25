"""
save_manager.py

Persistent storage layer for the Dog Grooming Flashcard application.

Responsibilities:
- Generate safe file paths for user save files
- Store game state as JSON
- Load previously saved state
- Delete (reset) saved progress

All save files are stored under:
    <project_root>/saves/<username>.json
"""

import os
import json
from typing import Optional, Dict, Any


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVES_DIR = os.path.join(BASE_DIR, "saves")


def _safe_filename(username: str) -> str:
    """
    Sanitize a username for safe filesystem usage.

    Keeps only alphanumeric characters, underscore and hyphen.
    This prevents path traversal and problematic filenames.

    Args:
        username (str): Raw username input.

    Returns:
        str: A filesystem-safe filename (without extension).
             Returns "user" if the cleaned result would be empty.

    Note:
        This is a lightweight sanitization, not a full security layer.
    """
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
    cleaned = "".join(ch for ch in username if ch in allowed)
    return cleaned or "user"


def get_save_path(username: str) -> str:
    """
    Build the absolute save file path for a given user.

    Ensures the `saves/` directory exists before returning the path.

    Args:
        username (str): The user's unique identifier.

    Returns:
        str: Absolute path to the user's save file.
    """
    os.makedirs(SAVES_DIR, exist_ok=True)
    fname = _safe_filename(username) + ".json"
    return os.path.join(SAVES_DIR, fname)


def save_state(username: str, state: Dict[str, Any]) -> str:
    """
    Persist the current game state to disk.

    The state is stored as a formatted JSON file for readability.

    Args:
        username (str): The user's unique identifier.
        state (Dict[str, Any]): Serializable game state dictionary.

    Returns:
        str: Absolute path of the saved file.

    Raises:
        TypeError: If `state` contains non-serializable objects.
        OSError: If writing to disk fails.
    """
    path = get_save_path(username)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4, ensure_ascii=False)
    return path


def load_state(username: str) -> Optional[Dict[str, Any]]:
    """
    Load a previously saved game state.

    Args:
        username (str): The user's unique identifier.

    Returns:
        Optional[Dict[str, Any]]:
            - Parsed state dictionary if the save file exists
            - None if no save file is found

    Raises:
        json.JSONDecodeError: If the save file is corrupted.
        OSError: If reading from disk fails.
    """
    path = get_save_path(username)
    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def delete_state(username: str) -> bool:
    """Delete a user's saved progress (reset functionality).

    Args:
        username (str): The user's unique identifier.

    Returns:
        bool:
            - True if a save file existed and was deleted
            - False if no save file was found
    """
    path = get_save_path(username)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False