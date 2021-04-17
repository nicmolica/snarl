from .observer import AbstractObserver
from .utils import grid_to_string
from .gamestate import Gamestate
import sys

class Observer(AbstractObserver):
    def __init__(self):
        self.gamestate = None
        self.ip = None

    def notify(self, gamestate):
        """Notifies this observer with the new gamestate information. This observer
        will render when notified.
        """
        self.gamestate = gamestate
        self.render()

    def render(self):
        """Returns an ASCII representation of the current `Gamestate`. This is useful for
        displaying the game to stakeholders. It also means that the game visualization can
        be easily sent to an external server, if so desired.
        """
        return self._render_to_stream(sys.stdout)

    def _render_to_stream(self, stream):
        """Renders to the particular output stream.
        """
        stream.write(grid_to_string(self.gamestate.render()) + "\n\n")