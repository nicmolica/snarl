import sys
sys.path.append('../')
import unittest
import random
from tile import Tile
from occupants import Occupant

class TestPosn(unittest.TestCase):
    def test_tile_can_be_unoccupied(self):
        try:
            t = Tile(0, 0)
            self.assertIsNone(t.occupant)
        except TypeError:
            self.fail("Tile without occupant could not be created!")

    def test_tile_requires_occupant_for_occupant(self):
        non_occupants = [2, 234.234, "sdfsdf", ["list", "with", 4, "elements"]]
        with self.assertRaises(TypeError):
            Tile(0, 0, random.choice(non_occupants))
        
    def test_tile_can_be_created_with_occupant(self):
        try:
            Tile(0, 0, Occupant())
        except:
            self.fail("Tile with occupant could not be created!")

    def test_posn_must_be_nonnegative(self):
        with self.assertRaises(ValueError):
            Tile(-2, 4)

    def test_tile_can_be_origin(self):
        try:
            Tile(0, 0)
        except:
            self.fail("Tile representing origin could not be created!")

    def test_tile_coordinates_stored_correctly(self):
        min_val = 0
        # Choosing a random large number; only needed for testing
        max_val = 9999999
        x = random.randint(min_val, max_val)
        y = random.randint(min_val, max_val)
        p = Tile(x, y)
        self.assertEqual(p.x, x)
        self.assertEqual(p.y, y)

    def test_tile_requires_integers(self):
        non_integers = [0.32, "small cats", [3, 4, 5], {"dictionary": "value"}]
        with self.assertRaises(TypeError):
            Tile(random.choice(non_integers), random.choice(non_integers))

            
if __name__ == '__main__':
    unittest.main()