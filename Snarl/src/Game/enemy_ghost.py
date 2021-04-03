import json
import random
import sys
from .enemy import Enemy
from .occupants import Ghost, Wall, Block, LevelKey, LevelExit
from .tile import Tile
from .rulechecker import Rulechecker

class EnemyGhost(Enemy):
    def __init__(self, name : str, entity_name : str) -> None:
        super().__init__(name, Ghost, entity_name)
    
    def _determine_move(self):
        """ Determines what move this ghost should make depending on whether or not
        the player is in the ghost's range
        """
        if self.state is None or self.location is None:
            raise RuntimeError("Cannot get Ghost move before Ghost has game info!")

        players_in_range = self._get_players_in_range()
        if len(players_in_range) > 0:
            # Move towards the closest player
            return self._get_move_to_player(players_in_range[0])
        else:
            # Move towards the closest wall
            return self._get_move_to_wall()

    def _get_move_to_player(self, player_loc):
        """Gets a move that is closer to the given player location but still valid.
        """
        # 1. figure out all the valid cardinal moves
        valid_cardinal_moves = self._get_valid_cardinal_moves()
        if valid_cardinal_moves == []:
            return None
        
        # 2. remove moves that take us farther away from player
        dist_to_player = lambda t: player_loc.distance(t)
        current_dist = dist_to_player(self.location)
        valid_progressive_moves = list(filter(lambda t: current_dist >= dist_to_player(t), valid_cardinal_moves))
        
        # 3. remove moves that go right into a wall or block (in case we're in a hallway or at the edge of a room)
        valid_moves_not_walls = list(filter(lambda t: \
            not self.state.current_level.get_tile(t).has_occupant(Block), \
                    valid_progressive_moves))

        # 4. if this leaves us with no moves, just move into the wall and hope for the best
        if len(valid_moves_not_walls) == 0:
            return random.choice(valid_cardinal_moves)
        
        # 5. if we are left with moves, pick the one that brings us closest to the player
        return sorted(valid_progressive_moves, key=dist_to_player)[0]

    def _get_move_to_wall(self):
        """ Figure out where the closest wall is and provide a move that bring us closer to it.
        """
        cardinals = self._get_valid_cardinal_moves()
        if cardinals == None:
            return None
        else:
            return sorted(cardinals, key=self._distance_to_closest_block)[0]

    def _distance_to_closest_block(self, tile):
        """ Determine the distance between this tile and the closest block.
        """
        left, right, up, down = float("inf"), float("inf"), float("inf"), float("inf")
        width, height = self.state.current_level.calculate_level_dimensions()
        for i in range(tile.x):
            if self.state.get_tile(Tile(i, tile.y)).has_occupant(Block):
                left = tile.x - i
        for i in range(tile.y):
            if self.state.get_tile(Tile(tile.x, i)).has_occupant(Block):
                up = tile.y - i
        for i in range(tile.x, width):
            if self.state.get_tile(Tile(i, tile.y)).has_occupant(Block):
                right = i - tile.x
        for i in range(tile.y, height):
            if self.state.get_tile(Tile(tile.x, i)).has_occupant(Block):
                down = i - tile.y

        return min(left, right, up, down)

    def _get_players_in_range(self):
        """Returns a list of the characters that are in the range (10 tiles) of this ghost.
        Returns an empty list if there are no such characters.
        This list is sorted in ascending order by closest character.
        """
        characters = self.state.get_current_characters()
        character_locs = []
        for character in characters:
            character_locs.append(self.state.get_entity_location(character))
        
        chars_in_room = list(filter(lambda c : c.distance(self.location) < 10, character_locs))
        # Get closest character in room
        return sorted(chars_in_room, key=lambda c : c.distance(self.location))