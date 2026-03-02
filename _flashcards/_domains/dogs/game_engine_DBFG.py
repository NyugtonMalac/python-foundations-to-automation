"""
Dog Grooming Flashcard – Core Game Engine

This module contains the complete business logic of the
Dog Grooming Flashcard learning system.

Responsibilities
----------------
- Card loading from JSON
- Weighted random card selection
- Answer normalization & comparison
- Statistics tracking
- Learning progression handling
- State export/import for persistence

Architecture Role
-----------------
This module is framework-agnostic:
- Used by CLI interface
- Used by Flask web interface
- Independent from authentication
- Independent from persistence implementation

Layer Position
--------------
Data (JSON)
    ↓
Game Engine (this module)
    ↓
Interface Layer (CLI / Flask)

Design Principles
-----------------
- No UI logic
- No file saving logic
- No session handling
- Pure domain behavior

All persistence is handled externally
(save_manager.py).
"""

import json
import random


ENCODING = "utf-8-sig"   # Handles UTF-8 with BOM


################ DogCards ################

class DogCard:

    """
    Represents a single flashcard.

    Attributes:
        id (str): Unique identifier
        breed (str): Dog breed
        coat_type (str): Coat type description
        grooming (str): Grooming method description
        image (str): Relative image path
        image_name (str): Extracted filename from path
    """

    def __init__(self, id, breed, coat_type, grooming, image):
        
        self.id = id
        self.breed = breed
        self.coat_type = coat_type
        self.grooming = grooming
        self.image = image
        self.image_name = image.split("/")[-1]
        self.cards_by_id = {}

    def __repr__(self):
        return f"DogCard(id={self.id}, breed={self.breed})"
    
    def __str__(self):
        return f">>>{self.id}<<<"


############# Flashcard Game #############

class FlashcardGame:
    
    """
    Core domain engine of the flashcard system.

    Handles:
    - Deck management
    - Card selection with adaptive weighting
    - Answer evaluation
    - Statistics aggregation
    - Learning progression tracking
    - State serialization for persistence

    Internal State:
    - dogcards: All loaded cards
    - remaining_cards: Cards still in learning deck
    - stats: Per-card statistics dictionary
    - current_card: Currently active card
    - total_seen / total_correct / total_wrong
    - learned_count

    This class contains no UI or persistence logic.
    """

    def __init__(self):
        self.dogcards = []
        self.remaining_cards = []
        self.stats = {}
        self.current_card = None
        self.total_seen = 0
        self.total_correct = 0
        self.total_wrong = 0
        self.learned_count = 0
  
    def load_cards(self, json_path: str) -> None:
        """
        Load flashcards from a JSON file.

        Args:
            file_name (str): Base name of JSON file (without extension)

        Effects:
            - Populates dogcards list
            - Initializes statistics structure
            - Resets remaining_cards to full deck
            - Builds cards_by_id lookup table
        """
        
        
        with open(json_path, "r", encoding=ENCODING) as file:
            raw_data = json.load(file)

        for d in raw_data:
            card = DogCard(
                id = d["id"],
                breed = d["breed"],
                coat_type = d["coat_type"],
                grooming = d["grooming"],
                image = d["image"]
            )
            self.dogcards.append(card)   

        self.cards_by_id = {card.id: card for card in self.dogcards}
        self.remaining_cards = self.dogcards.copy()

        for card in self.dogcards:
            self.stats[card.id] = { 
                "seen" : 0,
                "correct" : 0,
                "wrong" : 0,
                "weight" : 1
                }
            
    def update_weight(self, card_id, is_correct):
        """
        Update adaptive weight for a card.

        Strategy:
            - If correct → decrease weight (min 1)
            - If incorrect → increase weight significantly

        Purpose:
            Recently incorrect cards appear more frequently.
        """

        if is_correct:
            weight = max(1, self.stats[card_id]["weight"] - 10)     
        else: 
            weight= 80

        self.stats[card_id]["weight"] = weight

    def pick_random_card(self):
        """
        Select a card using weighted random choice.

        The probability of selection depends on the
        adaptive weight stored in self.stats.
        """

        weights = [self.stats[card.id]["weight"] for card in self.remaining_cards]
        selected = random.choices(self.remaining_cards, weights=weights, k=1)[0]

        self.current_card = selected

    def _get_current_card_base_data(self):
         return {
            "card_id" : self.current_card.id,
            "image_path" : self.current_card.image
            }

    def _get_current_card_good_answers(self):
        return {
            "breed": self._normalize(self.current_card.breed),
            "coat_type": self._normalize(self.current_card.coat_type),
            "grooming": self._normalize(self.current_card.grooming)
        }

    def _get_user_answers(self, user_ans_breed, user_ans_coat_type, user_ans_grooming):
        return {
            "breed": self._normalize(user_ans_breed),
            "coat_type": self._normalize(user_ans_coat_type),
            "grooming": self._normalize(user_ans_grooming)
        }

    def _normalize(self, text):
        if not text:
            return ""
        return str(text).strip().lower()

    def question_view(self):
        return self._get_current_card_base_data()

    def review_view(self, user_ans_breed, user_ans_coat_type, user_ans_grooming):
        """
        Compare user answers with correct answers.

        Returns:
            dict containing:
                - normalized correct answers
                - normalized user answers
                - all_correct (bool)

        Note:
            Does not modify game state.
        """
        
        good_answers = self._get_current_card_good_answers()
        user_answers = self._get_user_answers(user_ans_breed, user_ans_coat_type, user_ans_grooming)
        
        matches = {
            "breed" : user_answers["breed"] == good_answers["breed"],
            "coat_type" : user_answers["coat_type"] == good_answers["coat_type"],
            "grooming" : user_answers["grooming"] == good_answers["grooming"]
        }

        all_correct = all(matches.values())

        return {
            "correct_answers" : good_answers,
            "user_answers" : user_answers,
            "all_correct" : all_correct
        }
    
    def get_result_view(self, is_correct, remain_card):
        """
        Finalize a learning round.

        Args:
            is_correct (bool): User-evaluated correctness
            remain_card (bool): Whether card stays in deck

        Effects:
            - Updates global statistics
            - Updates per-card statistics
            - Adjusts adaptive weight
            - Removes card from deck if learned

        Returns:
            Aggregated statistics snapshot for UI.
        """

        self._evaluate_turn(is_correct=is_correct, remain_card=remain_card)


        return {
            "total_seen" : self.total_seen,
            "total_wrong" : self.total_wrong,
            "total_correct" : self.total_correct,
            "remaining_count": len(self.remaining_cards),
            "learned_count" : self.learned_count,
            "current_card_seen": self.stats[self.current_card.id]["seen"],
            "current_card_wrong": self.stats[self.current_card.id]["wrong"],
            "current_card_correct": self.stats[self.current_card.id]["correct"],
            "is_deck_empty" : self.is_deck_empty()
        }
        
    def is_deck_empty(self):
        return not self.remaining_cards

    def is_finished(self):
        """ 
        Generate a farewell message based on learning progress.

        Returns:
            Formatted summary string.
        """


        if not self.remaining_cards:
            well_done = "Gratulálok, mindent megtanultál!\n" 
        elif self.learned_count >= 10:
            well_done = "Nagyon ügyes voltál!\n" 
        elif self.learned_count >= 5:
            well_done = "Ügyes voltál!"
        else:
            well_done = ""


        farewell_msg = ("Köszönöm, hogy velem tanultál!\n"
                        "A tanulás során elért statisztikád:\n"
                        f"Megnézett kártyák száma: {self.total_seen}\n"
                        f"Ebből megtanult kártyák száma: {self.learned_count}\n"
                        f"Helyes válaszok száma: {self.total_correct}\n"
                        f"Rossz válaszok száma: {self.total_wrong}\n"
                        f"{well_done}"
                        )
        return farewell_msg

    def get_game_stats(self):
        return {
            "total_seen": self.total_seen,
            "total_correct": self.total_correct,
            "total_wrong": self.total_wrong,
            "remaining": len(self.remaining_cards)
        }

    def _evaluate_turn(self, is_correct, remain_card):
        self.total_seen += 1
        self.stats[self.current_card.id]["seen"] += 1
        
        if is_correct:
            self.total_correct += 1
            self.stats[self.current_card.id]["correct"] += 1
            self.update_weight(self.current_card.id, is_correct)
        else:
            self.total_wrong += 1
            self.stats[self.current_card.id]["wrong"] += 1
            self.update_weight(self.current_card.id, is_correct)
            

        if not remain_card:
            self.remaining_cards.remove(self.current_card)
        self.learned_count = len(self.dogcards) - len(self.remaining_cards)

################## for the web app ##################

    def export_state(self) -> dict:
        """Serialize current game state into a JSON-compatible dictionary.

        Used by:
            save_manager.py
        """

        return {
            "remaining_ids": [c.id for c in self.remaining_cards],
            "stats": self.stats,
            "total_seen": self.total_seen,
            "total_correct": self.total_correct,
            "total_wrong": self.total_wrong,
            "learned_count": self.learned_count,
        }

    def apply_state(self, state: dict) -> None:
        """
        Restore engine state from a previously exported snapshot.

        Args:
            state (dict): Saved game state

        Used by:
            Web application persistence layer.
        """
        
        if not state:
            return

        remaining_ids = set(state.get("remaining_ids", []))
        if remaining_ids:
            self.remaining_cards = [c for c in self.dogcards if c.id in remaining_ids]

        saved_stats = state.get("stats")
        if isinstance(saved_stats, dict):
            self.stats = saved_stats

        self.total_seen = int(state.get("total_seen", 0))
        self.total_correct = int(state.get("total_correct", 0))
        self.total_wrong = int(state.get("total_wrong", 0))
        self.learned_count = int(state.get("learned_count", 0))

    def set_current_card_by_id(self, card_id: str) -> bool:
        """
        Restore current_card based on ID.

        Returns:
            True if card found in remaining deck,
            otherwise False.
        """
        for c in self.remaining_cards:
            if c.id == card_id:
                self.current_card = c
                return True
        return False
