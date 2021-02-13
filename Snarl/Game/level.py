import itertools
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

    def any_overlaps(self):
        """Do any two rooms/hallways overlap with each other?
        """
        # 3 checks:
        # - For all pairs of 2 rooms, do the rooms intersect?
        # - For all waypoints, is the waypoint inside of a room?
        # - For all consecutive pairs of waypoints, does the line between them
        #   intersect with a line made by another pair of consecutive waypoints?

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

class Posn:
    """Represents an x-y position in a natural-valued 2D Cartesian grid.
    """
    def __init__(self, x, y):
        """Construct a new Posn with the given x-y coordinates.

        Arguments:
            x (int): the x-coordinate of the position.
            y (int): the y-coordiante of the position.
        
        Returns:
            None
        """
        if type(x) is int and type(y) is int:
            if x < 0 or y < 0:
                raise ValueError("Coordinates must be nonnegative!")

            self.x = x
            self.y = y
        else:
            raise TypeError("Position coordinates must be integers!")

    def __eq__(self, other):
        return type(other) == Posn and self.x == other.x and self.y == other.y

class Occupant:
    """Represents any entity that can occupy a Tile.
    """
    pass

class Player(Occupant):
    """Represents a player.
    """
    def __eq__(self, other):
        pass 

class Adversary(Occupant):
    """Represents an enemy.
    """
    def __eq__(self, other):
        pass

class LevelKey(Occupant):
    """Represents the key to unlock a level exit.
    """
    def __eq__(self, other):
        pass

class LevelExit(Occupant):
    """Represents the exit for a level.
    """
    def __eq__(self, other):
        pass

class Tile:   
    def __init__(self, occupant=None):
        """Constructs a new tile, possibly with an occupant.

        Arguments:
            occupant (Occupant): (optional) the occupant of the tile.
        
        Returns:
            None
        """
        if occupant:
            if type(occupant) is Occupant:
                self.occupant = occupant
            else:
                raise TypeError("Occupant of a tile must be an Occupant object!")
        else:
            self.occupant = None

class Space:
    """This class represents an enclosed space. It currently is only responsible
    for rendering that space.
    """
    pass

class Room(Space):
    def __init__(self, position, width, height, occupants, room_doors):
        """Constructs a new room.

        Arguments:
            position (Posn): the position of the room's upper-left corner.
            width (int): the room's size on the x-axis. Must be positive.
            height (int): the room's size on the y-axis. Must be positive.
            room_doors (list[Posn]): A list of the doors on the boundary of the room.
            open_tiles (list[list[Tiles]]): A 2D list of non-wall Tiles. Any
                empty indices are assumed to be walls.

        Returns:
            None
        """
        self.position = position
        self.width = width
        self.height = height
        self.occupants = occupants
        self.room_doors = room_doors
        if not self.is_valid():
            raise ValueError("Invalid room parameters")

    def __eq__(self, other):
        return type(other) == Room and self.position == other.position and \
            self.width == other.width and self.occupants == other.occupants and \
                self.room_doors == other.room_doors

    def is_valid(self):
        """Determine if the given parameters constitute a valid room.

        A room is invalid if the given exit_door location is not at the
        boundary dimensions of the room. 
        """
        return type(self.occupants) == list and type(self.position) == Posn and \
            not self.room_doors == [] and self.are_dimensions_positive() and \
            self.are_doors_on_walls()
                

    def are_dimensions_positive(self):
        """Are the width and height positive?
        """
        return self.width > 0 and self.height > 0

    def are_doors_on_walls(self):
        """Are the doors of this room on the room's walls?
        """
        x_min = self.position.x
        x_max = self.position.x + self.width
        y_min = self.position.y
        y_max = self.position.y + self.height

        for door in self.room_doors:
            if door.x == x_min or door.x == x_max:
                return door.y in range(y_min, y_max + 1)
            elif door.y == y_min or door.y == y_max:
                return door.x in range(x_min, x_max + 1)
            else:
                return False

    def does_it_intersect(self, other):
        """ Does this room intersect with the other room?
        """
        x1_min, x1_max = self.position.x, self.position.x + self.width
        x2_min, x2_max = other.position.x, other.position.x + other.width
        y1_min, y1_max = self.position.y, self.position.y + self.height
        y2_min, y2_max = other.position.y, other.position.y + other.height

        xflag = set(range(x1_min, x1_max)).intersection(set(range(x2_min, x2_max))) != set()
        yflag = set(range(y1_min, y1_max)).intersection(set(range(y2_min, y2_max))) != set()
        return xflag and yflag
    
    def contains(self, posn):
        return posn.x in range(self.position.x, self.position.x + self.width) and \
            posn.y in range(self.position.y, self.position.y + self.height)

class Hallway(Space):
    """Represents a hallway that connects two rooms. Hallways are composed of
    vertical and horizontal segments.
    """
    def __init__(self, waypoints):
        """Create a new hallway that follows the given waypoints.

        Arguments:
            waypoints(list[Posn]): the list of corners in the hallway.

        Returns:
            None
        """ 
        if type(waypoints) is not list:
            raise TypeError("Waypoints must be a list!")
        if not all([type(waypoint) is Posn for waypoint in waypoints]):
            raise TypeError("Waypoints must be a list of Posns!")
        if len(waypoints) < 2:
            raise ValueError("Waypoints list must contain at least two endpoints!")
        if not self.are_waypoints_valid():
            raise ValueError("Waypoints must form a sequence of horizontal and vertical segments!")
        self.waypoints = waypoints
        self.generate_segments()

    def __eq__(self, other):
        return type(other) is Hallway and self.waypoints == other.waypoints

    def are_waypoints_valid(self):
        """Determines if the waypoints will form a series of horizontal and vertical
        segments. If not, returns False.
        """
        for i in range(0, len(self.waypoints) - 1):
            this_waypoint = self.waypoints[i]
            next_waypoint = self.waypoints[i + 1]
            if not self.do_waypoints_share_axis(this_waypoint, next_waypoint):
                return False

    def do_waypoints_share_axis(self, waypoint1, waypoint2):
        """Do the given waypoints have at least one axis that is equal?
        """
        return waypoint1.x == waypoint2.x or waypoint1.y == waypoint2.y

    def initialize_tiles_size(self):
        """Sets the tiles field to sufficient dimensions to hold all waypoint
        coordinates.
        """
        max_width = max([waypoint.x for waypoint in self.waypoints])
        max_height = max([waypoint.y for waypoint in self.waypoints])
        self.tiles = [[None for i in range(max_height + 1)] \
            for j in range(max_width + 1)]

    def generate_segments(self):
        """Use this Hallway's waypoints to specify the positions of its
        walls and traversable tiles. This will place True in every index
        of self.tiles that corresponds to an index where this hallway has
        a wall or tile.
        """
        # Make sure our tiles array is big enough to hold coordinates for
        # all of the spaces that this hallway is going to occupy.
        self.initialize_tiles_size()
        # skips the last waypoint, because there's nowhere else to go
        for i in range(0, len(self.waypoints) - 1):
            this_waypoint = self.waypoints[i]
            next_waypoint = self.waypoints[i + 1]

            least_x = min(this_waypoint.x, next_waypoint.x)
            most_x = max(this_waypoint.x, next_waypoint.x)
            least_y = min(this_waypoint.y, next_waypoint.y)
            most_y = max(this_waypoint.y, next_waypoint.y)

            for x in range(least_x, most_x + 1):
                for y in range(least_y, most_y + 1):
                    self.tiles[x][y] = True
    
    def does_it_intersect(self, other):
        for i in range(0, len(self.waypoints) - 1):
            this_w = self.waypoints[i]
            next_w = self.waypoints[i + 1]
            for j in range(0, len(other.waypoints) - 1):
                this_p = other.waypoints[j]
                next_p = other.waypoints[j + 1]
                if self.does_segment_intersect(this_w, next_w, this_p, next_p):
                    return True
        return False
    
    def does_segment_intersect(self, w1, w2, p1, p2):
        xflag = set(range(w1.x, w2.x)).intersection(set(range(p1.x, p2.x))) != set()
        yflag = set(range(w1.y, w2.y)).intersection(set(range(p1.y, p2.y))) != set()
        return xflag and yflag