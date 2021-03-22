from .occupants import Character
from .player import Player
from .tile import Tile
import sys
import json

class PlayerImpl(Player):
    def __init__(self, player_name : str, character_name : str):
        """ Initialize this Player with a name and a Character, aliased by a name. Initially,
        the player is not expelled and has no surroundings. These fields may be changed as
        the game progresses.
        """
        if not type(player_name) == str:
            raise TypeError("Player Name must be a string!")
        if not type(character_name) == str:
            raise TypeError("Character Name must be a string!")
        self.player_name = player_name
        self.character = Character(character_name)
        self.expelled = False
        self.surroundings = None

    def __eq__(self, other):
        """ Is this Player equal to another Player?
        """
        if not isinstance(other, Player):
            return False
        return self.player_name == other.player_name and self.character == other.character

    def __hash__(self):
        """ Return a hash of the two identifying characteristics of a Player.
        """
        return hash((self.player_name, self.character))

    def move(self):
        """Given the current state of their surroundings, get a move from this
        player and return the coordinates of the desired move.
        """
        sys.stdout.write("Please provide a move in the form [x, y]:\n")
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

    def update_surroundings(self, grid):
        """Send a new grid of surrounding tiles to this player.
        """
        self.surroundings = grid

    def expel(self):
        """Tell this player that they were expelled from the level.
        """
        self.expelled = True