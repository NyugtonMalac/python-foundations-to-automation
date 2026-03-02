"""
Smoke test for FlashcardGame export/apply_state + persistence integration.

Run from repo root:
    python -m _flashcards._domains.dogs.tests.test_game_state
"""

from __future__ import annotations

import tempfile

from _flashcards._core.save_manager import save_state, load_state
from _flashcards._domains.dogs.config import DOGS_JSON_PATH
from _flashcards._domains.dogs.game_engine_DBFG import FlashcardGame


def main() -> None:
    username = "TestUser_2"

    with tempfile.TemporaryDirectory() as tmp_saves_dir:
        g1 = FlashcardGame()
        g1.load_cards(json_path=DOGS_JSON_PATH)
        g1.pick_random_card()

        # szimulálunk egy kört:
        g1.get_result_view(is_correct=True, remain_card=True)

        state = g1.export_state()
        save_state(username, state, tmp_saves_dir)

        loaded = load_state(username, tmp_saves_dir)
        assert loaded is not None, "Expected saved state to be loadable."

        g2 = FlashcardGame()
        g2.load_cards(json_path=DOGS_JSON_PATH)
        g2.apply_state(loaded)

        assert g2.total_seen == g1.total_seen
        assert g2.total_correct == g1.total_correct
        assert g2.total_wrong == g1.total_wrong
        assert len(g2.remaining_cards) == len(g1.remaining_cards)

        print("OK? remaining:", len(g2.remaining_cards))
        print("total_seen:", g2.total_seen)

    print("✅ test_game_state OK")


if __name__ == "__main__":
    main()