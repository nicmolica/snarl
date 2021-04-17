import sys
import unittest
import random
from Snarl.src.Game.room import Room
from Snarl.src.Game.tile import Tile
from Snarl.src.Game.occupants import Occupant, Character, Adversary, LevelExit, LevelKey
from Snarl.src.Game.utils import grid_to_string

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
        
    def test_nonstraddled_room(self):
        room = Room(Tile(2, 2), 5, 5, [Tile(2, 4)], [])
        way1 = Tile(1, 1)
        way2 = Tile(1, 2)
        self.assertFalse(room.is_straddled_by(way1, way2))

    def test_vertical_straddled_room(self):
        room = Room(Tile(2, 2), 5, 5, [Tile(2, 4)], [])
        way1 = Tile(4, 1)
        way2 = Tile(4, 10)
        self.assertTrue(room.is_straddled_by(way1, way2))

    def test_horizontal_straddled_room(self):
        room = Room(Tile(2, 2), 5, 5, [Tile(2, 4)], [])
        way1 = Tile(1, 4)
        way2 = Tile(10, 4)
        self.assertTrue(room.is_straddled_by(way1, way2))

if __name__ == '__main__':
    unittest.main()