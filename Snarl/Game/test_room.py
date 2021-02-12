import unittest
import random
from level import Room, Tile, Occupant, Posn

class TestRoom(unittest.TestCase):
    def test_room_creates_with_all_arguments(self):
        try:
            Room(Posn(3, 4), 5, 6, [],  [Posn(3, 5)])
        except:
            self.fail("Room with all arguments could not be created!")
        
    def test_room_requires_posn_corner(self):
        with self.assertRaises(TypeError):
            Room((3, 4), 6, 5, [], [Posn(3, 5)])

    def test_room_requires_positive_width(self):
        with self.assertRaises(ValueError):
            Room(Posn(3, 4), -1, 4, [], [Posn(3, 5)])

    def test_room_requires_positive_height(self):
        with self.assertRaises(ValueError):
            Room(Posn(3, 4), 3, -1, [], [Posn(3, 5)])

if __name__ == '__main__':
    unittest.main()