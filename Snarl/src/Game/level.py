import itertools
import random
from .room import Room
from .hallway import Hallway
from .occupants import Adversary, Character, Block, LevelKey, LevelExit, Occupant, Ghost, Door
from .tile import Tile

class Level:
    """Represents a SNARL Level.
    """
    def __init__(self, rooms: list, hallways: list, key_loc, exit_loc):
        """Creates the given level layout. Requires that no two rooms
        or hallways overlap and that all hallways connect two room doors.
        """
        if type(rooms) is not list or not all([type(r) is Room for r in rooms]):
            raise TypeError("Rooms must be a list of Room objects!")
        if type(hallways) is not list or not all([type(h) is Hallway for h in hallways]):
            raise TypeError("Hallways must be a list of Hallway objects!")

        self.rooms = rooms
        self.hallways = hallways
        self.is_completed = False
        self.characters = {}
        self.completed_characters = []
        self.adversaries = {}
        self.level_exit_unlocked = False

        if self._any_overlaps():
            raise ValueError("There are overlapping rooms or hallways in this level.")
        if not self._are_hallways_connected_to_doors():
            raise ValueError("There are disconnected hallways on this level.")

        self.key_location = key_loc
        self.exit_location = exit_loc
        self._update_tiles()
        if self.get_tile(key_loc).has_block() or self.get_tile(key_loc).has_occupant(Door):
            raise RuntimeError("Invalid key location. Cannot place a key on a block or a door.")
        if self.get_tile(exit_loc).has_block() or self.get_tile(exit_loc).has_occupant(Door):
            raise RuntimeError("Invalid exit location. Cannot place an exit on a block or a door.")
        if exit_loc == key_loc:
            raise RuntimeError("Cannot have the exit and the key located on the same tile.")

    def render(self) -> str:
        """Renders an ASCII representation of this level. Each coordinate in the level
        corresponds to a single ASCII character. Stores this grid of characters in self.rendered_tiles.

        Returns:
            rendered_tiles (list[list[character]]): A 2D list storing each character representing the level.
                Each element of the outer list contains a single row.
        """
        width, height = self.calculate_level_dimensions()
        rendered_tiles = [['X' for x in range(width)] for y in range(height)]
        # Render rooms
        for y in range(height):
            for x in range(width):
                rendered_tiles[y][x] = self.tiles[y][x].render()

        return rendered_tiles

    def get_tiles(self) -> list:
        """ Return the array of tiles.
        """
        return self.tiles.copy()

    def get_tiles_range(self, tile1: Tile, tile2: Tile) -> list:
        """ Return the rectangle of tiles between the specified tiles.
        """
        width, height = self.calculate_level_dimensions()
        min_x = max(min(tile1.x, tile2.x), 0)
        min_y = max(min(tile1.y, tile2.y), 0)
        max_x = min(max(tile1.x, tile2.x) + 1, width)
        max_y = min(max(tile1.y, tile2.y) + 1, height)
        return [row[min_x:max_x] for row in self.get_tiles()[min_y:max_y]]

    def calculate_level_dimensions(self):
        """Returns a tuple (width, height) of the level's dimensions, determined by
        the maximum coordinates needed by all of the level's rooms and hallways.
        """
        max_width = 0
        max_height = 0
        for room in self.rooms:
            room_max_x = room.position.x + room.width
            room_max_y = room.position.y + room.height
            if max_width < room_max_x:
                max_width = room_max_x
            if max_height < room_max_y:
                max_height = room_max_y

        for hall in self.hallways:
            for point in hall.waypoints:
                if max_width < point.x:
                    max_width = point.x
                if max_height < point.y:
                    max_height = point.y
        
        return max_width, max_height
    
    def locate_entity(self, occupant: Occupant) -> Tile:
        """ Locate the given occupant on the current level if it is a Character or Adversary.
        """
        if isinstance(occupant, Adversary):
            return self.adversaries[occupant]
        elif isinstance(occupant, Character):
            return self.characters[occupant]
        else:
            return None

    def move_occupant(self, occupant: Occupant, dest: Tile):
        """ Move the given occupant to the given destination if it is a Character or Adversary.
        """
        if isinstance(occupant, Adversary):
            self.get_tile(self.adversaries[occupant]).remove_occupant(occupant)
            self.get_tile(dest).occupants.append(occupant)
            self.adversaries[occupant] = self.get_tile(dest)
        elif isinstance(occupant, Character):
            self.get_tile(self.characters[occupant]).remove_occupant(occupant)
            self.get_tile(dest).occupants.append(occupant)
            self.characters[occupant] = self.get_tile(dest)
        else:
            raise RuntimeError("You can't move something that isn't a Character or an Adversary!")
        self.interact(self.get_tile(dest))

    def get_tile(self, tile: Tile) -> Tile:
        """ Given a tile, returns the actual Tile object in the grid associated with the same
        indices as the passed tile.
        """
        return self.tiles[tile.y][tile.x]

    def interact(self, dest: Tile):
        """Triggers any necessary interactions between the occupants of this tile. The interactions
        are as follows:
        1. Character + Key = unlock the level exit
        2. Character + Adversary = kill the player
        3. Character + Exit and level unlocked = complete the level
        """
        has_player = self.get_tile(dest).has_character()
        has_adv = self.get_tile(dest).has_adversary()
        has_ghost = self.get_tile(dest).has_occupant(Ghost)
        has_key = self.get_tile(dest).has_occupant(LevelKey)
        has_exit = self.get_tile(dest).has_occupant(LevelExit)
        has_block = self.get_tile(dest).has_block()
        
        characters = self._get_characters_on_tile(dest)
        if has_player and has_adv:
            for character in characters:
                self._remove_from_tile(character)
                self.characters.pop(character)
        elif has_player and has_key:
            self.unlocked_by = characters[0]
            self.unlock_level_exit()
        elif has_player and has_exit and self.level_exit_unlocked:
            for character in characters:
                self._remove_from_tile(character)
                self.completed_characters.append(character)
                self.characters.pop(character)

        if has_ghost and has_block:
            self._teleport_ghost(self.get_tile(dest).get_adversary())

    def _get_characters_on_tile(self, dest):
        """Gets any characters that are present on the tile.
        """
        return [occupant for occupant in self.get_tile(dest).occupants if isinstance(occupant, Character)]

    def _teleport_ghost(self, ghost):
        """ Teleport the ghost on the provided tile to a random tile in a random room.
        """
        room_tiles = list(map(lambda r: self._ghost_friendly_tiles(r), self.rooms))
        acceptable_rooms_tiles = list(filter(lambda r: r != [], room_tiles))
        chosen_room = random.choice(acceptable_rooms_tiles)
        chosen_tile = random.choice(chosen_room)
        self.move_occupant(ghost, chosen_tile)

    def random_spawn_tile(self):
        """Return a random tile onto which an Entity can be spawned.
        """
        room_tiles = list(map(lambda r: self._spawn_friendly_tiles(r), self.rooms))
        acceptable_rooms_tiles = list(filter(lambda r: r != [], room_tiles))
        chosen_room = random.choice(acceptable_rooms_tiles)
        chosen_tile = random.choice(chosen_room)
        return chosen_tile

    def _spawn_friendly_tiles(self, room):
        """Returns the tiles in a room on which an entity can be spawned.
        """
        friendly_tiles = []
        for t in room.get_open_tiles():
            tile = self.get_tile(t)
            if not tile.has_occupant(Adversary) and not tile.has_occupant(Block) and not \
                 tile.has_occupant(LevelKey) and not tile.has_occupant(LevelExit) and not \
                     tile.has_character() and not tile.has_occupant(Door):
                 friendly_tiles.append(t)

        return friendly_tiles

    def _ghost_friendly_tiles(self, room):
        """ Does the provided room have tiles that a ghost can land on?
        Empty tiles or tiles without a LevelKey or LevelExit. It's ok if a ghost lands
        on top of a character though.
        """
        friendly_tiles = []
        for t in room.get_open_tiles():
            tile = self.get_tile(t)
            if not tile.has_occupant(Adversary) and not tile.has_occupant(Block) and not \
                 tile.has_occupant(LevelKey) and not tile.has_occupant(LevelExit):
                 friendly_tiles.append(t)

        return friendly_tiles

    def _remove_from_tile(self, occ, tile = None):
        """Find the occupant and remove them from the tile grid.
        """
        loc = self.locate_entity(occ) if tile is None else tile
        self.get_tile(loc).remove_occupant(occ)

    def unlock_level_exit(self):
        """Unlocks the level exit tile.
        """
        self.level_exit_unlocked = True
        self._remove_from_tile(LevelKey(), self.key_location)

    def set_level_exit_status(self, status: bool):
        """Sets whether or not the level exit is unlocked.
        """
        if isinstance(status, bool):
            self.level_exit_unlocked = status
        else:
            raise TypeError("You can't set level exit status to something other than True or False")

    def add_character(self, character: Character, location: Tile):
        """ Add a player to this level at the specified location. Enforce
        uniqueness of player names.
        """
        if character in set(self.characters.keys()):
            raise ValueError("Cannot have duplicate characters!")
        self.characters[character] = self.get_tile(location)
        self.get_tile(location).add_occupant(character)

    def add_adversary(self, adversary: Adversary, location: Tile):
        """ Adds an adversary to this level at the specified location.
        """
        self.adversaries[adversary] = self.get_tile(location)
        self.get_tile(location).add_occupant(adversary)

    def get_top_left_room(self) -> Room:
        """ Get the top left room of this Level. Note that this function takes
        advantage of rich comparison provided by __lt__ on the Room class.
        """
        return sorted(self.rooms.copy())[0]

    def _any_overlaps(self) -> bool:
        """Do any two rooms/hallways overlap with each other? Uses 4 checks to verify this:
           - For all pairs of 2 rooms, do the rooms intersect? If yes for any, return true.
           - For all waypoints, is the waypoint inside of a room? If yes for any, return true.
           - For all consecutive pairs of waypoints, does the line between them intersect with
             a line made by another pair of consecutive waypoints? If yes for any, return true.
           - For all consecutive pairs of waypoints, does the segment they form intersect with
             a room? If yes for any, return true.
        """
        # 1st check:
        any_room_intersections = self._do_any_rooms_intersect()
        # 2nd check:
        any_hallways_inside_rooms = self._do_any_hallways_intersect_rooms()
        # 3rd check:
        any_hallways_intersect_hallways = self._do_any_hallways_intersect_hallways()
        # 4th check:
        does_hallway_straddle_room = self._does_any_hallway_straddle_room()

        return any_room_intersections or any_hallways_inside_rooms or \
            any_hallways_intersect_hallways or does_hallway_straddle_room
    
    def _do_any_rooms_intersect(self) -> bool:
        """Are there any two rooms in this level that share coordinates?
        """
        room_combos = itertools.combinations(self.rooms, 2)
        for (room1, room2) in room_combos:
            if room1 != room2 and room1.does_it_intersect(room2):
                return True
        return False
    
    def _do_any_hallways_intersect_rooms(self) -> bool:
        """Do any hallways have coordinates that are inside any room?
        For this, it suffices to check the hallway's waypoints.
        """
        waypoints = []
        for hall in self.hallways:
            waypoints.extend(hall.waypoints)
        for way in waypoints:
            for room in self.rooms:
                if room.contains(way):
                    return True
        return False

    def _do_any_hallways_intersect_hallways(self) -> bool:
        """Will any hallways intersect each other?
        """
        hall_combos = itertools.combinations(self.hallways, 2)
        for (hall1, hall2) in hall_combos:
            if hall1 != hall2 and hall1.does_it_intersect(hall2):
                return True
        return False

    def _does_any_hallway_straddle_room(self) -> bool:
        """ Does any pair of waypoints in the set of hallways straddle
        any one of the rooms?
        """
        waypoints = []
        for hall in self.hallways:
            waypoints.extend(hall.waypoints)
        for i in range(0, len(waypoints) - 1):
            for room in self.rooms:
                if room.is_straddled_by(waypoints[i], waypoints[i + 1]):
                    return True
        return False

    def _are_hallways_connected_to_doors(self) -> bool:
        """Do all hallways have their endpoints at room doors?
        """
        hall_ends = []
        for hall in self.hallways:
            hall_ends.append(hall.door1)
            hall_ends.append(hall.door2)
        
        room_doors = []
        for room in self.rooms:
            for door in room.get_room_doors():
                room_doors.append(door)

        return set(hall_ends).issubset(set(room_doors))

    def _update_tiles(self):
        """Updates the self.tiles field with the current tile information.
        """
        width, height = self.calculate_level_dimensions()
        self.tiles = [[Tile(x, y, Block()) for x in range(width)] for y in range(height)]
        self._update_rooms_tiles()
        self._update_hallways_tiles()
        key = self.locate_entity(LevelKey)
        if not key and self.key_location:
            self.tiles[self.key_location.y][self.key_location.x].add_occupant(LevelKey())
            self.tiles[self.exit_location.y][self.exit_location.x].add_occupant(LevelExit())

    def _update_hallways_tiles(self):
        """Alters self.tiles to contain the correct Tile information for all hallways in the level.
        """
        for hall in self.hallways:
            for i in range(0, len(hall.waypoints) - 1):
                this_w = hall.waypoints[i]
                next_w = hall.waypoints[i + 1]
                self._update_hallway_segment(this_w, next_w)

    def _update_hallway_segment(self, start, end):
        """Renders a single segment of the hallway, given the start and end coordinates.
        Does not require that start coordinates are less than end coordinates. Stores
        its result in self.rendered_tiles.

        Arguments:
            start (Tile): the position of the segment start.
            end (Tile): the position of the segment end.
        """
        self.tiles[start.y][start.x] = Tile(start.x, start.y)
        self.tiles[end.y][end.x] = Tile(end.x, end.y)
        y_min = min(start.y, end.y)
        y_max = max(start.y, end.y)
        x_min = min(start.x, end.x)
        x_max = max(start.x, end.x)
        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                self.tiles[y][x] = Tile(x, y)

    def _update_rooms_tiles(self):
        """Alters self.rendered_tiles to have room walls, objects, and doors in the coordinates
        specified by self.rooms.
        """
        for room in self.rooms:
            # Set the boundary rendered_tiles to a wall
            room_tiles = room.update_tiles()
            for x in range(room.position.x, room.position.x + room.width):
                for y in range(room.position.y, room.position.y + room.height):
                    self.tiles[y][x] = room_tiles[y - room.position.y][x - room.position.x]

    def _get_rooms_from_hallway(self, hallway):
        """Given a hallway, determine which rooms form the endpoint of the hallway.
        Returns the room origins as a 2-element list of 2-element lists representign coordinates.
        """
        room1 = None
        room2 = None
        for room in self.rooms:
            if room.contains(hallway.door1):
                room1 = room.position
            if room.contains(hallway.door2):
                room2 = room.position
        return [[room1.y, room1.x], [room2.y, room2.x]]

    def _get_rooms_from_tile_in_room(self, tile):
        """Gets the rooms that are connected by 1 hallway to the room containing the current tile.
        Assumes that the current tile is inside a room.
        """
        origin_room = None
        for room in self.rooms:
            if room.contains(tile):
                origin_room = room
        
        origin_room_coords = [origin_room.position.y, origin_room.position.x]

        doors = origin_room.get_room_doors()
        room_own_neighbor = False
        adjacent_halls = []
        # Find all hallways that are adjacent to the the origin room.
        # If the hallway has doors that both connect to the origin room,
        # then the origin room is its own neighbor.
        for hall in self.hallways:
            door1_in_room = False
            if any([hall.door1.coordinates_equal(door) for door in doors]):
                adjacent_halls.append(hall)
                door1_in_room = True
            door2_in_room = False
            if any([hall.door2.coordinates_equal(door) for door in doors]):
                adjacent_halls.append(hall)
                door2_in_room = True
            # Check that room is or is not its own neighbor
            if door1_in_room and door2_in_room:
                room_own_neighbor = True

        adjacent_rooms = []
        for hallway in adjacent_halls:
            adjacent_rooms.extend(self._get_rooms_from_hallway(hallway))

        unique_rooms = []
        [unique_rooms.append(x) for x in adjacent_rooms if x not in unique_rooms]
        # Must remove the room containing the tile, unless it is its own neighbor.
        if not room_own_neighbor:
            unique_rooms.remove(origin_room_coords)
        return unique_rooms
    
    def _tile_in_room_or_hallway(self, tile):
        """Given a level and a tile, check whether or not the tile is inside a room, hallway,
        or neither. Return "room", "hallway", or "void", respectively.
        """
        in_room = any([room.contains(tile) for room in self.rooms])
        in_hallway = any([hallway.contains(tile) for hallway in self.hallways])
        if in_room:
            return "room"
        elif in_hallway:
            return "hallway"
        else:
            return "void"

    def _get_rooms_from_tile_in_hallway(self, tile):
        """Given a tile in a hallway, return the origins of the rooms that the hallway connects.
        """
        hallway = None
        for hall in self.hallways:
            if hall.contains(tile):
                hallway = hall
    
        # Get the room origins from the doors
        return self._get_rooms_from_hallway(hallway)

    def get_reachable_rooms_from_tile(self, tile):
        """Get the origins of the rooms that are "immediately reachable" from the given tile.
        If the tile is in a room, it returns the origins of any rooms connected by a single
        hallway to the tile's room.
        If the tile is in a hallway, it returns the rooms at either end of the hallway.
        If the tile is not in a room and not in a hallway, return the empty array.
        """
        tile_type = self._tile_in_room_or_hallway(tile)
        if tile_type == "void":
            return []
        elif tile_type == "hallway":
            return self._get_rooms_from_tile_in_hallway(tile)
        else: #type is "room"
            return self._get_rooms_from_tile_in_room(tile)

    def get_level_key(self):
        """ Get the tile with the level key on it.
        """
        for row in self.tiles:
            for tile in row:
                if tile.has_occupant(LevelKey):
                    return tile
        
        return None

    def get_level_exit(self):
        """ Get the tile with the level exit on it.
        """
        for row in self.tiles:
            for tile in row:
                if tile.has_occupant(LevelExit):
                    return tile
        
        raise RuntimeError("No tile in this level has an exit on it.")

    def is_level_completed(self):
        """ Have all players either gotten to the exit or been ejected?
        """
        return not bool(self.characters)