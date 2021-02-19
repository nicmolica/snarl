from rulechecker import Rulechecker
from level import Level

class Gamestate:
    def __init__(self, level, num_of_players, num_of_adversaries):
        """ Creates a Gamestate with the given initial level and number of
        players and adversaries to create the game with.
        """
        self.levels = []
        self.levels.append(level)
        self.current_level = level
        self.rule_checker = Rulechecker()
        if num_of_players in range(1, 5):
            self.num_of_players = num_of_players
        else:
            raise ValueError("There must be 1-4 players.")

        # TODO: check valid number of adversaries
        self.num_of_adversaries = num_of_adversaries
    
    def move_player(self, player, dest):
        """ Uses the rule checker to verify a Player move is valid,
        then performs that move if it is.
        """
        if not self.rule_checker.is_valid_player_move(player, \
            self.current_level.locate_occupant(player), dest, self.current_level):
            raise ValueError("Invalid player move!")
        
        self.current_level.move_occupant(player, dest)
        
    def move_adversary(self, adversary, dest):
        """ Uses the rule checker to verify an Adversary move is valid,
        then performs that move if it is.
        """
        if not self.rule_checker.is_valid_adversary_move(adversary, \
            self.current_level.locate_occupant(adversary), dest, self.current_level):
            raise ValueError("Invalid adversary move!")

        self.current_level.move_occupant(adversary, dest)

    def complete_level(self, are_we_done):
        """ After a level has been completed, mark it as completed, generate
        the next level, and move all the players up to the next level.
        """
        # mark current level as complete
        self.current_level.is_completed = True

        # TODO generate next level (if not are_we_done)

        # TODO move all players to next level
        