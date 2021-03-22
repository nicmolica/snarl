from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def notify(self, gamestate):
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

    @abstractmethod
    def transmit_view(self, ip):
        """Given an IP address, creates a socket that transmits the current view of the `Gamestate`
        to a server. It obtains the current view by calling the `render()` method. This view may be
        either total or partial, depending on what the `Observer` ends up being used for.
        """
        pass