# This file just calls some things to test the traveller_server
# functionality.
import traveller_server as ts
import unittest

class TestNumJSON(unittest.TestCase):
    def test_emptynetwork(self):
        ts.create_towns([])
        self.assertEqual(0, len(ts.town_networks))

    def test_nopath(self):
        ts.create_towns([{"name": "Town 1", "neighbors": ["Town 2"], "characters": ["Bill"]}, \
            {"name": "Town 2", "neighbors": ["Town 3"], "characters": ["Charlie"]}, \
            {"name": "Town 3", "neighbors": ["Town 4"], "characters": ["April"]}, \
            {"name": "Town 4", "neighbors": [], "characters": ["Alicia"]}])
        self.assertFalse(ts.is_unblocked("Bill", "Town 4"))

    def test_ispath(self):
        ts.create_towns([{"name": "Town 1", "neighbors": ["Town 2"], "characters": ["Bill"]}, \
            {"name": "Town 2", "neighbors": ["Town 3"], "characters": []}, \
            {"name": "Town 3", "neighbors": ["Town 4"], "characters": []}, \
            {"name": "Town 4", "neighbors": [], "characters": []}])
        self.assertTrue(ts.is_unblocked("Bill", "Town 4"))

    def test_createnetwork_nonexistenttowns(self):
        with self.assertRaises(ValueError):
            ts.create_towns([{"name": "Town 1", "neighbors": ["Nonexistent Town"], "characters": []}])

    def test_createnetwork_malformedinputtown(self):
        with self.assertRaises(ValueError):
            ts.create_towns([{"name": "Town 1", "stuff": "missing keys"}])

    def test_isunblocked_towndoesnotexist(self):
        with self.assertRaises(ValueError):
            ts.create_towns([{"name": "Town 1",  "neighbors": [], "characters": ["Bill"]}])
            ts.is_unblocked("Bill", "Nonexistent Town")

if __name__ == '__main__':
    unittest.main()
