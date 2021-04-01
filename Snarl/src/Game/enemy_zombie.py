from .enemy import Enemy
from .occupants import Zombie
import random
from .rulechecker import Rulechecker

class EnemyZombie(Enemy):
    def __init__(self, enemy_name : str, entity_name : str) -> None:
        super().__init__(enemy_name, Zombie, entity_name)

    def _move_with_input(self, input_func):
        """Returns a player move given the input string representing the player
        input.
        """
        return self._determine_move()
    
    def _determine_move(self):
        """Determines what move this zombie should make depending on whether or not
        the player is in the same room.
        """
        if self.state is None or self.loc is None:
            raise RuntimeError("Cannot get Zombie move before Zombie has game info!")
        
        players_in_room = self._get_players_in_room()
        if len(players_in_room) > 0:
            # Move towards the closest player
            return self._get_move_to_player(players_in_room[0])
        else:
            # Move in a random valid direction.
            return self._get_random_open_dir()
    
    def _get_move_to_player(self, player_loc):
        """Gets a move that is closer to the given player location but still valid.
        """
        valid_moves = self._get_valid_cardinal_moves()
        if valid_moves == []:
            return None
        dist_to_player = lambda t: abs(t.x - player_loc.x) + abs(t.y - player_loc.y)
        return sorted(valid_moves, dist_to_player)[0]

    def _get_random_open_dir(self):
        """Using the current state, return a tile that is a valid move in a random direction.
        If there are no valid move directions, this method returns None.
        """
        valid_moves = self._get_valid_cardinal_moves()
        if valid_moves == []:
            return None
        return random.choice(valid_moves)

    def _get_valid_cardinal_moves(self):
        """Return the possible cardinal moves for this zombie.
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

    def _get_players_in_room(self):
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
            if room.contains(self.loc):
                my_room = room
                break
        
        chars_in_room = filter(lambda c : room.contains(c), character_locs)
        # Get closest character in room
        return sorted(iterable, lambda c : abs(c.x - self.loc.x) + abs(c.y - self.loc.y))

        
        