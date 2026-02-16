"""
booking_utils.py

Helper functions for the Ticket Booking exercise.

This module contains reusable functions used by the main
ticket_booking.py script, including:
- printing a color-coded seating map,
- validating user input for movie selection and seat coordinates,
- collecting seat reservations and updating the seating matrix.

The functions are intentionally kept simple and terminal-focused,
as this project is part of the "Python Foundations to Automation"
learning path and emphasizes clean control flow and input validation.
"""

def show_seating_map(auditorium):

    """
     Display the current seating layout in a formatted, color-coded view.

    Each seat is represented by a numeric status code:
    - 0 → Available
    - 2 → Selected (temporarily reserved)
    - 3 → Bought (finalized reservation)
    - any other value → Booked

    Parameters:
        auditorium (list of lists): 2D matrix representing the seating layout.
    """

    for row_id, row in enumerate(auditorium, 1):
        print(f"Row {row_id}: ", end="    ")
        for seat_id, seat in enumerate(row, 1):
            if seat == 0:
                print(f"Seat {seat_id}-\033[32m Available\033[0m", end="  ")
            elif seat == 2:
                print(f"Seat {seat_id} -\033[36m Selected \033[0m", end="  ")
            elif seat == 3:
                print(f"Seat {seat_id} -\033[34m Bought \033[0m", end="  ")   
            else:
                print(f"Seat {seat_id} -\033[31m Booked \033[0m", end="  ")
        print()

def select_movie(movies):

    """ 
    Prompt the user to select a movie from the provided dictionary.

    Repeatedly asks for input until a valid movie number is entered.
    Handles non-integer input using exception handling.

    Parameters:
        movies (dict): Dictionary mapping numeric keys to movie titles.

    Returns:
        int: The selected movie number.
    """

    while True:
        while True:
            try:
                film_req = int(input("\033[1mPlease select the movie you would like to watch by entering its number: \033[0m"))
                break
            except ValueError:
                print('Please enter only one number from the list!')
        
        if film_req in movies:
            print(f'\n\033[1;35mThank you! Selected movie is "{movies[film_req]}".\033[0m')
            return film_req
            
        else:
            print("Please try to choose a number from the list, thank you for your understanding.")

def get_position_input(position_name):

    """ 
    Request and validate a numeric seat coordinate (row or seat).

    Ensures that:
    - the input is an integer,
    - the value is within the allowed range (1-5).

    Parameters:
        position_name (str): Label used in the input prompt ("row" or "seat").

    Returns:
        int: A validated position number between 1 and 5.
    """

    while True:
        try:
            value = int(input(f'Which {position_name} would you like to book? '))
            if value not in [1,2,3,4,5]:
                print(f"Please enter a valid {position_name} number (1 to 5).")
                continue
            return value
        except ValueError:
            print("Please enter a whole number from 1 to 5. Thank you.")

def get_seats(auditorium, booked_tickets, ticket_nums):

    """ 
    Collect and process seat reservations from the user.

    For each requested ticket:
    - Prompts for row and seat number,
    - Validates that the seat is within range,
    - Checks whether the seat is available,
    - Updates the seating matrix if valid,
    - Reprints the updated seating layout.

    Parameters:
        auditorium (list of lists): 2D seating matrix.
        booked_tickets (int): Current booking counter (starting from 1).
        ticket_nums (int): Total number of tickets requested.

    Returns:
        int: Final number of processed bookings.
    """

    while booked_tickets <= ticket_nums:
        
        print(f"\n\033[1mPlease enter the details for seat number {booked_tickets}.\033[0m")
        
        row = get_position_input("row")
        seat = get_position_input("seat")

        if auditorium[row-1][seat-1] != 0:
            print("The selected seat is already reserved. Please choose another one.\n")
        else:
            booked_tickets += 1
            auditorium[row-1][seat-1] = 2
            print(f'\033[36mSeat {seat} in row {row} has been successfully reserved. \033[0m')
            show_seating_map(auditorium)
    return booked_tickets
