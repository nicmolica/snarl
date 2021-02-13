import sys
sys.path.append('../')
import unittest
import random
from level import Hallway, Posn

class TestHallway(unittest.TestCase):
    def test_hallway_creates_with_empty_waypoints(self):
        try:
            Hallway([], Posn(1, 0), Posn(10, 0))
        except:
            self.fail("Hallway with empty waypoints could not be created!")
    
    def test_hallway_cannot_have_diagonal_segments(self):
        with self.assertRaises(ValueError):
            Hallway([Posn(1, 1), Posn(2, 3)], Posn(1, 0), Posn(2, 4))

    def test_hallway_intersects_perpendicular_hallway(self):
        hall_hor = Hallway([], Posn(0, 5), Posn(11, 5))
        hall_ver = Hallway([], Posn(5, 0), Posn(5, 10))
        self.assertTrue(hall_hor.does_it_intersect(hall_ver))

    def test_hallways_equal(self):
        hall1 = Hallway([Posn(3, 7)], Posn(3, 4), Posn(3, 10))
        hall2 = Hallway([Posn(3, 7)], Posn(3, 4), Posn(3, 10))
        self.assertTrue(hall1 == hall2)

    def test_hallways_not_equal(self):
        hall1 = Hallway([Posn(3, 8)], Posn(3, 4), Posn(3, 10))
        hall2 = Hallway([Posn(3, 7)], Posn(3, 4), Posn(3, 10))
        self.assertTrue(hall1 == hall2)


if __name__ == '__main__':
    unittest.main()