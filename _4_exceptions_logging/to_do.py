"""
to_do.py

Command-line To-Do application.

This script is the entry point of the program. It initializes the application,
shows a menu-driven interface, and calls helper functions to perform operations
on a persistent task list stored in a text file.

Features:
- Add a task
- View tasks
- Remove a task (by name or by row number)
- Exit

Persistence:
Tasks are stored in a TXT file located next to this script.

Reliability:
File operations are expected to be wrapped in exception handling and important
events/errors should be logged to both console and a log file.

Note:
The TXT file should be committed to version control. Log files should be excluded
(e.g., using .gitignore).
"""


import sys
import os

# setting folder for helper files
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../_0_helpers'))) 

from terminal_clearer import clear_terminal
from setup_logger_v1 import setup_logger
from to_do_functions import (display_main_menu
                             , what_to_do_id
                             , add_task
                             , waiting_for_user
                             , set_base_dir
                             , view_tasks
                             , display_sub_menu
                             , remove_task_by_name
                             ,remove_task_by_id
)
# current folder for todo.txt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    set_base_dir(BASE_DIR)
    logger = setup_logger("to_do_app")
    clear_terminal()
    start = 0
    logger.info("Application started.")
    while start < 4:
        clear_terminal()
        start = what_to_do_id(display_main_menu())
        if start == 1:

            what_task = input("Please enter the task: ")
            add_task(task=what_task)
            print(f'Task: "{what_task}" has been added to the list.')
            logger.info("Task added: %s", what_task)
            waiting_for_user()
      
        elif start == 2:
            clear_terminal()
            print("Tasks in your To-Do list:")
            view_tasks()
            print()
            logger.info("User viewed the task list.")
            waiting_for_user()

        elif start == 3:
            clear_terminal()
            sub_start = what_to_do_id(display_sub_menu())
            if sub_start == 1:
                tsk_to_r = input("Please enter the task to be removed from the list: ")
                remove_task_by_name(tsk_to_r)
                logger.info('Task removed by name: %s', tsk_to_r.strip().lower())
                waiting_for_user()

            elif  sub_start == 2:
                tskid_to_r = int(input("Please enter the number of task to be removed: "))
                remove_task_by_id(tskid_to_r)
                logger.info("Task removed by id: %s", tskid_to_r)
                waiting_for_user()
        elif start == 4:
            clear_terminal()
            print("The program has finished.")
            logger.info('Application finished.')
            break
    


if __name__ == "__main__":
    main()