"""This file holds utility methods. When adding functions to this file, please be very thorough
with the docstrings.
"""

def grid_to_string(grid: list) -> str:
    """Given a 2D list of characters, return a string of the characters in grid form.
    Taken from
    
    https://stackoverflow.com/questions/17870612/printing-a-two-dimensional-array-in-python.
    
    Arguments:
        grid (list[list[char]]): A two-dimensional list where each [x][y] represents
            the character at coordinates (x, y)
    
    Returns:
        grid_str (str): A string formatted to display the grid.
    """
    return '\n'.join([''.join(['{:4}'.format(character) for character in row]).rstrip() for row in grid])