from .player import Player
from .tile import Tile
import sys
from .actor import Actor
from .utils import grid_to_string
import json

class Enemy(Actor):
    def __init__(self, enemy_name : str, entity_type, entity_name):
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
        # TODO: This should be a constructor arg; we aren't writing it for now because testing
        # self.out = sys.stdout
        self.out = None

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

    def move(self):
        """Given the current state of their surroundings, get a move from this
        player and return the coordinates of the desired move.
        """
        if self.out:
            self.out.write("Please provide a move in the form [x, y]:\n")
        return self._move_with_input(input)

    def _move_with_input(self, input_func):
        """Returns a player move given the input string representing the player
        input.
        """
        requested_input = input_func()
        input_json = json.loads(requested_input)
        if not type(input_json) == list or len(input_json) != 2:
            raise RuntimeError("User move input not valid: " + requested_input)
        x, y = input_json
        return Tile(x, y)

    def notify(self, grid):
        """Send a new grid of surrounding tiles to this player.
        """
        self.surroundings = grid
        self.render()

    def render(self):
        """Renders the current surroundigns and other info to the output stream.
        """
        char_grid = map(lambda row : map(lambda tile : tile.render(), row), self.surroundings)
        if self.out:
            self.out.write(grid_to_string(char_grid))
        
    def expel(self):
        """Tell this player that they were expelled from the level.
        """
        self.expelled = True

    def notify_error(self, error_message):
        """Notify this player of an error.
        """
        self.last_error = error_message 
        self.out.write(self.last_error)

    def get_entity(self):
        return self.entity