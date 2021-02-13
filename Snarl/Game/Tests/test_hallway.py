import sys
sys.path.append('../')
import unittest
import random
from tile import Tile
from hallway import Hallway

class TestHallway(unittest.TestCase):
    def test_hallway_creates_with_empty_waypoints(self):
        try:
            Hallway([], Tile(1, 0), Tile(10, 0))
        except:
            self.fail("Hallway with empty waypoints could not be created!")
    
    def test_hallway_cannot_have_diagonal_segments(self):
        with self.assertRaises(ValueError):
            Hallway([Tile(1, 1), Tile(2, 3)], Tile(1, 0), Tile(2, 4))

    def test_hallway_intersects_perpendicular_hallway(self):
        hall_hor = Hallway([], Tile(0, 5), Tile(10, 5))
        hall_ver = Hallway([], Tile(5, 0), Tile(5, 10))
        self.assertTrue(hall_ver.does_it_intersect(hall_hor))
    
    def test_hallway_intersects_parallel_hallway_with_same_coord(self):
        hall_first = Hallway([], Tile(0, 5), Tile(10, 5))
        hall_second = Hallway([], Tile(2, 5), Tile(12, 5))
        self.assertTrue(hall_first.does_it_intersect(hall_second))

    def test_hallway_does_not_intersect_disjoint_hallway(self):
        hall_first = Hallway([], Tile(0, 5), Tile(10, 5))
        hall_second = Hallway([], Tile(11, 5), Tile(22, 5))
        self.assertFalse(hall_first.does_it_intersect(hall_second))

    def test_hallways_equal(self):
        hall1 = Hallway([Tile(3, 7)], Tile(3, 4), Tile(3, 10))
        hall2 = Hallway([Tile(3, 7)], Tile(3, 4), Tile(3, 10))
        self.assertTrue(hall1 == hall2)

    def test_hallways_not_equal(self):
        hall1 = Hallway([Tile(3, 8)], Tile(3, 4), Tile(3, 10))
        hall2 = Hallway([Tile(3, 7)], Tile(3, 4), Tile(3, 10))
        self.assertFalse(hall1 == hall2)

if __name__ == '__main__':
    unittest.main()