import sys
import unittest
import random
from Snarl.src.Game.tile import Tile
from Snarl.src.Game.occupants import Occupant, Character, Adversary, Block

class TestPosn(unittest.TestCase):
    def test_tile_can_be_unoccupied(self):
        try:
            t = Tile(0, 0)
            self.assertListEqual(t.occupants, [])
        except TypeError:
            self.fail("Tile without occupant could not be created!")

    def test_tile_requires_occupant_for_occupant(self):
        non_occupants = [2, 234.234, "sdfsdf", ["list", "with", 4, "elements"]]
        with self.assertRaises(TypeError):
            Tile(0, 0, random.choice(non_occupants))
        
    def test_tile_can_be_created_with_occupants(self):
        try:
            Tile(0, 0, [Occupant(), Occupant()])
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

    def test_add_occupant(self):
        tile = Tile(1, 1)
        player = Character("Nic")
        tile.add_occupant(player)
        self.assertEqual(tile.get_character(), player)
    
    def test_get_player(self):
        tile = Tile(1, 1)
        player = Character("Nic")
        adversary = Adversary()
        tile.add_occupant(player)
        tile.add_occupant(adversary)
        self.assertEqual(tile.get_character(), player)

    def test_get_adversary(self):
        tile = Tile(1, 1)
        player = Character("Nic")
        adversary = Adversary()
        tile.add_occupant(player)
        tile.add_occupant(adversary)
        self.assertEqual(tile.get_adversary(), adversary)

    def test_has_block_true(self):
        tile = Tile(1, 1, [Block()])
        self.assertTrue(tile.has_block())

    def test_has_block_false(self):
        tile = Tile(1, 1)
        self.assertFalse(tile.has_block())

    def test_tile_render_no_occupants_renders_blank(self):
        open_tile = Tile(0, 0)
        self.assertEqual(' ', open_tile.render())

    def test_tile_render_multiple_occupants_renders_first_occupant(self):
        tile = Tile(0, 0, [Character("Character 1"), Adversary()])
        self.assertEqual('P', tile.render())

if __name__ == '__main__':
    unittest.main()