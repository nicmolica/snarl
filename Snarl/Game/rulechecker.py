from occupants import Player, Wall, Block, Adversary

class Rulechecker:
    def is_open_tile(self, tile, entity_type=None):
        """Checks that this tile is a type that can be moved to. In the future, this may need
        to take the type of the moving entity in order to check validity.
        """
        has_player = any([isinstance(occ, Player) for occ in tile.occupants])
        # Adversaries are allowed to move onto player-occupied spaces.
        if entity_type == Adversary:
            has_player = False
        has_wall = any([isinstance(occ, Wall) for occ in tile.occupants])
        has_block = any([isinstance(occ, Block) for occ in tile.occupants])
        
        return not has_player and not has_block and not has_wall

    def is_valid_player_move(self, src, dest, current_level):
        """ Is moving the player from src to dest a valid move on the provided level?
        The player should be able to make 2 cardinal moves onto traversable tiles.
        """
        x_dist = abs(src.x - dest.x)
        y_dist = abs(src.y - dest.y)
        dest_open = self.is_open_tile(current_level.tiles[dest.y][dest.x])
        
        return x_dist + y_dist < 3 and dest_open

    def is_valid_adversary_move(self, src, dest, current_level):
        """ Is moving the adversary from src to dest a valid move on the provided level?
        """
        x_dist = abs(src.x - dest.x)
        y_dist = abs(src.y - dest.y)
        dest_open = self.is_open_tile(current_level.tiles[dest.y][dest.x], Adversary)
        return x_dist + y_dist < 2 & dest_open

    def is_level_over(self, level):
        """ Has the given level been completed?
        """
        # TODO: This can be implemented in a later milestone.
        return True

    def is_game_over(self, gamestate):
        """ Has the game been completed?
        """
        # TODO: This can be implemented in a later milestone.
        return True

    def did_players_win(self, gamestate):
        """ Are there any players left alive? This method assumes the game is over.
        """
        return gamestate.current_level.players != []