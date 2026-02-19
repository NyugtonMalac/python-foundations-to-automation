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

import logging
import os
import json

_BASE_DIR = None
ENCODING = "utf-8"

logger = logging.getLogger(__name__)

def set_base_dir(base_dir: str) -> None:
    """
    Set the base directory used for task storage.

    The application stores the to-do json file next to the main script. Since this
    module may live in a different folder, the entry point should call this
    function once at startup to configure path resolution.

    Args:
        base_dir: Absolute path to the directory where the json file should be created/read.
    """

    global _BASE_DIR
    _BASE_DIR = base_dir

def get_file_path(todo="to_do"):
    """
    Build the absolute file path for the task storage file.

    Args:
        todo: Base filename (without extension). The default creates/uses 'to_do.json'.

    Returns:
        Absolute path to the json file used for persistence.

    Raises:
        RuntimeError: If the base directory has not been set via `set_base_dir()`.
    """

    if _BASE_DIR is None:
        msg = "Base directory is not set. Call set_base_dir() from main."
        logger.error(msg)
        raise RuntimeError(msg)
    return os.path.join(_BASE_DIR, f"{todo}.json")

def add_task(task, todo="to_do"):
    """
    Add a new task to the JSON task list.

    Steps (read–modify–write):
    1) Load the existing list from JSON (or use [] if file doesn't exist yet)
    2) Append the new normalized task
    3) Write the full list back to the JSON file

    Args:
        task: Task text provided by the user.
        todo: Base filename (without extension) for the storage file.

    Raises:
        OSError: If the file cannot be written.
    """
    try:    
        new_task = task.strip().lower()
        if not new_task:
            logger.warning("Empty task, not added to the list.")
            return
        
        tasks = get_task_list(todo)
        tasks.append(new_task)

        path = get_file_path(todo)
        with open(path, "w", encoding=ENCODING) as file:
            json.dump(tasks, file, ensure_ascii=False, indent=2)
        logger.info("Task added: %s", new_task)
    except OSError:
        logger.exception('Failed to add task to "%s.json": %s', todo, task)
        raise

def get_task_list(todo="to_do"):
    """
    Read all tasks from the JSON storage file into a Python list.

    If the file does not exist yet, the function returns an empty list.
    If the file exists but is empty/corrupted or not a list, it also falls back
    to an empty list (and logs what happened).

    Returns:
        list[str]: list of task strings
    """

    path = get_file_path(todo)

    try:
        with open(path, "r", encoding=ENCODING) as file:
            data = json.load(file)

        if not isinstance(data, list):
            logger.error("Invalid JSON structure in %s: expected a list, got %s"
                         , path
                         , type(data).__name__)
            return []
        
        return data
        
    except FileNotFoundError:
        msg = f"As {todo}.json does not exist yet, your task list is currently empty."
        logger.warning(msg)
        return []
    
    except json.JSONDecodeError:
        logger.error("Could not decode JSON from %s (file is empty or invalid JSON)."
                     , path)
        return []
        
    except OSError:
        logger.exception("File error while reading tasks from %s.", path)
        raise


def view_tasks(todo="to_do"):
    """
    Print the current tasks to the terminal with 1-based numbering.

    Args:
        todo: Base filename (without extension) for the storage file.
    """
    current_tasks = get_task_list(todo)
    if not current_tasks:
        print("Your task list is currently empty.")
    else:
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

    target = task.strip().lower()
    
    if target not in current_tasks:
        logger.warning('No matching task found for: "%s".', task.strip())
        return
   
    removed_count = 0 
    for tsk in current_tasks:
        if  tsk != target:
            remaining_tasks.append(tsk)
        else:
            removed_count += 1

    path = get_file_path(todo)
    with open(path, "w", encoding=ENCODING)  as file:    
        json.dump(remaining_tasks, file, ensure_ascii=False, indent=2)

    logger.info("Removed %d occurrence(s) of task by name: %s",
                removed_count,
                target)
    if removed_count == 1:
        prt_msg = f'{removed_count} task'
    else:
        prt_msg = f'{removed_count} tasks'
    print(f'{prt_msg} removed: "{task.strip()}".')
        


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
    row_nr = len(current_tasks)
    
    if 1 <= task_id <= row_nr:
        removed_task = current_tasks.pop(task_id - 1)
        
        path = get_file_path(todo)
        with open(path, "w", encoding=ENCODING)  as file:    
            json.dump(current_tasks, file, ensure_ascii=False, indent=2)
                
        print(f'Task #{task_id} has been removed from the to_do list.')
        logger.info("Task removed by id: %s (%s)", task_id, removed_task)
    else:
        logger.warning('No matching task number found: %s', task_id)

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
            print(f"Please enter a number between 1 and {menu_length}.")
        except ValueError:
            print("Please enter a whole number.")

def waiting_for_user():
    """
    Pause the program until the user presses Enter.

    Used to let the user read output before the screen is cleared and the menu is shown again.
    """
    input("Press Enter to continue...")



