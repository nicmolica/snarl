class Occupant:
    """Represents any entity that can occupy a Tile.
    """
    pass

class Player(Occupant):
    """Represents a player.
    """
    def __eq__(self, other):
        pass 

class Adversary(Occupant):
    """Represents an enemy.
    """
    def __eq__(self, other):
        pass

class LevelKey(Occupant):
    """Represents the key to unlock a level exit.
    """
    def __eq__(self, other):
        pass

class LevelExit(Occupant):
    """Represents the exit for a level.
    """
    def __eq__(self, other):
        pass