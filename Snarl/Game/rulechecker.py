from gamestate import Gamestate
from level import Level

class Rulechecker:
    def is_valid_player_move(self, player, src, dest, current_level):
        # player is Occupant, src is Tile (or None if player isn't a Player/Adversary), dest is Tile, level is Level
        return True

    def is_valid_adversary_move(self, player, src, dest, current_level):
        # player is Occupant, src is Tile (or None if player isn't a Player/Adversary), dest is Tile, level is Level
        return True

    def is_level_over(self, level):
        return True

    def is_game_over(self, gamestate):
        return True

    def did_players_win(self, gamestate):
        return gamestate.current_level.players != []