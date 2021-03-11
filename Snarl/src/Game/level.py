import itertools
from room import Room
from hallway import Hallway
from occupants import Adversary, Character, Block, LevelKey, LevelExit
from tile import Tile

class Level:
    def __init__(self, rooms, hallways):
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

        if self.any_overlaps():
            raise ValueError("There are overlapping rooms or hallways in this level.")
        if not self.are_hallways_connected_to_doors():
            raise ValueError("There are disconnected hallways on this level.")

        # This is done after we know that the room is valid.
        self.update_tiles()

    def any_overlaps(self):
        """Do any two rooms/hallways overlap with each other? Uses 4 checks to verify this:
           - For all pairs of 2 rooms, do the rooms intersect? If yes for any, return true.
           - For all waypoints, is the waypoint inside of a room? If yes for any, return true.
           - For all consecutive pairs of waypoints, does the line between them intersect with
             a line made by another pair of consecutive waypoints? If yes for any, return true.
           - For all consecutive pairs of waypoints, does the segment they form intersect with
             a room? If yes for any, return true.
        """
        # 1st check:
        any_room_intersections = self.do_any_rooms_intersect()
        # 2nd check:
        any_hallways_inside_rooms = self.do_any_hallways_intersect_rooms()
        # 3rd check:
        any_hallways_intersect_hallways = self.do_any_hallways_intersect_hallways()
        # 4th check:
        does_hallway_straddle_room = self.does_any_hallway_straddle_room()

        return any_room_intersections or any_hallways_inside_rooms or \
            any_hallways_intersect_hallways or does_hallway_straddle_room
    
    def do_any_rooms_intersect(self):
        """Are there any two rooms in this level that share coordinates?
        """
        room_combos = itertools.combinations(self.rooms, 2)
        for (room1, room2) in room_combos:
            if room1 != room2 and room1.does_it_intersect(room2):
                return True
        return False
    
    def do_any_hallways_intersect_rooms(self):
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
        # TODO deal with hallway segments that straddle rooms

    def do_any_hallways_intersect_hallways(self):
        """Will any hallways intersect each other?
        """
        hall_combos = itertools.combinations(self.hallways, 2)
        for (hall1, hall2) in hall_combos:
            if hall1 != hall2 and hall1.does_it_intersect(hall2):
                return True
        return False

    def does_any_hallway_straddle_room(self):
        """ Does any pair of waypoints in the set of hallways straddle
        any one of the rooms?
        """
        waypoints = []
        for hall in self.hallways:
            waypoints.extend(hall.waypoints)
        for i in range(0, len(waypoints) - 1):
            for room in self.rooms:
                if room.is_straddled_by(waypoints[i], waypoints[i + 1]):
                    print("waypoints: " + str(waypoints[i].x) + ", " + str(waypoints[i].y) + " to " + str(waypoints[i+1].x) + ", " + str(waypoints[i + 1].y))
                    print("room posn: " + str(room.position.x) + ", " + str(room.position.y))
                    return True
        return False

    def are_hallways_connected_to_doors(self):
        """Do all hallways have their endpoints at room doors?
        """
        hall_ends = []
        for hall in self.hallways:
            hall_ends.append(hall.door1)
            hall_ends.append(hall.door2)
        
        room_doors = []
        for room in self.rooms:
            for door in room.room_doors:
                room_doors.append(door)

        return set(hall_ends).issubset(set(room_doors))

    def update_tiles(self):
        """Updates the self.tiles field with the current tile information.
        """
        width, height = self.calculate_level_dimensions()
        self.tiles = [[Tile(x, y, Block()) for x in range(width)] for y in range(height)]
        self.update_rooms_tiles()
        self.update_hallways_tiles()

    def update_hallways_tiles(self):
        """Alters self.tiles to contain the correct Tile information for all hallways in the level.
        """
        for hall in self.hallways:
            for i in range(0, len(hall.waypoints) - 1):
                this_w = hall.waypoints[i]
                next_w = hall.waypoints[i + 1]
                self.update_hallway_segment(this_w, next_w)

    def update_hallway_segment(self, start, end):
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

    def update_rooms_tiles(self):
        """Alters self.rendered_tiles to have room walls, objects, and doors in the coordinates
        specified by self.rooms.
        """
        for room in self.rooms:
            # Set the boundary rendered_tiles to a wall
            room_tiles = room.update_tiles()
            for x in range(room.position.x, room.position.x + room.width):
                for y in range(room.position.y, room.position.y + room.height):
                    self.tiles[y][x] = room_tiles[y - room.position.y][x - room.position.x]

    def render(self):
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

    def render_vicinity(self):
        """Renders an ASCII representation of part of this level. Each coordinate in the level
        corresponds to a single ASCII character. Stores this grid of characters in self.rendered_tiles.

        Returns:
            rendered_tiles (list[list[character]]): A 2D list storing each character representing the level.
                Each element of the outer list contains a single row.
        """
        pass
        # TODO write this method

    def get_tiles(self):
        """ Return the array of tiles.
        """
        return self.tiles.copy()

    def get_tiles_range(self, tile1, tile2):
        """ Return the rectangle of tiles between the specified tiles.
        """
        min_x = min(tile1.x, tile2.x)
        min_y = min(tile1.y, tile2.y)
        max_x = max(tile1.x, tile2.x) + 1
        max_y = max(tile1.y, tile2.y) + 1
        # TODO test this method
        return [row[min_x:max_x] for row in self.tiles.copy()[min_y:max_y]]

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
    
    def locate_occupant(self, occupant):
        """ Locate the given occupant on the current level if it is a Character or Adversary.
        """
        if isinstance(occupant, Adversary):
            return self.adversaries[occupant]
        elif isinstance(occupant, Character):
            return self.characters[occupant]
        else:
            return None

    def move_occupant(self, occupant, dest):
        """ Move the given occupant to the given destination if it is a Character or Adversary.
        """
        if isinstance(occupant, Adversary):
            self.get_tile(self.adversaries[occupant]).occupants = []
            self.get_tile(dest).occupants.append(occupant)
            self.adversaries[occupant] = self.get_tile(dest)
        elif isinstance(occupant, Character):
            self.get_tile(self.characters[occupant]).occupants = []
            self.get_tile(dest).occupants.append(occupant)
            self.characters[occupant] = self.get_tile(dest)
        else:
            raise TypeError("You can't move something that isn't a Character or an Adversary!")
        self.interact(self.get_tile(dest))

    def get_tile(self, tile):
        """ Given a tile, returns the actual Tile object in the grid associated with the same
        indices as the passed tile.
        """
        return self.tiles[tile.y][tile.x]

    def interact(self, dest):
        """Triggers any necessary interactions between the occupants of this tile. The interactions
        are as follows:
        1. Character + Key = unlock the level exit
        2. Character + Adversary = kill the player
        3. Character + Exit and level unlocked = complete the level
        """
        types = [type(occupant) for occupant in self.get_tile(dest).occupants]
        has_player = Character in types
        has_adv = any([isinstance(occupant, Adversary) for occupant in self.get_tile(dest).occupants])
        has_key = LevelKey in types
        has_exit = LevelExit in types

        if has_player and has_adv:
            characters = [occupant for occupant in self.get_tile(dest).occupants if isinstance(occupant, Character)]
            for character in characters:
                self.characters.pop(character)
        elif has_player and has_key:
            self.unlock_level_exit()
        elif has_player and has_exit and self.level_exit_unlocked:
            # Happens twice because a character could have been killed before this happens
            characters = [occupant for occupant in self.get_tile(dest).occupants if isinstance(occupant, Character)]
            for character in characters:
                self.completed_characters.append(character)
                self.characters.pop(character)
        
    def unlock_level_exit(self):
        """Unlocks the level exit tile.
        """
        self.level_exit_unlocked = True

    def set_level_exit_status(self, status):
        """Locks the level exit tile.
        """
        if isinstance(status, bool):
            self.level_exit_unlocked = status
        else:
            raise TypeError("You can't set level exit status to something other than True or False")

    def add_character(self, player, location):
        """ Add a player to this level at the specified location. Enforce
        uniqueness of player names.
        """
        if player in set(self.characters.keys()):
            raise ValueError("Cannot have duplicate characters!")
        self.characters[player] = self.get_tile(location)
        self.get_tile(location).add_occupant(player)

    def add_adversary(self, adversary, location):
        """ Adds an adversary to this level at the specified location.
        """
        self.adversaries[adversary] = self.get_tile(location)
        self.get_tile(location).add_occupant(adversary)

    def get_top_left_room(self):
        """ Get the top left room of this Level. Note that this function takes
        advantage of rich comparison provided by __lt__ on the Room class.
        """
        return sorted(self.rooms.copy())[0]