from abc import ABC, abstractmethod
from .gamestate import Gamestate

class AbstractObserver(ABC):
    """Abstract observer interface that can receive updates about the current gamestate.
    """
    @abstractmethod
    def notify(self, gamestate: Gamestate):
        """This is essentially a setter. It sets the `gamestate` field of this `Observer` object
        to the current `Gamestate` of the `Gamemanager` that is being observed. This will be called
        every time there is a change to the `Gamestate` so that the `Observer` will always have
        up-to-date information.
        """
        pass

    @abstractmethod
    def render(self):
        """Returns an ASCII representation of the current `Gamestate`. This is useful for
        displaying the game to stakeholders. It also means that the game visualization can
        be easily sent to an external server, if so desired.
        """
        pass