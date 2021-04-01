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

    def move(self):
        """Given the current state of their surroundings, get a move from this
        player and return the coordinates of the desired move.
        """
        if self.out:
            self.out.write("Please provide a move in the form [x, y]:\n")
        return self._move_with_input(input)
    
    @abstractmethod
    def _move_with_input(self, input_func):
        pass

    def notify(self, arg):
        """Send a new grid of surrounding tiles to this player.
        """
        if type(arg) is not dict:
            raise RuntimeError("Player notification must be dictionary!")
        if self.out:
            self.out.write(arg)
        if "layout" in arg:
            self.surroundings = arg["layout"]


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