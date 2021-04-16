from enum import Enum

class Moveresult(Enum):
    """Represents the result type of a player's move.
    """
    OK = "OK"
    KEY = "Key"
    EXIT = "Exit"
    EJECT = "Eject"
    INVALID = "Invalid"