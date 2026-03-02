"""
Data cleaning utilities for text normalization.

This module provides reusable helper functions for:
- Removing diacritical marks (accents) from Unicode strings
- Converting text into URL- and filename-safe slugs

These utilities are primarily used in the data preparation
pipeline (CSV → JSON conversion), especially for generating
web-safe image filenames.
"""

import unicodedata

def remove_accents(text: str) -> str:
    """
    Remove diacritical marks (accents) from a Unicode string.

    The function uses Unicode normalization (NFKD) to decompose
    accented characters into their base character and combining marks,
    then removes the combining marks.

    Args:
        text (str): Input string that may contain accented characters.

    Returns:
        str: Normalized string without diacritical marks.

    Example:
        --> remove_accents("Német boxer")
        'Nemet boxer'
    """
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(c for c in normalized if not unicodedata.combining(c))


def slugify(text: str, from_str:str = " ", to_str:str = "_") -> str:
    """
    Convert a string into a URL- and filename-safe slug.

    The transformation includes:
    - Removing accents
    - Converting to lowercase
    - Replacing a target substring (default: space) with another substring (default: hyphen)

    Note:
        This function performs minimal normalization. It does not yet
        remove special symbols or handle multiple consecutive spaces.
        It may be extended in the future.

    Args:
        text (str): Input string.

    Returns:
        str: Slugified string suitable for filenames or URLs.

    Example:
        --> slugify("Német boxer")
        'nemet-boxer'
    """
    text = remove_accents(text)
    text = text.lower()
    text = text.replace(from_str, to_str)
    return text