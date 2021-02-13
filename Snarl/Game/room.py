from tile import Tile

class Room:
    def __init__(self, position, width, height, room_doors, open_tiles = []):
        """Constructs a new room.

        Arguments:
            position (Tile): the position of the room's upper-left corner.
            width (int): the room's size on the x-axis. Must be positive.
            height (int): the room's size on the y-axis. Must be positive.
            room_doors (list[Tile]): A list of the doors on the boundary of the room.
            open_tiles (list[Tile]): A list of positions that contain traversable tiles.
                Coordinates are absolute.

        Returns:
            None
        """
        self.position = position
        self.width = width
        self.height = height
        self.room_doors = room_doors
        self.open_tiles = open_tiles
        if not self.is_valid():
            raise ValueError("Invalid room parameters")

    def __eq__(self, other):
        """ Overwrite == for Rooms to directly check equality.
        """
        return type(other) == Room and self.position == other.position and \
            self.width == other.width and \
                self.room_doors == other.room_doors

    def __hash__(self):
        """ Overwriting hash for Rooms because we overwrote ==.
        """
        return hash((self.position, self.width, self.height, self.room_doors))

    def is_valid(self):
        """Determine if the given parameters constitute a valid room.

        A room is invalid if the given exit_door location is not at the
        boundary dimensions of the room. 
        """
        return type(self.position) == Tile and \
            not self.room_doors == [] and self.are_dimensions_positive() and \
                self.are_doors_on_walls() or not all([type(d) is Tile for d in self.room_doors])

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
        """ Is the given Tile inside of this room?
        """
        return posn.x in range(self.position.x, self.position.x + self.width) and \
            posn.y in range(self.position.y, self.position.y + self.height)

    def render(self):
        """Renders this room as a 2D list of ASCII characters.
        """
        self.tiles =  [[' ' for y in range(self.height)] for x in range(self.width)]
        self.render_walls()
        self.render_doors()
        self.render_open_tiles()

        return self.tiles

    def render_doors(self):
        """Alters self.tiles to have appropriate characters for the doors.
        """
        for door in self.room_doors:
            self.tiles[door.x - self.position.x][door.y - self.position.y] = 'D'

    def render_open_tiles(self):
        for tile in self.open_tiles:
            self.tiles[tile.x - self.position.x][tile.y - self.position.y] = ' '

    def render_walls(self):
        """Alters self.tiles to have appropriate characters for this room's walls.
        """
        for x in range(self.width):
            for y in range(self.height):
                # This tile is a horizontal wall.
                if x == 0 or x == self.width - 1:
                    self.tiles[x][y] = '-'
                elif y == 0 or y == self.height - 1:
                    self.tiles[x][y] = '|'
                else:
                    self.tiles[x][y] = 'X'
