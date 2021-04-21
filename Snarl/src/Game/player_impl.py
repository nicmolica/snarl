from .occupants import Character
from .player import AbstractPlayer
from .tile import Tile
from .moveresult import Moveresult
import sys
from .utils import grid_to_string
import json

class Player(AbstractPlayer):
    """Represents a player in the game of Snarl. Has several fields to keep track of important
    telemetry such as keys collected, name, and the entity that it is responsible for in the game
    itself.

    May optionally be given methods to input and output information. Defaults to sys.stdout and
    input.
    """
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
        self.keys_collected = 0
        self.successful_exits = 0
        self.times_ejected = 0

    def __eq__(self, other):
        """ Is this Player equal to another Player?
        """
        if not isinstance(other, AbstractPlayer):
            return False
        return self.name == other.name and self.entity == other.entity

    def __hash__(self):
        """ Return a hash of the two identifying characteristics of a Player.
        """
        return hash((self.name, self.entity))

    def copy(self):
        """Returns a Player object whose names and stats are a copy of this object.
        Does not preserve input, output.
        """
        new = Player(self.name, self.entity.name)
        new.keys_collected = self.keys_collected
        new.successful_exits = self.successful_exits
        new.times_ejected = self.times_ejected
        return new

    def _determine_move(self):
        """Returns a player move given the input string representing the player
        input.
        """
        self.out.write("move")
        requested_input = self.input_func()
        if requested_input == "skip":
            return None
        input_json = json.loads(requested_input)
        if input_json is None:
            return None
        if not type(input_json) == list or len(input_json) != 2:
            raise RuntimeError("User move input not valid: " + requested_input)
        y, x = input_json
        return Tile(x, y)

    def get_entity(self):
        return self.entity