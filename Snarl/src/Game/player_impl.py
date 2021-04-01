from .occupants import Character
from .player import Player
from .tile import Tile
from .moveresult import Moveresult
import sys
from .utils import grid_to_string
import json

class PlayerImpl(Player):
    def __init__(self, player_name : str, character_name : str, out = sys.stdout):
        """ Initialize this Player with a name and a Character, aliased by a name. Initially,
        the player is not expelled and has no surroundings. These fields may be changed as
        the game progresses.
        """
        if not type(player_name) == str:
            raise TypeError("Player Name must be a string!")
        if not type(character_name) == str:
            raise TypeError("Character Name must be a string!")
        self.player_name = player_name
        self.entity = Character(character_name)
        self.expelled = False
        self.surroundings = None
        self.out = out

    def __eq__(self, other):
        """ Is this Player equal to another Player?
        """
        if not isinstance(other, Player):
            return False
        return self.player_name == other.player_name and self.entity == other.entity

    def __hash__(self):
        """ Return a hash of the two identifying characteristics of a Player.
        """
        return hash((self.player_name, self.entity))

    def move(self):
        """Given the current state of their surroundings, get a move from this
        player and return the coordinates of the desired move.
        """
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

    def notify(self, arg):
        """Send a new grid of surrounding tiles to this player.
        """
        if type(arg) is not dict:
            raise RuntimeError("Player notification must be dictionary!")
        self.out.write(arg)
        if "layout" in arg:
            self.surroundings = arg["layout"]

    def render(self):
        """Renders the current surroundings and other info to the output stream.
        """
        char_grid = map(lambda row : map(lambda tile : tile.render(), row), self.surroundings)
        self.out.write(grid_to_string(char_grid))
        
    def expel(self):
        """Tell this player that they were expelled from the level.
        """
        self.expelled = True

    def get_entity(self):
        return self.entity