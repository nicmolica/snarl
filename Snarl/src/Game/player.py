from abc import ABC, abstractmethod
from .tile import Tile

class Player(ABC):
    @abstractmethod
    def __eq__(self, other):
        """ Is this Player equal to another Player?
        """
        pass

    @abstractmethod
    def __hash__(self):
        """ Return a hash of the two identifying characteristics of a Player.
        """
        pass

    @abstractmethod
    def move(self) -> Tile:
        """Given the current state of their surroundings, get a move from this
        player and return the coordinates of the desired move.
        """
        pass

    @abstractmethod
    def update_surroundings(self, grid: list):
        """Send a new grid of surrounding tiles to this player.
        """
        pass

    @abstractmethod
    def expel(self):
        """Tell this player that they were expelled from the level.
        """
        pass