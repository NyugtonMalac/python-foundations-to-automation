"""
Dog Grooming Flashcard - Command Line Interface (CLI)

This module provides a terminal-based interface for the
Dog Grooming Flashcard learning system.

Purpose
-------
- Offer a local, interactive learning experience
- Demonstrate separation between:
    • Game Engine (business logic)
    • CLI layer (presentation)
- Enable testing without web interface

Architecture
------------
FlashcardGame (engine)
    ↓
CLI interaction loop (this file)
    ↓
User input / terminal output

Key Characteristics
-------------------
- No persistence layer (state lives in memory)
- No authentication
- Pure engine-driven session
- Fully decoupled from Flask application

This module is intended for:
- Local development
- Engine debugging
- Educational demonstration
"""

from _flashcards._domains.dogs.config import DOGS_JSON_PATH
from _flashcards._cli_helpers.terminal_clearer import clear_terminal
from _flashcards._domains.dogs.game_engine_DBFG import FlashcardGame




def main():
    """
    Entry point for CLI gameplay.

    Flow:
    1. Initialize FlashcardGame engine
    2. Load card dataset (dogs.json)
    3. Loop until:
        - Deck is empty
        - User chooses to exit
    4. For each round:
        - Pick random card
        - Collect user answers
        - Show review comparison
        - Let user evaluate correctness
        - Update engine state
        - Display statistics

    Notes:
    - All game logic is handled by FlashcardGame.
    - This function only manages user interaction.
    """

    clear_terminal()
    dog_flashcard_game = FlashcardGame()
    dog_flashcard_game.load_cards(json_path=DOGS_JSON_PATH)

    print("Üdvözöllek a Kutya Grooming tanuló alkalmazásban!\n")

    user_exit = False

    # -----------------------------
    # Main gameplay loop
    # -----------------------------
    
    while not dog_flashcard_game.is_deck_empty() and not user_exit:
        clear_terminal()
        dog_flashcard_game.pick_random_card()
        
        question_variables = dog_flashcard_game.question_view()

        card_id = question_variables["card_id"]
        image_path = question_variables["image_path"]

        print(f"A kutya képe: {card_id} ({image_path})")

        user_ans_breed = input("Kérlek add meg a kutya fajtáját: ")
        user_ans_coat_type = input("Kérlek add meg a kutya szőrzetének típusát: ")
        user_ans_grooming = input("Kérlek add meg a kutya ápolásának módját: ")

        # Compare user input with engine answers

        review_result = dog_flashcard_game.review_view(user_ans_breed=user_ans_breed,
                                       user_ans_coat_type=user_ans_coat_type, 
                                       user_ans_grooming=user_ans_grooming)
        
        all_correct = review_result["all_correct"]
        
        if all_correct:
            ans_matches = "teljes mértékben megegyezett."
        else:
            ans_matches = "nem egyezett meg teljes mértékben."

        correct_ans_breed = review_result["correct_answers"]["breed"]
        correct_ans_coat_type = review_result["correct_answers"]["coat_type"]
        correct_ans_grooming = review_result["correct_answers"]["grooming"]

        user_ans_breed = review_result["user_answers"]["breed"]
        user_ans_coat_type = review_result["user_answers"]["coat_type"]
        user_ans_grooming = review_result["user_answers"]["grooming"]

        clear_terminal()

        print(
            f"A kutya képe: {card_id} ({image_path})\n\n"
            "A kutya adatlapja szerinti válaszok:\n"
            f"Kutya fajtája: {correct_ans_breed}\n"
            f"Szőrzete: {correct_ans_coat_type}\n"
            f"Ápolásának módja: {correct_ans_grooming}\n\n"
            "A te válaszaid:\n"
            f"Kutya fajtája: {user_ans_breed}\n"
            f"Szözete: {user_ans_coat_type}\n"
            f"Ápolűsűnak módja: {user_ans_grooming}\n\n"    
            f"A válaszaid a kártyán szereplő információkkal {ans_matches}\n"
            "Kérlek, értékeld a válaszaidat:"
        )

        # Apply user decision and update statistics

        user_ans_is_correct = input("Véleményed szerint helyesek voltak? (i/n): ")

        if user_ans_is_correct.strip().lower() == 'i':
            is_correct = True
        else:
            is_correct = False

        user_ans_remain_card = input("Köszönöm. Szeretnéd a kártyát a tanulópakliból kivenni? (i/n): ")
        if user_ans_remain_card.strip().lower() == 'i':
            remain_card = False
        else:
            remain_card = True

        results = dog_flashcard_game.get_result_view(is_correct=is_correct, remain_card=remain_card)

        total_seen = results["total_seen"]
        total_wrong = results["total_wrong"]
        total_correct = results["total_correct"]

        remaining_count = results["remaining_count"]
        learned_count = results["learned_count"]

        current_card_seen = results["current_card_seen"]
        current_card_correct = results["current_card_correct"]
        current_card_wrong = results["current_card_wrong"]

        if remain_card:
            ans_remain = "a tanuló pakliban marad."
        else:
            ans_remain = "bekerült a megtanult pakliba. :o)"

        clear_terminal()

        print(
            f"A kutya képe: {card_id} ({image_path})\n\n"
            f"Ezt a kártyát {current_card_seen} alkalommal láttad.\n" 
            f"Ebből {current_card_correct} alkalommal sikeresen, {current_card_wrong} alkalommal helytelenül válaszoltál.\n"
            f"\nEz a kártya {ans_remain}\n\n"
            "Tanulás előrehaladása:\n"
            f"Eddig {total_seen} kártyát láttál, {total_correct} helyes és {total_wrong} helytelen választ adtál.\n"
            f"A tanuló pakliban {remaining_count} és a megtanult pakliban {learned_count} kártya van."

        )

        user_exit_q = input("Ha szeretnéd befejezni a tanulást, nyomj egy i-t, vagy a  folytatáshoz egy entert: ")
        if user_exit_q.strip().lower() == "i":
            user_exit = True
        
    clear_terminal()
    print(dog_flashcard_game.is_finished())

if __name__ == "__main__":
    # Run CLI version of the application.
    # In production deployment, Flask web app is used instead.
    main()

