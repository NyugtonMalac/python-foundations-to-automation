"""
save_manager.py

Persistent storage layer for flashcard applications.

Responsibilities:
- Generate safe file paths for user save files
- Store game state as JSON
- Load previously saved state
- Delete (reset) saved progress

The storage location is provided by the caller (domain config),
so this module can be reused across multiple flashcard domains
(e.g. dogs, language).
"""

import os
import json
from typing import Optional, Dict, Any


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
    """
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
    cleaned = "".join(ch for ch in username if ch in allowed)
    return cleaned or "user"


def get_save_path(username: str, saves_dir: str) -> str:
    """
    Build the absolute save file path for a given user.

    Ensures the saves directory exists before returning the path.

    Args:
        username (str): The user's unique identifier.
        saves_dir (str): Absolute directory path where save files are stored.

    Returns:
        str: Absolute path to the user's save file.
    """
    os.makedirs(saves_dir, exist_ok=True)
    fname = _safe_filename(username) + ".json"
    return os.path.join(saves_dir, fname)


def save_state(username: str, state: Dict[str, Any], saves_dir: str) -> str:
    """
    Persist the current game state to disk.

    Args:
        username (str): The user's unique identifier.
        state (Dict[str, Any]): JSON-serializable game state dictionary.
        saves_dir (str): Directory where save files are stored.

    Returns:
        str: Absolute path of the saved file.
    """
    path = get_save_path(username, saves_dir)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4, ensure_ascii=False)
    return path


def load_state(username: str, saves_dir: str) -> Optional[Dict[str, Any]]:
    """
    Load a previously saved game state.

    Args:
        username (str): The user's unique identifier.
        saves_dir (str): Directory where save files are stored.

    Returns:
        dict if found, otherwise None.
    """
    path = get_save_path(username, saves_dir)
    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def delete_state(username: str, saves_dir: str) -> bool:
    """
    Delete a user's saved progress (reset functionality).

    Args:
        username (str): The user's unique identifier.
        saves_dir (str): Directory where save files are stored.

    Returns:
        True if a save file existed and was deleted, otherwise False.
    """
    path = get_save_path(username, saves_dir)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False