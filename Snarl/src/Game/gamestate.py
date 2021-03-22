from .rulechecker import Rulechecker
from .level import Level
from .tile import Tile
from .room import Room
from .occupants import Entity, Character, Adversary

class Gamestate:
    def __init__(self, level: Level, num_of_players: int, num_of_adversaries: int):
        """ Creates a Gamestate with the given initial level and number of
        players and adversaries to create the game with.
        """
        self.levels = []
        self.levels.append(level)
        self.current_level = level
        self.rule_checker = Rulechecker()
        if num_of_players in range(1, 5):
            self.num_of_players = num_of_players
        else:
            raise ValueError("There must be 1-4 players.")

        if (num_of_adversaries < 0):
            raise ValueError("Cannot pass a negative quantity of adversaries!")

        self.num_of_adversaries = num_of_adversaries

    def move(self, entity: Entity, dest: Tile):
        """ Move the player/adversary to the new location.
        """
        self.current_level.move_occupant(entity, dest)

    def complete_level(self, are_we_done: bool):
        """ After a level has been completed, mark it as completed, generate
        the next level, and move all the players up to the next level.
        """
        # mark current level as complete
        self.current_level.is_completed = True

        # TODO generate next level (if not are_we_done)-this will happen when we have level gen
        # TODO move all players to next level

    def get_tiles(self) -> list:
        """ Return the full array of tiles in the current level.
        """
        return self.current_level.get_tiles()
        
    def get_tiles_range(self, tile1: Tile, tile2: Tile) -> list:
        """ Return the array of tiles between the two provided tiles in the current level.
        """
        return self.current_level.get_tiles_range(tile1, tile2)
    
    def get_character_surroundings(self, character: Character, radius: int) -> list:
        """Return a square of the tiles around the given player in the given radius.
        """
        loc = self.current_level.locate_occupant(character)
        level_width, level_height = self.current_level.calculate_level_dimensions()
        minx = max(0, loc.x - radius)
        maxx = min(level_width, loc.x + radius)
        miny = max(0, loc.y - radius)
        maxy = min(level_height, loc.y + radius)
        return self.get_tiles_range(Tile(minx, miny), Tile(maxx, maxy))

    def add_character(self, character: Character, location: Tile):
        """ Add a character to the current Level.
        """
        self.current_level.add_character(character, location)

    def add_adversary(self, adversary: Adversary, location: Tile):
        """ Add a character to the current Level.
        """
        self.current_level.add_adversary(adversary, location)

    def get_top_left_room(self) -> Room:
        """ Get the top left room of the current Level.
        """
        return self.current_level.get_top_left_room()

    def render(self) -> str:
        """ Renders the current level.
        """
        return self.current_level.render()