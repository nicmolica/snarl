from .occupants import Character, Wall, Block, Zombie, Ghost, Entity, Adversary, Door, Wall
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
        if src.coordinates_equal(dest):
            return True
        x_dist = abs(src.x - dest.x)
        y_dist = abs(src.y - dest.y)
        dest_open = self.is_open_tile(current_level.get_tile(dest), current_level)
        too_far = x_dist + y_dist > 2 
        if too_far or not dest_open:
            s= "Invalid move: "
            if too_far:
                s += "Destination too far, "
            if not dest_open:
                s += "Destination blocked, "
            s += f"Source X: {src.x} Y: {src.y} Destination: X: {dest.x} Y: {dest.y}"
            raise RuntimeError(s)
        
        return True

    def _is_valid_adversary_move(self, adversary: Adversary, dest: Tile, current_level: Level) -> bool:
        """ Is moving the adversary from src to dest a valid move on the provided level?
        """
        src = current_level.locate_occupant(adversary)
        x_dist = abs(src.x - dest.x)
        y_dist = abs(src.y - dest.y)
        dest_open = self.is_open_tile(current_level.get_tile(dest), current_level, type(adversary))
        
        return x_dist + y_dist < 2 and dest_open

    def is_level_over(self, level: Level) -> bool:
        """ Has the given level been completed? Does not tell you if the level
        was won or lost.
        """
        return len(level.characters) == 0

    def is_game_over(self, gamestate) -> bool:
        """ Has the game been completed? This means that either all the players are dead, or the game
        has been properly completed.
        """
        all_players_dead = gamestate.all_players_expelled()
        state_complete = gamestate.game_complete()
        return state_complete or all_players_dead
        

    def did_players_win(self, gamestate) -> bool:
        """ Are there any players left alive? This method assumes the game is over.
        """
        return gamestate.current_level.characters != []

    def is_open_tile(self, tile: Tile, current_level, entity_type: type = None) -> bool:
        """Checks that this tile is a type that can be moved to. In the future, this may need
        to take the type of the moving entity in order to check validity.
        """
        has_player = tile.has_character()
        has_block = tile.has_block()
        # Adversaries are allowed to move onto player-occupied spaces.
        if entity_type is not None and issubclass(entity_type, Adversary):
            has_player = False
            has_key = current_level.get_tile(tile).coordinates_equal(current_level.get_level_key())
            has_exit = current_level.get_tile(tile).coordinates_equal(current_level.get_level_exit())
            has_door = current_level.get_tile(tile).has_occupant(Door)
            if entity_type == Ghost:
                # Ghosts can move through walls
                has_block = has_exit or has_key
            if entity_type == Zombie:
                # Zombies can't move onto doors
                has_block = has_block or has_door or has_exit or has_key
        
        return not has_player and not has_block