from .occupants import Occupant, Character, Adversary, Block

class Tile:
    """Represents an (x, y) tile in a Cartesian grid with nonnegative coordinates.
    May be occupied by an Occupant. This class is used both to communicate locations
    and to store actual game state data.
    """
    def __init__(self, x: int, y: int, occupants: list = []):
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

    def add_occupant(self, occupant: Occupant):
        """ Blindly add the passed Occupant to this Tile, without verifying if there are
        other Occupants already there.
        """
        if isinstance(occupant, Occupant):
            self.occupants.append(occupant)
        else:
            raise TypeError("Cannot add a non-Occupant to a tile.")

    def get_character(self) -> Character:
        """ Return the player on this Tile, if there is one. Assume there will never be
        more than one.
        """
        for occupant in self.occupants:
            if isinstance(occupant, Character):
                return occupant

        return None

    def get_adversary(self) -> Adversary:
        """ Return the adversary on this Tile, if there is one. Assume there will never be
        more than one.
        """
        for occupant in self.occupants:
            if isinstance(occupant, Adversary):
                return occupant

        return None

    def has_block(self) -> bool:
        """ Does this tile have a block on it?
        """
        for occupant in self.occupants:
            if isinstance(occupant, Block):
                return True

        return False

    def has_character(self) -> bool:
        """ Does this tile have a character on it?
        """
        for occupant in self.occupants:
            if isinstance(occupant, Character):
                return True

        return False

    def has_adversary(self) -> bool:
        """ Does this tile have an adversary on it?
        """
        for occupant in self.occupants:
            if isinstance(occupant, Adversary):
                return True

        return False

    def has_occupant(self, occupant_type) -> bool:
        """ Does the tile have an occupant of the given type on it?
        """
        for occupant in self.occupants:
            if isinstance(occupant, occupant_type):
                return True

        return False

    def coordinates_equal(self, other) -> bool:
        """ Do the coordinates of this tile match the coordinates of the other tile?
        """
        return isinstance(other, Tile) and self.x == other.x and self.y == other.y

    def remove_occupant(self, occupant) -> None:
        """Removes the given occupant from this tile's occupants.
        """
        self.occupants.pop(self.occupants.index(occupant))

    def distance(self, other) -> int:
        """ Manhattan distance between this and another tile.
        """
        if not isinstance(other, Tile):
            raise TypeError("Cannot measure distance to something that is not a tile!")
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def render(self) -> str:
        """Renders the given tile, showing a player or adversary if any exist on this tile.
        """
        if self.occupants != []:
            # We always want to show a character avatar if there is one. Otehrwise we could end up
            # with invisible characters.
            character = next(iter([occ for occ in self.occupants if isinstance(occ, Character)]), None)
            if character is not None:
                return character.render()
            # Similarly with adversaries.
            adv = next(iter([occ for occ in self.occupants if isinstance(occ, Adversary)]), None)
            if adv is not None:
                return adv.render()
            return self.occupants[0].render()
        else:
            return ' '