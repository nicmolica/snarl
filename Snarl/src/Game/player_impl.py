from .occupants import Character
from .player import Player
from .tile import Tile
from .moveresult import Moveresult
import sys
from .utils import grid_to_string
import json

class PlayerImpl(Player):
    def __init__(self, name : str, entity_name : str, out = sys.stdout, input_func = input):
        """ Initialize this Player with a name and a Character, aliased by a name. Initially,
        the player is not expelled and has no surroundings. These fields may be changed as
        the game progresses.
        """
        if not type(name) == str:
            raise TypeError("Player Name must be a string!")
        if not type(entity_name) == str:
            raise TypeError("Character Name must be a string!")
        self.name = name
        self.entity = Character(entity_name)
        self.expelled = False
        self.surroundings = None
        self.out = out
        self.input_func = input_func

    def __eq__(self, other):
        """ Is this Player equal to another Player?
        """
        if not isinstance(other, Player):
            return False
        return self.name == other.name and self.entity == other.entity

    def __hash__(self):
        """ Return a hash of the two identifying characteristics of a Player.
        """
        return hash((self.name, self.entity))

    def _determine_move(self):
        """Returns a player move given the input string representing the player
        input.
        """
        requested_input = self.input_func()
        # TODO: We probably don't want this command to be present in production but it's good for testing.
        if requested_input == 'q':
            self.out.write("Exiting game...")
            exit(0)
        input_json = json.loads(requested_input)
        if not type(input_json) == list or len(input_json) != 2:
            raise RuntimeError("User move input not valid: " + requested_input)
        x, y = input_json
        return Tile(x, y)

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