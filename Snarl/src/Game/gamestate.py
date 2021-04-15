from .rulechecker import Rulechecker
from .level import Level
from .tile import Tile
from .room import Room
from .occupants import Entity, Character, Adversary, Block, LevelExit, LevelKey

class Gamestate:
    def __init__(self, start_level: Level, num_of_players: int, num_of_adversaries: int, levels = [], characters = []):
        """ Creates a Gamestate with the given initial level and number of
        players and adversaries to create the game with.
        """
        self.levels = levels
        self.current_level = start_level
        self.num_levels_completed = 0
        self.rule_checker = Rulechecker()
        self.characters = characters
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

    def next_level(self):
        """ After a level has been completed, mark it as completed, generate
        the next level, and move all the players to the next level.
        """
        self.current_level.is_completed = True
        self.num_levels_completed += 1
        self.current_level = self.levels.pop(0)

    def is_current_level_completed(self):
        """ Is the current level completed?
        """
        return self.current_level.is_level_completed()

    def get_tile(self, tile):
        """Returns the level's tile at the given tile's coordinates.
        """
        return self.current_level.get_tile(tile)

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
        tile1, tile2 = self.get_character_view_range(character, radius)
        real_tiles = self.get_tiles_range(tile1, tile2)
        loc = self.get_entity_location(character)
        level_width, level_height = self.current_level.calculate_level_dimensions()

        if loc.x - radius < 0:
            for row in real_tiles:
                row.insert(0, Tile(0, 0, [Block()]))
        if level_width - (loc.x + radius + 1) < 0:
            for row in real_tiles:
                row.append(Tile(0, 0, [Block()]))
        if loc.y - radius < 0:
            real_tiles.insert(0, [Tile(0, 0, [Block()]) for tile in range(2*radius + 1)])
        if level_height - (loc.y + radius +  1) < 0:
            real_tiles.append([Tile(0, 0, [Block()]) for tile in range(2*radius + 1)])

        return real_tiles

    def get_character_view_range(self, character: Character, radius: int):
        """ Get tiles on 2 corners of the rectangular view range of the character.
        """
        loc = self.current_level.locate_occupant(character)
        level_width, level_height = self.current_level.calculate_level_dimensions()
        minx = max(0, loc.x - radius)
        maxx = min(level_width, loc.x + radius)
        miny = max(0, loc.y - radius)
        maxy = min(level_height, loc.y + radius)
        return (Tile(minx, miny), Tile(maxx, maxy))

    def add_character(self, character: Character, location: Tile):
        """ Add a character to the current Level.
        """
        self.characters.append(character)
        self.current_level.add_character(character, location)

    def add_adversary(self, adversary: Adversary, location: Tile):
        """ Add a character to the current Level.
        """
        self.current_level.add_adversary(adversary, location)

    def get_top_left_room(self) -> Room:
        """ Get the top left room of the current Level.
        """
        return self.current_level.get_top_left_room()
    
    def get_random_spawn_tile(self):
        """Gets a random tile onto which an Entity can be spawned.
        """
        return self.current_level.random_spawn_tile()

    def all_players_expelled(self) -> bool:
        """ Have all the players been expelled?
        """
        current_players = list(self.current_level.characters)
        completed_players = self.current_level.completed_characters
        if len(current_players) == 0 and len(completed_players) == 0:
            return True
        return False

    def is_character_expelled(self, character : Character) -> bool:
        """Has the given character been expelled from the level?
        """
        if not isinstance(character, Character):
            return False
        current_players = list(self.current_level.characters)
        completed_characters = self.current_level.completed_characters
        if character not in current_players and character not in completed_characters:
            return True
        return False

    def game_complete(self):
        """Does this gamestate represent a completed game of Snarl?
        """
        return self.current_level.is_completed and len(self.levels) == 0
    
    def is_current_level_unlocked(self):
        """Has the current level's exit been unlocked?
        """
        return self.current_level.level_exit_unlocked

    def get_current_characters(self):
        """Gets the characters playing the current level.
        """
        return list(self.current_level.characters)

    def get_completed_characters(self):
        """Returns a list of the characters taht have completed the current level.
        """
        completed = self.current_level.completed_characters
        return  completed if completed is not None else []
    
    def get_entity_location(self, occupant):
        """Return the coordinates of the current occupant.
        """
        return self.current_level.locate_occupant(occupant)

    def render(self) -> str:
        """ Renders the current level.
        """
        return self.current_level.render()

    def objects_in_range(self, t1: Tile, t2: Tile) -> list:
        """ Returns all the objects in the range between the two provided tiles.
        """
        objects = []
        tile_list = self.current_level.get_tiles_range(t1, t2)
        for row in tile_list:
            for tile in row:
                if tile.has_occupant(LevelKey):
                    objects.append((tile, LevelKey()))
                elif tile.has_occupant(LevelExit):
                    objects.append((tile, LevelExit()))
        return objects

    def actors_in_range(self, t1: Tile, t2: Tile) -> list:
        """ Returns all the actors in the range between the two provided tiles.
        """
        actors = []
        tile_list = self.current_level.get_tiles_range(t1, t2)
        for row in tile_list:
            for tile in row:
                for occ in tile.occupants:
                    if isinstance(occ, Entity):
                        actors.append((tile, occ))
        return actors
    
    def get_level_unlocked_by(self):
        """Return the character who unlocked the current level, or None if the level
        is not unlocked.
        """
        if self.current_level.level_exit_unlocked:
            return self.current_level.unlocked_by