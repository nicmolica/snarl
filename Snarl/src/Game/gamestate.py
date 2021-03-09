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

        if (num_of_adversaries < 0):
            raise ValueError("Cannot pass a negative quantity of adversaries!")

        self.num_of_adversaries = num_of_adversaries

    def move(self, dest):
        """ Move the player/adversary to the new location.
        """
        # TODO write this method (should simply do type checking and call move_player or move_adversary)
        pass
    
    def move_player(self, src, dest):
        """ Uses the rule checker to verify a Character move is valid,
        then performs that move if it is.
        """
        # TODO remove rule_checker validation from here and put it in gamemanagers
        if not self.rule_checker.is_valid_player_move(self.current_level.get_tile(src), \
            self.current_level.get_tile(dest), self.current_level):
            raise ValueError("Invalid player move!")
        
        self.current_level.move_occupant(self.current_level.get_tile(src).get_player(), \
            self.current_level.get_tile(dest))
        
    def move_adversary(self, src, dest):
        """ Uses the rule checker to verify an Adversary move is valid,
        then performs that move if it is.
        """
        # TODO remove rule_checker validation from here and put it in gamemanagers
        if not self.rule_checker.is_valid_adversary_move(self.current_level.get_tile(src), \
            self.current_level.get_tile(dest), self.current_level):
            raise ValueError("Invalid adversary move!")

        self.current_level.move_occupant(self.current_level.get_tile(src).get_adversary(), \
            self.current_level.get_tile(dest))

    def complete_level(self, are_we_done):
        """ After a level has been completed, mark it as completed, generate
        the next level, and move all the players up to the next level.
        """
        # mark current level as complete
        self.current_level.is_completed = True

        # TODO generate next level (if not are_we_done)-this will happen when we have level gen
        # TODO move all players to next level

    def get_tiles(self):
        """ Return the full array of tiles in the current level.
        """
        return self.current_level.get_tiles()
        
    def get_tiles_range(self, tile1, tile2):
        """ Return the array of tiles between the two provided tiles in the current level.
        """
        return self.current_level.get_tiles_range(tile1, tile2)
        
    def add_character(self, character, location):
        """ Add a character to the current Level.
        """
        self.current_level.add_character(character, location)

    def get_top_left_room(self):
        """ Get the top left room of the current Level.
        """
        return self.current_level.get_top_left_room()