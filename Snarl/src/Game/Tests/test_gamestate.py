import sys
sys.path.append('../')
import unittest
from gamestate import Gamestate
from level import Level
from hallway import Hallway
from room import Room
from tile import Tile
from occupants import Player, Adversary

class TestGamestate(unittest.TestCase):
    def test_gamestate_rejects_too_many_players(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        with self.assertRaises(ValueError):
            Gamestate(level, 5, 10)

    def test_gamestate_rejects_too_few_players(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        with self.assertRaises(ValueError):
            Gamestate(level, 0, 10)

    def test_gamestate_rejects_too_few_adversaries(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        with self.assertRaises(ValueError):
            Gamestate(level, 1, -1)

    def test_move_player(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(2, 2), Tile(3, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        gs = Gamestate(level, 1, 0)
        gs.current_level.add_player(Player("Dumbledore"), Tile(2, 2))
        gs.move_player(Tile(2, 2), Tile(3, 3))
        # player was successfully added to new tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 3)).get_player(), Player("Dumbledore"))
        # player was successfully removed from old tile
        self.assertEqual(gs.current_level.get_tile(Tile(2, 2)).get_player(), None)
    
    def test_move_player_through_doorway(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        gs = Gamestate(level, 1, 0)
        gs.current_level.add_player(Player("Dumbledore"), Tile(3, 4))
        gs.move_player(Tile(3, 4), Tile(3, 6))
        # player was successfully added to new tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 6)).get_player(), Player("Dumbledore"))
        # player was successfully removed from old tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 4)).get_player(), None)

    def test_move_player_in_hallway(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        gs = Gamestate(level, 1, 0)
        gs.current_level.add_player(Player("Dumbledore"), Tile(3, 6))
        gs.move_player(Tile(3, 6), Tile(1, 6))
        # player was successfully added to new tile
        self.assertEqual(gs.current_level.get_tile(Tile(1, 6)).get_player(), Player("Dumbledore"))
        # player was successfully removed from old tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 6)).get_player(), None)

    def test_move_adversary(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(2, 2), Tile(3, 2)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        gs = Gamestate(level, 1, 0)
        gs.current_level.add_adversary(Adversary(), Tile(2, 2))
        gs.move_adversary(Tile(2, 2), Tile(3, 2))
        # player was successfully added to new tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 2)).get_adversary(), Adversary())
        # player was successfully removed from old tile
        self.assertEqual(gs.current_level.get_tile(Tile(2, 2)).get_player(), None)

    def test_move_adversary_through_doorway(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(3, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        gs = Gamestate(level, 1, 0)
        gs.current_level.add_adversary(Adversary(), Tile(3, 3))
        gs.move_adversary(Tile(3, 3), Tile(3, 4))
        # player was successfully added to new tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 4)).get_adversary(), Adversary())
        # player was successfully removed from old tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 3)).get_player(), None)

    def test_move_adversary_through_hallway(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        gs = Gamestate(level, 1, 0)
        gs.current_level.add_adversary(Adversary(), Tile(1, 6))
        gs.move_adversary(Tile(1, 6), Tile(1, 7))
        # player was successfully added to new tile
        self.assertEqual(gs.current_level.get_tile(Tile(1, 7)).get_adversary(), Adversary())
        # player was successfully removed from old tile
        self.assertEqual(gs.current_level.get_tile(Tile(1, 6)).get_player(), None)

if __name__ == '__main__':
    unittest.main()