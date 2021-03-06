from gamestate import Gamestate
from rulechecker import Rulechecker
from occupants import Entity, Player, Adversary
# from observer import Observer # TODO uncomment this once it exists

class Gamemanager:
    def __init__(self, max_players = 4, view_distance = 2, num_of_levels = 1):
        if view_distance >= 1:
            self.view_distance = view_distance
        else:
            raise ValueError("Invalid view distance: " + str(view_distance))

        if num_of_levels >= 1:
            self.num_of_levels = num_of_levels
        else:
            raise ValueError("Invalid number of levels: " + str(num_of_levels))

        if max_players >= 1:
            self.max_players = max_players
        else:
            raise ValueError("Invalid number of players: " + str(max_players))

        self.rule_checker = Rulechecker()
        self.game_state = None # TODO fix this so there's an actual gamestate
        self.turn_order = []
        self.current_turn = None
        self.player_list = []
        self.adversary_list = []
        self.observers = []

    def start_game(self):
        """ Begin the game by placing all the players in the top left room of the first level.
        """
        pass

    def get_player_move(self):
        """ Receive the next move from a player either from STDIN or from some other entry
        method/client.
        """
        pass

    def move_adversaries(self):
        """ Once the players are done moving, let all the adversaries take their turns.
        """
        # TODO change this so that it only moves a single adversary to allow more freedom with turn order
        pass

    def update_players(self):
        """ Update all the players about changes to the Gamestate surrounding them. This
        happens every time any player moves or there is an interaction that could change
        the way the level looks.
        """
        pass

    def render(self):
        """ Return an ASCII representation of the current game state.
        """
        return self.game_state.render()

    def begin_next_level(self):
        """ Begin the next Level of the dungeon by moving all the players to the next
        Level. If the game should end, then quit the game via self.quit_game().
        """
        pass

    def quit_game(self):
        """ Quit the game.
        """
        pass

    def add_player(self, player):
        """ Register a new player to the game and add it to the correct spot in the turn order.
        """
        if player in set(self.player_list.copy()):
            raise ValueError("Cannot have duplicate players in a game!")
        elif len(self.player_list) == self.max_players:
            raise ValueError("Cannot add more than " + str(self.max_players) + " players to a game!")
        
        self.player_list.append(player)
        self.turn_order.append(player)

    def add_adveraries(self, adversaries = []):
        """ Add all the provided adversaries to the adversary_list field and put them in the correct
        place in the turn order list.
        """
        if isinstance(adversaries, Adversary):
            self.adversary_list.append(adversaries)
        elif all([isinstance(adversary, Adversary) for adversary in adversaries]):
            for adversary in adversaries:
                self.adversary_list.append(adversary)
                self.turn_order.append(adversary)
        else:
            raise TypeError("All adversaries must be of the type \"Adversary.\"")

    def register_observer(self, observer):
        """ Register a new Observer by adding it to the list of observers.
        """
        self.observers.append(observer)

    def notify_observers(self):
        """ Notify all Observers of a change to the Gamestate.
        """
        for observer in self.observers:
            observer.notify(self.game_state)