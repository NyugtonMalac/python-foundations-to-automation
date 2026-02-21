"""
path_utils.py

Utility helpers for building absolute file paths for read/write/export tasks.

Why it exists:
- Your project files may live in multiple folders (apps + helpers).
- You often want to create output files next to the entry-point script.
- This module lets the entry point set a base directory once, then build
  absolute file paths reliably anywhere in the project.

############# please add the following rows to the main ap #############
import sys
import os

# setting folder for helper files
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                 '../_0_helpers'))
                                 ) 

from set_base_directory import set_base_dir

# setting current folder for file operation
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

##########################################################################


"""
import logging
import os


_BASE_DIR = None


logger = logging.getLogger(__name__)

def set_base_dir(base_dir: str) -> None:
    """
    Set the base directory used for file operations.

    Call this once from your main script (entry point), typically with:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        set_base_dir(BASE_DIR)

    Args:
        base_dir (str): Absolute path to the directory where files should be created/read.
    """

    global _BASE_DIR
    _BASE_DIR = base_dir


def get_file_path(file_name:str = "new_file", file_extension:str = ".json") -> str:
    """
    Build an absolute path for a file in the configured base directory.

    Args:
        file_name (str): File name without extension.
        file_extension (str): File extension (".json" or "json" both accepted).

    Returns:
        str: Absolute path like "/abs/path/new_file.json".

    Raises:
        RuntimeError: If base directory was not set via set_base_dir().
    """

    if _BASE_DIR is None:
        msg = "Base directory is not set. Call set_base_dir() from main."
        logger.error(msg)
        raise RuntimeError(msg)
    ext = file_extension.strip()
    fname = file_name.strip()
    if not ext.startswith("."):
        ext = "." + ext
    return os.path.join(_BASE_DIR, f"{fname}{ext}")
