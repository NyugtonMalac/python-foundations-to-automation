"""
Rock Paper Scissors - Loop and Input Validation Exercise

This script implements a two-player Rock-Paper-Scissors game
using while and for loops.

The program:
- Prompts the players to enter the number of rounds.
- Validates that the number is odd to ensure a decisive outcome.
- Re-prompts the user until a valid odd number is provided.
- Collects each player's move for every round, validating
  that the input is one of: "rock", "paper", or "scissors".
- Re-prompts in case of invalid input.
- Tracks and updates player scores after each round.
- Displays the final winner and the score difference.

This exercise focuses on loop control, input validation,
state tracking, and structured game logic design as part of the
"Python Foundations to Automation" learning path.
"""

print("\nHello,\n"
      "\nWelcome to the Rock-Paper-Scissors game.\n\n"
      "To ensure that the game has a clear winner, an odd number of rounds must be played.\n"
      "If both players choose the same move, the round is a tie and will be replayed.\n"
    )


while True:
    rounds_num = int(input('Please enter the number of rounds you would like to play: '))

    if rounds_num % 2:
        break

options = ["rock", "paper", "scissors"]

turn_num = 1

player_1_points = 0
player_2_points = 0

print('\nThank you.\n'
      f'There will be {rounds_num} rounds.\n'
      'Please choose only one of the following options: rock, paper, or scissors.\n')

wins = ["rock_paper", "paper_scissors", "scissors_rock"]


while turn_num <= rounds_num: 

    tie = False

    while True:
        player_1 = input('Player 1, please enter your move (rock / paper / scissors): ')
        player_1 = player_1.strip().lower()

        if player_1 in options:

            while True:
                player_2 = input('Player 2, please enter your move (rock / paper / scissors): ')
                player_2 = player_2.strip().lower()
                
                if player_2 in options:

                    if player_2 != player_1:
                        turn_num += 1
                    else:
                        print("It's a tie! The round will be replayed until a winner is determined.\n")
                        tie = True
                    break
        else:
            continue

        break


    player_2_checking = player_1 + "_" + player_2

    if not tie:
        if player_2_checking in wins:
            player_2_points += 1
        else:
            player_1_points += 1

        print(f"Player 1 chose: {player_1}, \nPlayer 2 chose: {player_2}\nPoint goes to: {'Player 2' if player_2_checking in wins else 'Player 1'}\n")

winner = "Player 2" if player_2_points > player_1_points else "Player 1"

print(f"\n\n>>>>>  And the winner is: {winner}.  <<<<<\n\nCongratulations!\nSee you next time!\n")




