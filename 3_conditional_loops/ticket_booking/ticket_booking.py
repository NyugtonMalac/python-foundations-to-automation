"""
Ticket Booking - Seat Reservation Matrix Exercise

A terminal-based, simplified cinema ticket booking program.

The program:
- Displays a list of available movies and validates the user's selection.
- Shows a 5x5 seating layout represented as a list of lists.
- Lets the user book a chosen number of seats by entering row and seat numbers.
- Validates that each selected position is within range and not already reserved.
- Updates and reprints the seating layout after each successful reservation.
- Prints a final summary and marks reserved seats as purchased.

This exercise focuses on nested loops, list-of-lists manipulation,
input validation, basic state tracking, and modular design
(using helper functions in booking_utils.py) as part of the
"Python Foundations to Automation" learning path.
"""

from booking_utils import show_seating_map, select_movie, get_seats

movies = {
    1 : 'Twilight'
    , 2 : 'The Vampire Diaries'
    , 3 : 'Only Lovers Left Alive'
    , 4 : 'Underworld'
    , 5 : 'Interview with the Vampire'
    , 6 : 'Queen of the Damned'
    , 7 : 'Warm Bodies'
    , 8 : 'Let the Right One In'
    , 9 : 'Jennifer’s Body'
    , 10 : 'The Craft'
    }


auditorium = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 4, 4],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 4, 4, 0, 0]
]

print("\nHello!\n\n"
    "Welcome to the Ticket Booking Tool.\n\n"
    "\033[1;35mNow showing in theaters today: \033[0m" 
      )

for key, value in movies.items():
    print(f"    {key}. {value}")

print()


selected_movie_number = select_movie(movies)

print("\n\033[1mHere is the seating layout:\n\033[0m")
show_seating_map(auditorium)


while True:

    try:
        ticket_nums = int(input('\n\033[1mHow many tickets would you like to book? \033[0m'))
        break

    except ValueError:
        print('Please enter a whole number!')


print(f'\nYou have chosen to book {ticket_nums} tickets.')

booked_tickets = 1

booked_tickets =get_seats(auditorium, booked_tickets, ticket_nums)


print(f"\n\n\033[0;35mThank you."
    f"\nAll {booked_tickets-1} out of {ticket_nums} seats have been successfully reserved"
     f" for {movies[selected_movie_number]}: \033[0m\n")

for row_id, row in enumerate(auditorium):
    
    for seat_id, seat in enumerate(row):
        
        if seat == 2: 
            auditorium[row_id][seat_id] = 3


show_seating_map(auditorium)

print(f"\nWe look forward to seeing you again!\n")