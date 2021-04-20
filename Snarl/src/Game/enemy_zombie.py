from .enemy import Enemy
from .occupants import Zombie
import random
from .rulechecker import Rulechecker
from .tile import Tile

class EnemyZombie(Enemy):
    """Represents the controller of a Zombie in a SNARL game.
    """
    def __init__(self, name : str, entity_name : str) -> None:
        super().__init__(name, Zombie, entity_name)
    
    def _determine_move(self):
        """Determines what move this zombie should make depending on whether or not
        the player is in the same room.
        """
        if self.state is None or self.location is None:
            raise RuntimeError("Cannot get Zombie move before Zombie has game info!")
        
        players_in_room = self._get_players_in_room()
        move = None
        if len(players_in_room) > 0:
            # Move towards the closest player
            move = self._get_move_to_player(players_in_room[0])
        else:
            # Move in a random valid direction.
            move = self._get_random_open_dir()
        
        print("self.location: ")
        print("x: " + str(self.location.x) + ", y: " + str(self.location.y))
        print("next move: ")
        if move == None:
            print("move is null")
        else:
            print("x: " + str(move.x) + ", y: " + str(move.y))
        return move
    
    def _get_move_to_player(self, player_loc):
        """Gets a move that is closer to the given player location but still valid.
        """
        valid_moves = self._get_valid_cardinal_moves()
        if valid_moves == []:
            return None
        dist_to_player = lambda t: player_loc.distance(t)
        return sorted(valid_moves, key=dist_to_player)[0]

    def _get_random_open_dir(self):
        """Using the current state, return a tile that is a valid move in a random direction.
        If there are no valid move directions, this method returns None.
        """
        valid_moves = self._get_valid_cardinal_moves()
        if valid_moves == None:
            return None
        return random.choice(valid_moves)

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
            if room.contains(self.location):
                my_room = room
                break
        
        chars_in_room = list(filter(lambda c : my_room.contains(c), character_locs))
        # Get closest character in room
        return sorted(chars_in_room, key=lambda c: c.distance(self.location))

        
        