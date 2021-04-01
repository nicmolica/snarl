from .player import Player
from .tile import Tile
import sys
from .actor import Actor
from .utils import grid_to_string
import json

class Enemy(Actor):
    def __init__(self, enemy_name : str, entity_type, entity_name, out = None):
        """ Initialize this Player with a name and a Character, aliased by a name. Initially,
        the player is not expelled and has no surroundings. These fields may be changed as
        the game progresses.
        """
        if not type(enemy_name) == str:
            raise TypeError("Enemy Name must be a string!")
        self.enemy_name = enemy_name
        self.entity = entity_type(entity_name)
        self.expelled = False
        self.surroundings = None
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
        return self.enemy_name == other.enemy_name and self.entity == other.entity

    def __hash__(self):
        """ Return a hash of the two identifying characteristics of a Player.
        """
        return hash((self.enemy_name, self.entity))

    def render(self):
        """Renders the current surroundigns and other info to the output stream.
        """
        char_grid = map(lambda row : map(lambda tile : tile.render(), row), self.surroundings)
        if self.out:
            self.out.write(grid_to_string(char_grid))
        
    def expel(self):
        """Tell this enemy that they were expelled from the level.
        """
        self.expelled = True

    def get_entity(self):
        return self.entity