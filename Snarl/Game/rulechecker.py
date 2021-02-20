from gamestate import Gamestate
from level import Level

class Rulechecker:
    def is_valid_player_move(self, src, dest, current_level):
        """ Is moving the player from src to dest a valid move on the provided level?
        The player should be able to make 2 cardinal moves onto traversable tiles.
        """
        x_dist = abs(src.x - dest.x)
        y_dist = abs(src.y - dest.y)
        # TODO: Is dest an open tile?
        return x_dist + y_dist < 3 and Player not in [type(occ) for occ in dest.occupants]

    def is_valid_adversary_move(self, src, dest, current_level):
        """ Is moving the adversary from src to dest a valid move on the provided level?
        """
        x_dist = abs(src.x - dest.x)
        y_dist = abs(src.y - dest.y)
        # TODO: Is dest an open tile?
        return x_dist + y_dist < 2

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