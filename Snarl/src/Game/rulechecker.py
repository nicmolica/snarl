from .occupants import Character, Wall, Block, Adversary, Entity
from .tile import Tile
from .level import Level

class Rulechecker:
    def is_valid_move(self, entity: Entity, dest: Tile, current_level: Level) -> bool:
        """ Is moving the entity from src to dest a valid move on the provided level?
        """
        if isinstance(entity, Character):
            return self._is_valid_player_move(entity, dest, current_level)
        elif isinstance(entity, Adversary):
            return self._is_valid_adversary_move(entity, dest, current_level)

    def _is_valid_player_move(self, character: Character, dest: Tile, current_level: Level) -> bool:
        """ Is moving the player from src to dest a valid move on the provided level?
        The player should be able to make 2 cardinal moves onto traversable tiles.
        """
        src = current_level.locate_occupant(character)
        x_dist = abs(src.x - dest.x)
        y_dist = abs(src.y - dest.y)
        dest_open = self.is_open_tile(current_level.get_tile(dest))
        too_far = x_dist + y_dist > 2 
        if too_far or not dest_open:
            s= "Invalid move: "
            if too_far:
                s += "Destination too far, "
            if not dest_open:
                s += "Destination blocked"
            raise RuntimeError(s)
        
        return True

    def _is_valid_adversary_move(self, adversary: Adversary, dest: Tile, current_level: Level) -> bool:
        """ Is moving the adversary from src to dest a valid move on the provided level?
        """
        src = current_level.locate_occupant(adversary)
        x_dist = abs(src.x - dest.x)
        y_dist = abs(src.y - dest.y)
        dest_open = self.is_open_tile(current_level.get_tile(dest), Adversary)
        
        return x_dist + y_dist < 2 and dest_open

    def is_level_over(self, level: Level) -> bool:
        """ Has the given level been completed? Does not tell you if the level
        was won or lost.
        """
        return len(level.characters) == 0

    def is_game_over(self, gamestate) -> bool:
        """ Has the game been completed?
        """
        # TODO: This can be implemented in a later milestone.
        return True

    def did_players_win(self, gamestate) -> bool:
        """ Are there any players left alive? This method assumes the game is over.
        """
        return gamestate.current_level.characters != []

    def is_open_tile(self, tile: Tile, entity_type: type = None) -> bool:
        """Checks that this tile is a type that can be moved to. In the future, this may need
        to take the type of the moving entity in order to check validity.
        """
        has_player = tile.has_character()
        # Adversaries are allowed to move onto player-occupied spaces.
        if entity_type == Adversary:
            has_player = False
        has_block = tile.has_block()
        
        return not has_player and not has_block