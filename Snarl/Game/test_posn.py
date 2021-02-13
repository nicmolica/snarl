import unittest
import random
from level import Posn

class TestPosn(unittest.TestCase):
    def test_posn_must_be_nonnegative(self):
        with self.assertRaises(ValueError):
            Posn(-2, 4)

    def test_posn_can_be_origin(self):
        try:
            Posn(0, 0)
        except:
            self.fail("Posn representing origin could not be created!")

    def test_posn_coordinates_stored_correctly(self):
        min_val = 0
        # Choosing a random large number; only needed for testing
        max_val = 9999999
        x = random.randint(min_val, max_val)
        y = random.randint(min_val, max_val)
        p = Posn(x, y)
        self.assertEqual(p.x, x)
        self.assertEqual(p.y, y)

    def test_posn_requires_integers(self):
        non_integers = [0.32, "small cats", [3, 4, 5], {"dictionary": "value"}]
        with self.assertRaises(TypeError):
            Posn(random.choice(non_integers), random.choice(non_integers))
            
if __name__ == '__main__':
    unittest.main()