"""This file holds the Occupant class and its descendants. Occupants are considered
to be anything that can occupy a tile; for example, a Level Key is an occupant.
"""
class Occupant:
    """Represents any entity that can occupy a Tile.
    """
    def __init__(self):
        pass

    def __eq__(self, other):
        return False

    def __hash__(self):
        return 1

class Entity(Occupant):
    """ Represents either a Character or an Adversary.
    """
    def __init__(self):
        pass

    def __eq__(self, other):
        return False

    def __hash__(self):
        return 3

class Character(Entity):
    """Represents a character controlled by a player.
    """
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash((self.name))
    
    def render(self) -> str:
        return 'P'

class Adversary(Entity):
    """Represents an enemy.
    """
    def __eq__(self, other):
        # TODO maybe fix the equality methods on Adversary/Zombie/Ghost
        return isinstance(other, Adversary)

    def __hash__(self):
        return 0

    def render(self):
        return 'A'

class Zombie(Adversary):
    zombie_count = 0
    """Represents a zombie.
    """
    def __init__(self, name = ""):
        self.name = name + str(Zombie.zombie_count)
        Zombie.zombie_count += 1

    def __eq__(self, other):
        return isinstance(other, Zombie) and self.name == other.name

    def __hash__(self):
        return hash(("zombie", self.name))

    def render(self):
        return 'Z'

class Ghost(Adversary):
    ghost_count = 0
    """Represents a ghost.
    """
    def __init__(self, name = ""):
        self.name = name + str(Ghost.ghost_count)
        Ghost.ghost_count += 1
    
    def __eq__(self, other):
        return isinstance(other, Ghost) and self.name == other.name

    def __hash__(self):
        return hash(("ghost", self.name))

    def render(self):
        return 'G'

class LevelKey(Occupant):
    """Represents the key to unlock a level exit.
    """
    def __eq__(self, other):
        pass

    def __hash__(self):
        pass

    def render(self):
        return 'K'

class LevelExit(Occupant):
    """Represents the exit for a level.
    """
    def __eq__(self, other):
        pass

    def __hash__(self):
        pass

    def render(self):
        return 'E'

class Door(Occupant):
    """Represents the exit for a level.
    """
    def __eq__(self, other):
        pass

    def __hash__(self):
        pass

    def render(self):
        return 'D'


class Block(Occupant):
    """Represents the exit for a level.
    """
    def __eq__(self, other):
        pass

    def __hash__(self):
        pass

    def render(self):
        return 'X'

class Wall(Block):
    """Represents the exit for a level.
    """
    def __eq__(self, other):
        pass

    def __hash__(self):
        pass

    def render(self):
        return '#'

class VerticalWall(Wall):
    def render(self):
        return '|'

class HorizontalWall(Wall):
    def render(self):
        return '-'