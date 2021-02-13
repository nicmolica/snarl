"""This file holds the Occupant class and its descendants. Occupants are considered
to be anything that can occupy a tile; for example, a Level Key is an occupant.
"""
class Occupant:
    """Represents any entity that can occupy a Tile.
    """
    def render(self):
        return ' '

class Player(Occupant):
    """Represents a player.
    """
    def __eq__(self, other):
        pass 

    def __hash__(self, other):
        pass
    
    def render(self):
        return 'P'

class Adversary(Occupant):
    """Represents an enemy.
    """
    def __eq__(self, other):
        pass

    def __hash__(self, other):
        pass

    def render(self):
        return 'A'

class LevelKey(Occupant):
    """Represents the key to unlock a level exit.
    """
    def __eq__(self, other):
        pass

    def __hash__(self, other):
        pass

    def render(self):
        return 'K'

class LevelExit(Occupant):
    """Represents the exit for a level.
    """
    def __eq__(self, other):
        pass

    def __hash__(self, other):
        pass

    def render(self):
        return 'E'