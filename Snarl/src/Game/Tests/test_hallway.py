import sys
import unittest
import random
from Snarl.src.Game.tile import Tile
from Snarl.src.Game.hallway import Hallway

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

    def test_assign_start_end_waypoints_vertical(self):
        hall = Hallway([], Tile(5, 5), Tile(5, 10))
        self.assertEqual(hall.waypoints[0], Tile(5, 6))
        self.assertEqual(hall.waypoints[1], Tile(5, 9))

    def test_assign_start_end_waypoints_horizontal(self):
        hall = Hallway([], Tile(5, 5), Tile(10, 5))
        self.assertEqual(hall.waypoints[0], Tile(6, 5))
        self.assertEqual(hall.waypoints[1], Tile(9, 5))

    def test_zero_length_hallway(self):
        hall = Hallway([], Tile(5, 5), Tile(5, 6))
        self.assertEqual(len(hall.waypoints), 0)

    def test_constructor_errors_when_waypoints_not_a_list(self):
        with self.assertRaises(TypeError):
            Hallway("small cats", Tile(3, 4), Tile(2, 34))

    def test_constructor_errors_when_waypoints_not_a_list_of_tiles(self):
        with self.assertRaises(TypeError):
            Hallway(["list", "of", "strings"], Tile(3, 4), Tile(2, 34))

    def test_constructor_errors_when_doors_not_tiles(self):
        with self.assertRaises(TypeError):
            Hallway([], Tile(1, 2), "Glaurung the Golden")

    def test_constructor_errors_when_waypoints_in_zero_length_hallway(self):
        with self.assertRaises(ValueError):
            Hallway([Tile(0, 1)], Tile(0, 0), Tile(0, 1))

    def test_constructor_errors_when_adjacent_doors_do_not_form_segment(self):
        with self.assertRaises(ValueError):
            Hallway([], Tile(0, 0), Tile(1, 1))

    def test_contains_contains_tiles_it_contains(self):
        h = Hallway([], Tile(0, 0), Tile(10, 0))
        self.assertTrue(h.contains(Tile(5, 0)))

    def test_contains_does_not_contain_tiles_outside_hallway(self):
        h = Hallway([], Tile(0, 0), Tile(10, 0))
        self.assertFalse(h.contains(Tile(0, 123)))

if __name__ == '__main__':
    unittest.main()