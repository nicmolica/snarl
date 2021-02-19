from gamestate import Gamestate
from level import Level

class Rulechecker:
    def is_valid_player_move(self, player, src, dest, current_level):
        """ Is moving the player from src to dest a valid move on the provided level?
        """
        # player is Occupant, src is Tile (or None if player isn't a Player/Adversary), dest is Tile, level is Level
        return True

    def is_valid_adversary_move(self, player, src, dest, current_level):
        """ Is moving the adversary from src to dest a valid move on the provided level?
        """
        # player is Occupant, src is Tile (or None if player isn't a Player/Adversary), dest is Tile, level is Level
        return True

    def is_level_over(self, level):
        """ Has the given level been completed?
        """
        return True

    def is_game_over(self, gamestate):
        """ Has the game been completed?
        """
        return True

    def did_players_win(self, gamestate):
        """ Are there any players left alive? This method assumes the game is over.
        """
        return gamestate.current_level.players != []