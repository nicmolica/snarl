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

    def test_room_open_tiles_around_0_radius_fails(self):
        room1 = Room(Tile(0, 0), 5, 6, [Tile(0, 3)])
        with self.assertRaises(ValueError):
            room1.open_tiles_around(Tile(1, 1), 0)

    def test_room_open_tiles_around_outside_room_fails(self):
        room1 = Room(Tile(0, 0), 5, 6, [Tile(0, 3)])
        with self.assertRaises(RuntimeError):
            room1.open_tiles_around(Tile(100, 100), 2)
    
    def test_room_open_tiles_around_1_radius_does_not_return_self(self):
        player = Character("Character 1")
        enemy1 = Adversary()
        enemy2 = Adversary()
        level_key = LevelKey()
        level_exit = LevelExit()
        open_tiles = [Tile(4, 5, player), Tile(4, 6, level_key), Tile(4, 7, enemy1), \
            Tile(5, 6), Tile(5, 7, enemy2), Tile(6, 7, level_exit)]
        room = Room(Tile(3, 4), 5, 6, [Tile(3, 5)], open_tiles)
        tiles = room.render()
        open_tiles_around = room.open_tiles_around(Tile(5, 6), 1)
        self.assertNotIn((5, 6), [(tile.x, tile.y) for tile in open_tiles_around])

    def test_room_open_tiles_around_1_radius_returns_correct_tiles(self):
        player = Character("Character 1")
        enemy1 = Adversary()
        enemy2 = Adversary()
        level_key = LevelKey()
        level_exit = LevelExit()
        open_tiles = [Tile(4, 5, player), Tile(4, 6, level_key), Tile(4, 7, enemy1), \
            Tile(5, 6), Tile(5, 7, enemy2), Tile(6, 7, level_exit)]
        room = Room(Tile(3, 4), 5, 6, [Tile(3, 5)], open_tiles)
        tiles = room.render()
        open_tiles_around = room.open_tiles_around(Tile(5, 6), 1)
        coords = [(tile.x, tile.y) for tile in open_tiles_around]
        self.assertIn((4, 6), coords)
        self.assertIn((5, 7), coords)

    def test_room_open_tiles_around_radius_returns_door(self):
        player = Character("Character 1")
        enemy1 = Adversary()
        enemy2 = Adversary()
        level_key = LevelKey()
        level_exit = LevelExit()
        open_tiles = [Tile(4, 5, player), Tile(4, 6, level_key), Tile(4, 7, enemy1), \
            Tile(5, 6), Tile(5, 7, enemy2), Tile(6, 7, level_exit)]
        room = Room(Tile(3, 4), 5, 6, [Tile(3, 5)], open_tiles)
        tiles = room.render()
        open_tiles_around = room.open_tiles_around(Tile(4, 5), 1)
        coords = [(tile.x, tile.y) for tile in open_tiles_around]
        self.assertIn((3, 5), coords)

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

    def test_room_rendering(self):
        player = Character("Character 1")
        enemy1 = Adversary()
        enemy2 = Adversary()
        level_key = LevelKey()
        level_exit = LevelExit()
        open_tiles = [Tile(4, 5, player), Tile(4, 6, level_key), Tile(4, 7, enemy1), \
            Tile(5, 6), Tile(5, 7, enemy2), Tile(6, 7, level_exit)]
        room1 = Room(Tile(3, 4), 5, 6, [Tile(3, 5)], open_tiles)
        tiles = room1.render()
        expected_string = "-   -   -   -   -" + "\nD   P   X   X   |" + "\n|   K       X   |" \
            + "\n|   A   A   E   |" + "\n|   X   X   X   |" + "\n-   -   -   -   -"
        self.assertEqual(expected_string, grid_to_string(tiles))

if __name__ == '__main__':
    unittest.main()