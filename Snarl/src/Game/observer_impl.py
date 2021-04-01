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
        return self._render_to_stream(sys.stdout)

    def _render_to_stream(self, stream):
        """Renders to the particular output stream.
        """
        stream.write(grid_to_string(self.gamestate.render()))