from .player import AbstractPlayer
from .tile import Tile
import sys
from .actor import Actor
from .utils import grid_to_string
from .rulechecker import Rulechecker
import json

class Enemy(Actor):
    """Represents basic behavior for a SNARL enemy, including information about the entity
    that it plays in the game.
    """
    def __init__(self, name : str, entity_type, entity_name, out = None):
        """ Initialize this Player with a name and a Character, aliased by a name. Initially,
        the player is not expelled and has no surroundings. These fields may be changed as
        the game progresses.
        """
        if not type(name) == str:
            raise TypeError("Enemy Name must be a string!")
        self.name = name
        self.entity = entity_type(entity_name)
        self.expelled = False
        self.state = None
        self.location = None
        self.out = out
    
    def notify(self, arg):
        """Updates this enemy with a notification of the form
        { "state" : GameState, "loc": Tile }
        """
        if type(arg) is not dict:
            raise RuntimeError("Adversary notification must be dictionary!")
        if "state" in arg:
            self.state = arg["state"]
        if "loc" in arg:
            self.location = arg["loc"]

    def __eq__(self, other):
        """ Is this Enemy equal to another Enemy?
        """
        if not isinstance(other, Enemy):
            return False
        return self.name == other.name and self.entity == other.entity

    def __hash__(self):
        """ Return a hash of the two identifying characteristics of a Player.
        """
        return hash((self.name, self.entity))

    def render(self):
        """Renders the current surroundigns and other info to the output stream.
        """
        char_grid = map(lambda row : map(lambda tile : tile.render(), row), self.state.get_tiles())
        if self.out:
            self.out.write(grid_to_string(char_grid))
        
    def expel(self):
        """Tell this enemy that they were expelled from the level.
        """
        self.expelled = True

    def get_entity(self):
        return self.entity

    def _get_valid_cardinal_moves(self):
        """Return the possible cardinal moves for this enemy.
        """
        # If any coordinate is 0, can't move in that axis's negative direction.
        up = Tile(self.location.x, self.location.y + 1)
        right = Tile(self.location.x + 1, self.location.y)
        cardinals = [up, right]
        if (self.location.x > 0):
            left = Tile(self.location.x - 1, self.location.y)
            cardinals.append(left)
        if (self.location.y > 0):
            down = Tile(self.location.x, self.location.y - 1)
            cardinals.append(down)
        
        valid = lambda t : Rulechecker().is_valid_move(self.entity, t, self.state.current_level)
        valid_moves = list(filter(valid, cardinals))
        if valid_moves == []:
            return None
        return valid_moves