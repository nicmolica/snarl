from occupants import Occupant, Player

class Tile:
    """Represents an (x, y) tile in a Cartesian grid with nonnegative coordinates.
    May be occupied by an Occupant.
    """
    def __init__(self, x, y, occupants=[]):
        """Constructs a new tile, possibly with an occupant.

        Arguments:
            occupant (Occupant): (optional) the occupant of the tile.
        
        Returns:
            None
        """
        if type(x) is not int or type(y) is not int:
            raise TypeError("Tile coordinates must be integers!")

        if x < 0 or y < 0:
            raise ValueError("Tile coordinates must be nonnegative!")
        
        self.x = x
        self.y = y

        if occupants:
            if isinstance(occupants, Occupant):
                self.occupants = [occupants]
            elif all([isinstance(occupant, Occupant) for occupant in occupants]):
                self.occupants = occupants
            else:
                raise TypeError("Occupant of a tile must be an Occupant object!")
        else:
            self.occupants = []
    
    def __eq__(self, other):
        """ Overwriting == for Tiles in order to directly compare equality.
        """
        return type(other) == Tile and self.x == other.x and self.y == other.y \
            and self.occupants == other.occupants
    
    def __hash__(self):
        """ Overwriting hash for Tiles because we overwrote ==.
        """
        return hash((self.x, self.y, str(self.occupants)))

    def render(self):
        """Renders the given tile, including the first occupant.
        """
        if self.occupants != []:
            return self.occupants[0].render()
        else:
            return ' '

    def add_occupant(self, occupant):
        """ Blindly add the passed Occupant to this Tile, without verifying if there are
        other Occupants already there.
        """
        if isinstance(occupant, Occupant):
            self.occupants.append(occupant)
        else:
            raise TypeError("Cannot add a non-Occupant to a tile.")

    def get_player(self):
        """ Return the player on this Tile, if there is one. Assume there will never be
        more than one.
        """
        for occupant in self.occupants:
            if isinstance(occupant, Player):
                return occupant

        return None