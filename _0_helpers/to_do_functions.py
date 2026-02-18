"""
to_do_functions.py

Helper functions for a command-line To-Do application.

This module contains:
- file path resolution based on a base directory provided by the main script
- CRUD-like operations on tasks stored in a plain text file
- menu printing and validated user input helpers

Design note:
The base directory is set once by calling `set_base_dir()` from the program's
entry point (to_do.py). This keeps file path handling predictable and testable.
"""

import os

_BASE_DIR = None
ENCODING = "utf-8"

def set_base_dir(base_dir: str) -> None:
    """
    Set the base directory used for task storage.

    The application stores the to-do TXT file next to the main script. Since this
    module may live in a different folder, the entry point should call this
    function once at startup to configure path resolution.

    Args:
        base_dir: Absolute path to the directory where the TXT file should be created/read.
    """

    global _BASE_DIR
    _BASE_DIR = base_dir

def get_file_path(todo="to_do"):
    """
    Build the absolute file path for the task storage file.

    Args:
        todo: Base filename (without extension). The default creates/uses 'to_do.txt'.

    Returns:
        Absolute path to the TXT file used for persistence.

    Raises:
        RuntimeError: If the base directory has not been set via `set_base_dir()`.
    """

    if _BASE_DIR is None:
        raise RuntimeError("Base directory is not set. Call set_base_dir() from main.")
    return os.path.join(_BASE_DIR, f"{todo}.txt")

def add_task(task, todo="to_do"):
    """
    Append a new task to the task storage file.

    The task text is normalized (trimmed and lowercased) before storing.

    Args:
        task: The task text provided by the user.
        todo: Base filename (without extension) for the storage file.

    Notes:
        File I/O errors should be handled with try/except and logged (assignment requirement).
    """
        
    path = get_file_path(todo)
    with open(path, "a", encoding=ENCODING) as file:
        file.write(f"{task.strip().lower()}\n")

def get_task_list(todo="to_do"):
    """
    Read all tasks from the storage file into a list.

    Args:
        todo: Base filename (without extension) for the storage file.

    Returns:
        A list of task strings (normalized without trailing newlines).

    Notes:
        If the file is missing/empty, the function should return an empty list
        (once you add exception handling).
    """

    tasks = []
    path = get_file_path(todo)
    with open(path, "r", encoding=ENCODING) as file:
        lines = file.readlines()
        for line in lines:
            tasks.append(line.strip())
    return tasks


def view_tasks(todo="to_do"):
    """
    Print the current tasks to the terminal with 1-based numbering.

    Args:
        todo: Base filename (without extension) for the storage file.
    """
    current_tasks = get_task_list(todo)
    for task_id, task in enumerate(current_tasks, 1):
        print(f"{task_id}. {task.strip().capitalize()}")

def remove_task_by_name(task, todo="to_do"):
    """
    Remove all tasks that exactly match the given task name.

    The comparison is performed after normalizing the input task (trim + lowercase).
    If multiple identical tasks exist, all matching entries will be removed.

    Args:
        task: The task text to remove.
        todo: Base filename (without extension) for the storage file.

    Notes:
        The current implementation rewrites the entire file after filtering tasks.
    """
    current_tasks = get_task_list(todo)
    remaining_tasks = []
    
    for tsk in current_tasks:
        if  tsk != task.strip().lower():
            remaining_tasks.append(tsk)
    
    path = get_file_path(todo)
    with open(path, "w", encoding=ENCODING)  as file:    
        for tsk in remaining_tasks:
            file.write(f"{tsk}\n")

    print(f'Task(s): "{task}" has been removed from the to_do list.')


def remove_task_by_id(task_id, todo="to_do"):
    """
    Remove a single task by its 1-based row number.

    Args:
        task_id: 1-based index as displayed by `view_tasks()`.
        todo: Base filename (without extension) for the storage file.

    Notes:
        You should validate that `task_id` is within range before rewriting the file.
    """
    current_tasks = get_task_list(todo)
    remaining_tasks = []
    
    for tsk_id, tsk in enumerate(current_tasks, 1):
        if  tsk_id != task_id:
            remaining_tasks.append(tsk)
    
    path = get_file_path(todo)
    with open(path, "w", encoding=ENCODING)  as file:    
        for tsk in remaining_tasks:
            file.write(f"{tsk}\n")
            
    print(f'Task nr{task_id} has been removed from the to_do list.')

def display_main_menu():
    """
    Print the main menu options and return the number of options.

    Returns:
        The count of menu items (used for validating user input).
    """

    print("Welcome to the To-Do List Manager. \nPlease choose one of the options below:")
    menu_main = {
        1 : "Add Task",
        2 : "View Tasks",
        3 : "Remove Task",
        4 : "Exit"
    }

    for k,v in menu_main.items():
        print(f"{k}. {v}")
    return len(menu_main)

def display_sub_menu():
    """
    Print the task removal submenu options and return the number of options.

    Returns:
        The count of submenu items (used for validating user input).
    """

    print("Please choose one of the options below:")
    menu_sub = {
        1 : "Delete a task by name",
        2 : "Delete a task by its row number"
    }

    for k,v in menu_sub.items():
        print(f"{k}. {v}")
    return len(menu_sub)

def what_to_do_id(menu_length):
    """
    Prompt the user for a menu choice and validate it.

    The function keeps asking until the user enters an integer within the allowed range.

    Args:
        menu_length: The maximum valid option number (inclusive).

    Returns:
        A valid integer choice in the range [1, menu_length].
    """

    while True:
        try: 
            resp = int(input("Please select a task by its number: "))
            if resp in range(1, menu_length + 1):
                return resp
            print(f"Please enter a number between 1 and {menu_length}!")
        except ValueError:
            print("Please enter a whole number.")

def waiting_for_user():
    """
    Pause the program until the user presses Enter.

    Used to let the user read output before the screen is cleared and the menu is shown again.
    """
    input("Press Enter to continue...")



