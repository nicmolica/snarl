from .actor import Actor
from abc import abstractmethod
from .tile import Tile

class AbstractPlayer(Actor):
    """(Mostly) abstract representation of a player. Defines interface for notifying player
    about the game and getting moves/entity information from the player.
    """
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
    def expel(self):
        """Tell this player that they were expelled from the level.
        """
        pass

    @abstractmethod
    def get_entity(self):
        pass

    def notify(self, arg):
        """ Give this player information about their surroundings.
        """
        if type(arg) is not dict:
            raise RuntimeError("Player notification must be dictionary!")
        if self.out:
            self.out.write(arg)
        if "layout" in arg:
            self.surroundings = arg["layout"]
        if "position" in arg:
            self.location = arg["position"]
