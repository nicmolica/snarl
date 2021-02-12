import unittest
import random
from level import Tile, Occupant

class TestPosn(unittest.TestCase):
    def test_tile_can_be_unoccupied(self):
        try:
            t = Tile()
            self.assertIsNone(t.occupant)
        except TypeError:
            self.fail("Tile without occupant could not be created!")

    def test_tile_requires_occupant_for_occupant(self):
        non_occupants = [2, 234.234, "sdfsdf", ["list", "with", 4, "elements"]]
        with self.assertRaises(TypeError):
            Tile(random.choice(non_occupants))
        
    def test_tile_can_be_created_with_occupant(self):
        try:
            Tile(Occupant())
        except:
            self.fail("Tile with occupant could not be created!")
            
if __name__ == '__main__':
    unittest.main()