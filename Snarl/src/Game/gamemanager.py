import random
from gamestate import Gamestate
from rulechecker import Rulechecker
from occupants import Entity, Character, Adversary
from turnorder import Turnorder
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
        self.turn_order = Turnorder([])
        self.current_turn = None
        self.player_list = []
        self.adversary_list = []
        self.observers = []

    def start_game(self):
        """ Begin the game by placing all the players in the top left room of the first level.
        """
        top_left_room = self.game_state.get_top_left_room()
        open_tiles = top_left_room.open_tiles.copy()

        if len(self.player_list) < len(open_tiles):
            raise ValueError("There are not enough tiles in the first room for each player to have a spot.")

        random.shuffle(open_tiles)

        for player in self.player_list:
            character_location = open_tiles.pop()
            self.game_state.add_character(player, character_location)

        # TODO make a gamestate and set self.game_state to it
        self.run()

    def get_move(self):
        """ Determine the type of the entity currently moving and get the move they want to make.
        """
        if isinstance(self.current_turn, Character):
            return self.get_player_move()
        elif isinstance(self.current_turn, Adversary):
            return self.get_adversary_move()
        else:
            raise TypeError("You're trying to move something that isn't a character or an adversary.")

    def get_player_move(self):
        """ Receive the next move from a player either from STDIN or from some other entry
        method/client.
        """
        pass

    def get_adversary_move(self):
        """ Receive the next move from an adversary either from STDIN or from some other entry
        method/client.
        """
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

    def add_character(self, player):
        """ Register a new player to the game and add it to the correct spot in the turn order.
        """
        if player in set(self.player_list.copy()):
            raise ValueError("Cannot have duplicate players in a game!")
        elif len(self.player_list) == self.max_players:
            raise ValueError("Cannot add more than " + str(self.max_players) + " players to a game!")
        
        self.player_list.append(player)
        self.turn_order.add(player)

    def add_adveraries(self, adversaries = []):
        """ Add all the provided adversaries to the adversary_list field and put them in the correct
        place in the turn order list.
        """
        if isinstance(adversaries, Adversary):
            self.adversary_list.append(adversaries)
        elif all([isinstance(adversary, Adversary) for adversary in adversaries]):
            for adversary in adversaries:
                self.adversary_list.append(adversary)
                self.turn_order.add(adversary)
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

    def move(self, move):
        """ Determine if the provided move is valid. If so, perform it.
        """
        # throws exception with helpful message if move is invalid
        self.rule_checker.is_valid_move(self.current_turn, move, self.game_state.current_level)
        self.game_state.move(self.current_turn, move)

    def run(self):
        """ Main game loop.
        """
        # TODO finish writing this loop
        while not self.rule_checker.is_game_over(self.game_state):
            move = self.get_move()
            try:
                self.move(move)
            except Exception as e:
                print("You can't do that! " + e)
            self.update_players() # might be deprecated and replaced with notify_observers
            self.notify_observers()
            self.current_turn = self.turn_order.next()