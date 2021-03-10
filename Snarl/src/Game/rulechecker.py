from occupants import Character, Wall, Block, Adversary

class Rulechecker:
    def is_valid_move(self, entity, dest, current_level):
        """ Is moving the entity from src to dest a valid move on the provided level?
        """
        if hasattr(entity, "character"):
            return self.is_valid_player_move(entity, dest, current_level)
        elif isinstance(entity, Adversary):
            return self.is_valid_adversary_move(entity, dest, current_level)

    def is_valid_player_move(self, player, dest, current_level):
        """ Is moving the player from src to dest a valid move on the provided level?
        The player should be able to make 2 cardinal moves onto traversable tiles.
        """
        src = current_level.locate_occupant(player)
        x_dist = abs(src.x - dest.x)
        y_dist = abs(src.y - dest.y)
        dest_open = self.is_open_tile(current_level.get_tile(dest))
        
        return x_dist + y_dist < 3 and dest_open

    def is_valid_adversary_move(self, adversary, dest, current_level):
        """ Is moving the adversary from src to dest a valid move on the provided level?
        """
        src = current_level.locate_occupant(adversary)
        x_dist = abs(src.x - dest.x)
        y_dist = abs(src.y - dest.y)
        dest_open = self.is_open_tile(current_level.get_tile(dest), Adversary)
        
        return x_dist + y_dist < 2 and dest_open

    def is_level_over(self, level):
        """ Has the given level been completed? Does not tell you if the level
        was won or lost.
        """
        return len(level.characters) == 0

    def is_game_over(self, gamestate):
        """ Has the game been completed?
        """
        # TODO: This can be implemented in a later milestone.
        return True

    def did_players_win(self, gamestate):
        """ Are there any players left alive? This method assumes the game is over.
        """
        return gamestate.current_level.characters != []

    def is_open_tile(self, tile, entity_type=None):
        """Checks that this tile is a type that can be moved to. In the future, this may need
        to take the type of the moving entity in order to check validity.
        """
        has_player = any([isinstance(occ, Character) for occ in tile.occupants])
        # Adversaries are allowed to move onto player-occupied spaces.
        if entity_type == Adversary:
            has_player = False
        has_wall = any([isinstance(occ, Wall) for occ in tile.occupants])
        has_block = any([isinstance(occ, Block) for occ in tile.occupants])
        
        return not has_player and not has_block and not has_wall