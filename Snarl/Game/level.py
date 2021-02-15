import itertools
from room import Room
from hallway import Hallway

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

        if self.any_overlaps():
            raise ValueError("There are overlapping rooms or hallways in this level.")
        # if not self.are_hallways_connected_to_doors():
        #     raise ValueError("There are disconnected hallways on this level.")

    def any_overlaps(self):
        """Do any two rooms/hallways overlap with each other? Uses 3 checks to verify this:
           - For all pairs of 2 rooms, do the rooms intersect? If yes for any, return true.
           - For all waypoints, is the waypoint inside of a room? If yes for any, return true.
           - For all consecutive pairs of waypoints, does the line between them intersect with
             a line made by another pair of consecutive waypoints? If yes for any, return true.
        """
        # 1st check:
        room_combos = itertools.combinations(self.rooms, 2)
        for (room1, room2) in room_combos:
            if room1 != room2 and room1.does_it_intersect(room2):
                return True

        # 2nd check:
        waypoints = []
        for hall in self.hallways:
            waypoints.extend(hall.waypoints)
        for way in waypoints:
            for room in self.rooms:
                if room.contains(way):
                    return True

        # 3rd check:
        hall_combos = itertools.combinations(self.hallways, 2)
        for (hall1, hall2) in hall_combos:
            if hall1 != hall2 and hall1.does_it_intersect(hall2):
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

    def render(self):
        """Renders an ASCII representation of this level. Each coordinate in the level
        corresponds to a single ASCII character.
        """
        width, height = self.calculate_level_dimenions()
        self.tiles = [['X' for x in range(width)] for y in range(height)]
        # Render rooms
        self.set_rooms_tiles()
        self.set_hallways_tiles()

        return self.tiles

    def set_hallways_tiles(self):
        """Alters self.tiles to have walkable tiles in the coordinates where the hallways
        are.
        """
        for hall in self.hallways:
            for i in range(0, len(hall.waypoints) - 1):
                this_w = hall.waypoints[i]
                next_w = hall.waypoints[i + 1]
                self.render_hallway_segment(this_w, next_w)
    
    def render_hallway_segment(self, start, end):
        self.tiles[start.y][start.x] = ' '
        self.tiles[end.y][end.x] = ' '
        y_min = min(start.y, end.y)
        y_max = max(start.y, end.y)
        x_min = min(start.x, end.x)
        x_max = max(start.x, end.x)
        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                self.tiles[y][x] = ' '


    def set_rooms_tiles(self):
        """Alters self.tiles to have room walls, objects, and doors in the coordinates
        specified by self.rooms
        """
        for room in self.rooms:
            # Set the boundary tiles to a wall
            room_tiles = room.render()
            for x in range(room.position.x, room.position.x + room.width):
                for y in range(room.position.y, room.position.y + room.height):
                    self.tiles[y][x] = room_tiles[y - room.position.y][x - room.position.x]

    def calculate_level_dimenions(self):
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
    