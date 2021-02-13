import sys
sys.path.append('../')
import unittest
import random
from room import Room
from tile import Tile
from occupants import Occupant

class TestRoom(unittest.TestCase):
    def test_room_creates_with_all_arguments(self):
        try:
            Room(Tile(3, 4), 5, 6, [Tile(3, 5)])
        except:
            self.fail("Room with all arguments could not be created!")
        
    def test_room_requires_posn_corner(self):
        with self.assertRaises(ValueError):
            Room((3, 4), 6, 5, [Tile(3, 5)])

    def test_room_requires_positive_width(self):
        with self.assertRaises(ValueError):
            Room(Tile(3, 4), -1, 4, [Tile(3, 5)])

    def test_room_requires_positive_height(self):
        with self.assertRaises(ValueError):
            Room(Tile(3, 4), 3, -1, [Tile(3, 5)])
    
    def test_room_equality(self):
        room1 = Room(Tile(3, 4), 5, 6, [Tile(3, 5)])
        room2 = Room(Tile(3, 4), 5, 6, [Tile(3, 5)])
        self.assertTrue(room1 == room2)

    def test_room_printing(self):
        open_tiles = [Tile(4, 5), Tile(4, 6), Tile(4, 7), Tile(5, 6), Tile(5, 7), Tile(6, 7)]
        room1 = Room(Tile(3, 4), 5, 6, [Tile(3, 5)], open_tiles)
        tiles = room1.render()
        print('\n')
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in tiles]))

if __name__ == '__main__':
    unittest.main()