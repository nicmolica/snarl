from abc import ABC, abstractmethod
from .tile import Tile

class Actor(ABC):
    @abstractmethod
    def __init__(self, name, entity_name, out = None):
        """ This doesn't do anything, it exists just for the purpose of telling the
        abstract class which fields exist on an Actor.
        """
        self.out = out

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

    def move(self):
        """Given the current state of their surroundings, get a move from this
        player and return the coordinates of the desired move.
        """
        if self.out:
            self.out.write("Please provide a move in the form [x, y]:\n")
        return self._determine_move()

    @abstractmethod
    def _determine_move(self):
        """ Determine the next move for this actor, either by asking a human player
        for input, or by algorithmically determining the next move for an adversary.
        """
        pass

    @abstractmethod
    def notify(self, arg):
        """Send a new grid of surrounding tiles to this actor.
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