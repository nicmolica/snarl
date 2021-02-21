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

class TestRulechecker(unittest.TestCase):
    def test_is_not_open_when_player_moves_to_player_tile(self):
        rulechecker = Rulechecker()
        is_open = rulechecker.is_open_tile(Tile(3, 4, [Player()]))
        self.assertFalse(is_open)

    def test_is_open_when_adversary_moves_to_player_tile(self):
        rulechecker = Rulechecker()
        is_open = rulechecker.is_open_tile(Tile(3, 4, [Player()]), Adversary)
        self.assertTrue(is_open)

    def test_valid_player_move_2_steps_same_dir(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        is_valid = rulechecker.is_valid_player_move(Tile(3, 4), Tile(4, 5), level)
            
if __name__ == '__main__':
    unittest.main()