import unittest

class TestNumJSON(unittest.TestCase):
    def test_mult(self):
        self.assertEqual(mult([3, 6, 9]), 162, "Should be 162")

if __name__ == '__main__':
    unittest.main()
