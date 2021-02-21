import sys
sys.path.append('../')
import unittest
import random
from tile import Tile
from room import Room
from hallway import Hallway
from level import Level
from occupants import Player, Adversary
from rulechecker import Rulechecker
from gamestate import Gamestate

class TestRulechecker(unittest.TestCase):
    def test_is_not_open_when_player_moves_to_player_tile(self):
        rulechecker = Rulechecker()
        is_open = rulechecker.is_open_tile(Tile(3, 4, [Player()]))
        self.assertFalse(is_open)

    def test_is_open_when_adversary_moves_to_player_tile(self):
        rulechecker = Rulechecker()
        is_open = rulechecker.is_open_tile(Tile(3, 4, [Player()]), Adversary)
        self.assertTrue(is_open)

    def test_valid_player_move_2_steps_diagonal(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        is_valid = rulechecker.is_valid_player_move(Tile(2, 6), Tile(1, 7), level)
        self.assertTrue(is_valid)
    
    def test_valid_player_move_2_steps_same_dir(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        is_valid = rulechecker.is_valid_player_move(Tile(1, 9), Tile(1, 7), level)
        self.assertTrue(is_valid)

    def test_invalid_player_move_too_far(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        is_valid = rulechecker.is_valid_player_move(Tile(1, 13), Tile(1, 7), level)
        self.assertFalse(is_valid)

    def test_invalid_player_move_blocked_dest(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        is_valid = rulechecker.is_valid_player_move(Tile(0, 0), Tile(0, 2), level)
        self.assertFalse(is_valid)

    def test_valid_adversary_move(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        is_valid = rulechecker.is_valid_player_move(Tile(1, 8), Tile(1, 7), level)
        self.assertTrue(is_valid)
    
    def test_invalid_adversary_move_too_far(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        is_valid = rulechecker.is_valid_player_move(Tile(1, 11), Tile(1, 7), level)
        self.assertFalse(is_valid)

    def test_invalid_adversary_move_blocked_dest(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        is_valid = rulechecker.is_valid_player_move(Tile(0, 0), Tile(1, 0), level)
        self.assertFalse(is_valid)
        
    def test_players_won_when_players_won(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        state = Gamestate(level, 2, 0)
        players_won = rulechecker.did_players_win(state)
        self.assertTrue(players_won)

    def test_players_lost_when_players_lost(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        state = Gamestate(level, 1, 0)
        # Manually remove all players from current level; this will happen elsewhere when players
        # defeated.
        state.current_level.players = []
        players_won = rulechecker.did_players_win(state)
        self.assertFalse(players_won)

if __name__ == '__main__':
    unittest.main()