import random
from .gamestate import Gamestate
from .rulechecker import Rulechecker
from .occupants import Entity, Character, Adversary
from .turnorder import Turnorder
# from observer import Observer # TODO uncomment this once it exists

class Gamemanager:
    def __init__(self, max_players = 4, view_distance = 2, num_of_levels = 1,):
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
        # This is populated when the game is started.
        self.game_state = None
        self.turn_order = Turnorder([])
        self.current_turn = None
        self.player_list = []
        self.adversary_list = []
        self.observers = []

    def start_game(self, level):
        """ Begin the game by placing all the players in the top left room of the first level.
        """
        # Initialize game state and begin
        # TODO: the '0' will be changed to # of adversaries when we add adversaries.
        self.game_state = Gamestate(level, len(self.player_list), 0)
        top_left_room = self.game_state.get_top_left_room()
        open_tiles = top_left_room.open_tiles.copy()

        if len(self.player_list) > len(open_tiles):
            raise ValueError("There are not enough tiles in the first room for each player to have a spot.")

        random.shuffle(open_tiles)

        for player in self.player_list:
            character_location = open_tiles.pop()
            self.game_state.add_character(player.character, character_location)

        self.run()

    def get_move(self):
        """ Determine the type of the entity currently moving and get the move they want to make.
        """
        if not self.game_state:
            raise ValueError("Cannot call get_move when the game has not started!")
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
        if not self.game_state:
            raise ValueError("Cannot call get_player_move when the game has not started!")
        try:
            current_player = next(player for player in self.player_list if player.character == self.current_turn)
            return current_player.move()
        except:
            raise ValueError("Attempted to get player move from a player who does not exist!")

    def get_adversary_move(self):
        """ Receive the next move from an adversary either from STDIN or from some other entry
        method/client.
        """
        # TODO: No adversaries yet; can be implemented in a later milestone.
        if not self.game_state:
            raise ValueError("Cannot call get_adversary_move when the game has not started!")

    def update_players(self):
        """ Update all the players about changes to the Gamestate surrounding them. This
        happens every time any player moves or there is an interaction that could change
        the way the level looks.
        """
        if not self.game_state:
            raise ValueError("Cannot call update_players when the game has not started!")

        for player in self.player_list:
            grid = self.game_state.get_character_surroundings(player.character, self.view_distance)
            player.update_surroundings(grid)

    def render(self):
        """ Return an ASCII representation of the current game state.
        """
        if not self.game_state:
            raise ValueError("Cannot call render when the game has not started!")

        return self.game_state.render()

    def begin_next_level(self):
        """ Begin the next Level of the dungeon by moving all the players to the next
        Level. If the game should end, then quit the game via self.quit_game().
        """
        # TODO: Implement later; per milestone spec this can be a stub for now.
        if not self.game_state:
            raise ValueError("Cannot call begin_next_level when the game has not started!")

    def quit_game(self):
        """ Quit the game.
        """
        # TODO: Implement later; per milestone spec this can be a stub for now.
        if not self.game_state:
            raise ValueError("Cannot call quit_game when the game has not started!")

    def add_player(self, player):
        """ Register a new player to the game and add it to the correct spot in the turn order.
        """
        if player in set(self.player_list.copy()):
            raise ValueError("Cannot have duplicate players in a game!")
        elif len(self.player_list) == self.max_players:
            raise ValueError("Cannot add more than " + str(self.max_players) + " players to a game!")
        
        self.player_list.append(player)
        self.turn_order.add(player)
        self.observers.append(player)

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

    # TODO: should we just put players in this list and notify them taht way? or do it separately?
    def notify_observers(self):
        """ Notify all Observers of a change to the Gamestate.
        """
        for observer in self.observers:
            observer.notify(self.game_state)

    def move(self, move):
        """ Determine if the provided move is valid. If so, perform it.
        """
        if not self.game_state:
            raise ValueError("Cannot call move when the game has not started!")
        # throws exception with helpful message if move is invalid
        self.rule_checker.is_valid_move(self.current_turn, move, self.game_state.current_level)
        self.game_state.move(self.current_turn, move)

    def run(self):
        """ Main game loop.
        """
        if not self.game_state:
            raise ValueError("Cannot call run when the game has not started!")

        while not self.rule_checker.is_game_over(self.game_state):
            move = self.get_move()
            try:
                self.move(move)
            except Exception as e:
                print("You can't do that! " + e)
            self.update_players() # might be deprecated and replaced with notify_observers
            # self.notify_observers()
            self.current_turn = self.turn_order.next()