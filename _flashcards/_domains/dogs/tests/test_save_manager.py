"""
Smoke test for the save_manager persistence functions.

Run from repo root:
    python -m _flashcards._domains.dogs.tests.test_save_manager
"""

from __future__ import annotations

import tempfile

from _flashcards._core.save_manager import save_state, load_state, delete_state


def main() -> None:
    username = "TestUser_1"

    with tempfile.TemporaryDirectory() as tmp_saves_dir:
        delete_state(username, tmp_saves_dir)

        state = {
            "total_seen": 3,
            "total_correct": 2,
            "total_wrong": 1,
            "remaining_ids": ["dog_001", "dog_004"],
            "stats": {"dog_001": {"seen": 1, "correct": 1, "wrong": 0, "weight": 1}},
        }

        path = save_state(username, state, tmp_saves_dir)
        print("Saved to:", path)

        loaded = load_state(username, tmp_saves_dir)
        print("Loaded:", loaded)

        assert loaded == state, "Loaded state does not match saved state."

        assert delete_state(username, tmp_saves_dir) is True
        assert load_state(username, tmp_saves_dir) is None

    print("✅ test_save_manager OK")


if __name__ == "__main__":
    main()