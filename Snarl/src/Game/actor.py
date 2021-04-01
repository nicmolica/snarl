from abc import ABC, abstractmethod
from .tile import Tile

class Actor(ABC):
    @abstractmethod
    def __eq__(self, other):
        """ Is this Actor equal to another Actor?
        """
        pass

    @abstractmethod
    def __hash__(self):
        """ Return a hash of the two identifying characteristics of an Actor.
        """
        pass

    @abstractmethod
    def move(self) -> Tile:
        """Given the current state of their surroundings, get a move from this
        actor and return the coordinates of the desired move.
        """
        pass

    @abstractmethod
    def notify(self, grid: list):
        """Send the new state information to this actor. The actor may not receive the
        full level information.
        """
        pass

    @abstractmethod
    def expel(self):
        """Tell this actor that they were expelled from the level.
        """
        pass

    @abstractmethod
    def get_entity(self):
        """Return the entity representing this Actor.
        """
        pass