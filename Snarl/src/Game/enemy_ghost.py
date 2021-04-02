import json
from .enemy import Enemy
from .occupants import Ghost
from .tile import Tile
from .rulechecker import Rulechecker

class EnemyGhost(Enemy):
    def __init__(self, name : str, entity_name : str) -> None:
        super().__init__(name, Ghost, entity_name)
    
    def _determine_move(self):
        pass

    def _get_move_to_player(self, player_loc):
        """Gets a move that is closer to the given player location but still valid.
        """
        valid_moves = self._get_valid_cardinal_moves()
        if valid_moves == []:
            return None
        # TODO consider changing method of getting dist to player for those outside of room
        dist_to_player = lambda t: abs(t.x - player_loc.x) + abs(t.y - player_loc.y)
        return sorted(valid_moves, dist_to_player)[0]

    def _get_valid_cardinal_moves(self):
        """Return the possible cardinal moves for this ghost.
        """
        # If any coordinate is 0, can't move in that axis's negative direction.
        up = Tile(self.location.x, self.location.y + 1)
        right = Tile(self.location.x + 1, self.location.y)
        cardinals = [up, right]
        if (self.location.x > 0):
            left = Tile(self.location.x - 1, self.location.y)
            cardinals.append(left)
        if (self.location.y > 0):
            down = Tile(self.location.x, self.location.y - 1)
            cardinals.append(down)
        
        valid = lambda t : Rulechecker().is_valid_move(self.entity, t, self.state.current_level)
        valid_moves = list(filter(valid, cardinals))
        return valid_moves

    def _get_players_in_range(self):
        """Returns a list of the characters that are in the same room as this zombie.
        Returns an empty list if there are no such characters.
        This list is sorted in ascending order by closest character.
        """
        characters = self.state.get_current_characters()
        character_locs = []
        for character in characters:
            character_locs.append(self.state.get_entity_location(character))

        rooms = self.state.current_level.rooms
        my_room = None
        for room in rooms:
            if room.contains(self.location):
                my_room = room
                break
        
        chars_in_room = list(filter(lambda c : my_room.contains(c), character_locs))
        # Get closest character in room
        return sorted(chars_in_room, lambda c : abs(c.x - self.location.x) + abs(c.y - self.location.y))