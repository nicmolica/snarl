from tile import Tile

class Room:
    """Represents a Room. Rooms are enclosed rectangles with a position in the
    grid, positive width and height, at least one room door on the room's boundary,
    and a list of non-wall tiles inside the room.
    """
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
        return isinstance(other, Room) and self.position == other.position and \
            self.width == other.width and \
                self.room_doors == other.room_doors

    def __hash__(self):
        """ Overwriting hash for Rooms because we overwrote ==.
        """
        return hash((self.position, self.width, self.height, self.room_doors))

    def is_valid(self):
        """Determine if the given parameters constitute a valid room.

        A room is invalid if the given exit_door location is not at the
        boundary dimensions of the room, if the room domensions are not positive,
        if there is no room door, or if the given room door is not a Tile.
        """
        room_has_door = self.room_doors != []
        room_doors_are_tiles = all([isinstance(d, Tile) for d in self.room_doors])
        return isinstance(self.position, Tile) and room_has_door and self.are_dimensions_positive() \
                and self.are_doors_on_walls() and room_doors_are_tiles and self.tiles_are_valid()

    def are_dimensions_positive(self):
        """Are the width and height positive?
        """
        return self.width > 0 and self.height > 0

    def tiles_are_valid(self):
        """Makes sure that all of the open tiles given in the open tile layout are actually valid.
        """
        # Should not allow open tiles on the boundary.
        x_min = self.position.x + 1
        x_max = self.position.x + self.width - 1
        y_min = self.position.y + 1
        y_max = self.position.y + self.height - 1

        for tile in self.open_tiles:
            if not isinstance(tile, Tile):
                return False
            if tile.x not in range(x_min, x_max):
                return False
            if tile.y not in range(y_min, y_max):
                return False

        return True

    def are_doors_on_walls(self):
        """Are the doors of this room on the room's walls?
        """
        x_min = self.position.x
        x_max = self.position.x + self.width - 1
        y_min = self.position.y
        y_max = self.position.y + self.height - 1

        for door in self.room_doors:
            if door.x == x_min or door.x == x_max:
                return door.y in range(y_min, y_max)
            elif door.y == y_min or door.y == y_max:
                return door.x in range(x_min, x_max)
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
    
    def contains(self, tile):
        """ Is the given Tile inside of this room?
        """
        return tile.x in range(self.position.x, self.position.x + self.width) and \
            tile.y in range(self.position.y, self.position.y + self.height)

    def render(self):
        """Renders this room as a 2D list of ASCII characters. Also stores the result
        in self.tiles.

        Returns:
            tiles (list[list[character]]): A 2D list of the strings representing this level's
                tiles. The list is referenced [y][x]-the entries of the outer list are each
                a single row of the room.
        """
        # Make sure the tiles array is the proper size; inits to empty strings
        self.tiles =  [[' ' for x in range(self.width + 1)] for y in range(self.height + 1)]
        self.render_walls()
        self.render_doors()
        self.render_open_tiles()

        return self.tiles

    def render_doors(self):
        """Alters self.tiles to contain appropriate characters for the doors.
        """

        for door in self.room_doors:
            relative_x = door.x - self.position.x
            relative_y = door.y - self.position.y
            self.tiles[relative_y][relative_x] = 'D'

    def render_open_tiles(self):
        """Alters self.tiles to contain appropriate characters for open tiles,
        including any of their occupants.
        """
        for tile in self.open_tiles:
            relative_x = tile.x - self.position.x 
            relative_y = tile.y - self.position.y
            if tile.occupant:
                self.tiles[relative_y][relative_x] = tile.occupant.render()
            else:
                self.tiles[relative_y][relative_x] = ' '

    def render_walls(self):
        """Alters self.tiles to contain appropriate characters for this room's walls.
        """
        for x in range(self.width):
            for y in range(self.height):
                # This tile is a horizontal wall.
                if y == 0 or y == self.height - 1:
                    self.tiles[y][x] = '-'
                elif x == 0 or x == self.width - 1:
                    self.tiles[y][x] = '|'
                else:
                    self.tiles[y][x] = 'X'
