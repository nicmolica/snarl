import sys
sys.path.append('../')
import unittest
from level import Level
from room import Room
from hallway import Hallway
from tile import Tile
from utils import grid_to_string

class TestLevel(unittest.TestCase):
    def test_rooms_field_rejects_nonrooms(self):
        with self.assertRaises(TypeError):
            Level(["I am not a room", "I am not a room either"], [Hallway([], Tile(1, 0), Tile(10, 0))])
    
    def test_hallways_field_rejects_nonhallways(self):
        with self.assertRaises(TypeError):
            Level([], ["I am not a hallway", "I am not a hallway either"])

    def test_rejects_overlapping_rooms(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)])
        room2 = Room(Tile(9, 9), 10, 10, [Tile(9, 9), Tile(19, 19)])
        with self.assertRaises(ValueError):
            Level([room1, room2], [])

    def test_rejects_overlapping_hallways(self):
        hallway1 = Hallway([], Tile(0, 5), Tile(10, 5))
        hallway2 = Hallway([], Tile(5, 10), Tile(5, 0))
        with self.assertRaises(ValueError):
            Level([], [hallway1, hallway2])
    
    def test_rejects_overlapping_room_and_hallway(self):
        room = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)])
        hallway = Hallway([], Tile(0, 5), Tile(10, 5))
        with self.assertRaises(ValueError):
            Level([room], [hallway])

    def test_rejects_disconnected_hallway(self):
        hallway = Hallway([], Tile(0, 5), Tile(10, 5))
        with self.assertRaises(ValueError):
            Level([], [hallway])

    def test_any_overlaps_accepts_valid_level(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        try:
            Level([room1, room2, room3], [hallway1, hallway2])
        except:
            self.fail("Level.any_overlaps improperly rejected valid level!")

    def test_zero_length_hallway(self):
        try:
            room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
            hallway1 = Hallway([], Tile(3, 4), Tile(3, 5))
            room2 = Room(Tile(0, 5), 5, 5, [Tile(3, 5)])
            level = Level([room1, room2], [hallway1])
        except:
            self.fail("Could not create level with zero-length hallway!")

    def test_level_render(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        expected = "-   -   -   -   -\n|   X   X   X   |\n|   X   X   X   |\n|   X   X   X   |\n" + \
            "-   -   -   D   -\nX   X   X       X\nX               X\nX       X   X   X\n" + \
                "X       X   X   X\nX       X   X   X\nX       X   X   X\nX       X   X   X\n" + \
                    "X       X   X   X\nX       X   X   X\nX       X   X   X\nX       X   X   X\n" + \
                        "X       X   X   X\nX       X   X   X\nX               X\nX   X   X       X\n" + \
                            "-   -   -   D   -\n|   X   X   X   |\n|   X   X   X   |\n" + \
                                "|   X   X   X   |\n|   X   X   X   |\n|   X   X   X   |\n" + \
                                    "|   X   X   X   |\n|   X   X   X   |\n|   X   X   X   |\n" + \
                                        "-   -   -   -   -"
        self.assertEqual(expected, grid_to_string(level.render()))


if __name__ == '__main__':
    unittest.main()