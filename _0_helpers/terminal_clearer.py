"""
terminal_clearer.py

Small utility module to clear the terminal screen in a cross-platform way
(Windows vs. macOS/Linux).

Used by the To-Do CLI app to keep the menu interface clean.
"""


import os

def clear_terminal():
    """
    Clear the terminal screen in a cross-platform way.

    Uses 'cls' on Windows and 'clear' on macOS/Linux.
    """
        
    if os.name == 'nt':  # windows
        os.system('cls')
    else:                # mac, linux
        os.system('clear')