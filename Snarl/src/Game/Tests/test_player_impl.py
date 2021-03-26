from Snarl.src.Game.player_impl import PlayerImpl
import unittest
import json

class TestPlayerImpl(unittest.TestCase):
    def test_player_name_must_be_string(self):
        with self.assertRaises(TypeError):
            PlayerImpl({ "I am": "not a string"}, "Character Name")
    
    def test_character_name_must_be_string(self):
        with self.assertRaises(TypeError):
            PlayerImpl("Player Name", {"not": "string"})
    
    def test_player_inits_to_not_expelled(self):
        p = PlayerImpl("Player Name", "Character Name")
        self.assertFalse(p.expelled)
    
    def test_player_surroundings_init_to_none(self):
        p = PlayerImpl("Player Name", "Character Name")
        self.assertIsNone(p.surroundings)

    def test_players_with_both_names_equal_are_equal(self):
        p1 = PlayerImpl("Player Name", "Character Name")
        p2 = PlayerImpl("Player Name", "Character Name")
        self.assertEqual(p1, p2)
    
    def test_players_with_diff_player_name_not_equal(self):
        p1 = PlayerImpl("Player Name", "Character Name")
        p2 = PlayerImpl("Other Player Name", "Character Name")
        self.assertNotEqual(p1, p2)
    
    def test_players_with_diff_character_name_not_equal(self):
        p1 = PlayerImpl("Player Name", "Character Name")
        p2 = PlayerImpl("Player Name", "Other Character Name")
        self.assertNotEqual(p1, p2)

    def test_update_surroundings_alters_surroundings_field(self):
        p = PlayerImpl("Player Name", "Character Name")
        p.notify("dummy surroundings")
        self.assertIsNotNone(p.surroundings)
    
    def test_expel_alters_expel_field(self):
        p = PlayerImpl("Player Name", "Character Name")
        p.expel()
        self.assertTrue(p.expelled)
    
    def test_move_requires_array_input(self):
        p = PlayerImpl("Player Name", "Character Name")
        with self.assertRaises(json.JSONDecodeError):
            p._move_with_input(lambda : "Not an array")
    
    def test_move_correctly_parses_input_to_tile(self):
        p = PlayerImpl("Player Name", "Character Name")
        tile = p._move_with_input(lambda : "[2, 3]")
        self.assertEqual(tile.x, 2)
        self.assertEqual(tile.y, 3)
    
    def test_move_raises_error_if_input_too_long(self):
        p = PlayerImpl("Player Name", "Character Name")
        with self.assertRaises(RuntimeError):
            tile = p._move_with_input(lambda : "[2, 3, 6]")

if __name__ == '__main__':
    unittest.main()