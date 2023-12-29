"""
This module contains all functions
and classes as tools.
"""

def open_file(path: str) -> str:
    """
    Open a file and returns its
    content
    """
    with open(path, 'r') as file:
        return file.read()