from .observer import Observer
from .utils import grid_to_string
from .gamestate import Gamestate
import sys

class ObserverImpl(Observer):
    def __init__(self):
        self.gamestate = None
        self.ip = None

    def notify(self, gamestate):
        self.gamestate = gamestate

    def render(self):
        """Returns an ASCII representation of the current `Gamestate`. This is useful for
        displaying the game to stakeholders. It also means that the game visualization can
        be easily sent to an external server, if so desired.
        """
        sys.stdout.write(grid_to_string(self.gamestate.render()))

    def transmit_view(self, ip):
        """Given an IP address, creates a socket that transmits the current view of the `Gamestate`
        to a server. It obtains the current view by calling the `render()` method. This view may be
        either total or partial, depending on what the `Observer` ends up being used for.
        """
        # TODO: This can be done later, when networking is a required feature.
        pass