from Snarl.src.Game.player_impl import Player
import unittest
import json

class OutTrace:
    def write(self, output):
        self.output = output

class TestPlayerImpl(unittest.TestCase):
    def test_player_name_must_be_string(self):
        with self.assertRaises(TypeError):
            Player({ "I am": "not a string"}, "Character Name")
    
    def test_character_name_must_be_string(self):
        with self.assertRaises(TypeError):
            Player("Player Name", {"not": "string"})
    
    def test_player_inits_to_not_expelled(self):
        p = Player("Player Name", "Character Name")
        self.assertFalse(p.expelled)
    
    def test_player_surroundings_init_to_none(self):
        p = Player("Player Name", "Character Name")
        self.assertIsNone(p.surroundings)

    def test_players_with_both_names_equal_are_equal(self):
        p1 = Player("Player Name", "Character Name")
        p2 = Player("Player Name", "Character Name")
        self.assertEqual(p1, p2)
    
    def test_players_with_diff_player_name_not_equal(self):
        p1 = Player("Player Name", "Character Name")
        p2 = Player("Other Player Name", "Character Name")
        self.assertNotEqual(p1, p2)
    
    def test_players_with_diff_character_name_not_equal(self):
        p1 = Player("Player Name", "Character Name")
        p2 = Player("Player Name", "Other Character Name")
        self.assertNotEqual(p1, p2)

    def test_update_surroundings_alters_surroundings_field(self):
        out = OutTrace()
        p = Player("Player Name", "Character Name", out)
        p.notify({"dummy": "surroundings"})
        self.assertIsNotNone(out.output)
    
    def test_expel_alters_expel_field(self):
        p = Player("Player Name", "Character Name")
        p.expel()
        self.assertTrue(p.expelled)
    
    def test_move_requires_array_input(self):
        p = Player("Player Name", "Character Name", input_func = lambda : "Not an array")
        with self.assertRaises(json.JSONDecodeError):
            p._determine_move()
    
    def test_move_correctly_parses_input_to_tile(self):
        p = Player("Player Name", "Character Name", input_func = lambda : "[2, 3]")
        tile = p._determine_move()
        self.assertEqual(tile.x, 2)
        self.assertEqual(tile.y, 3)
    
    def test_move_raises_error_if_input_too_long(self):
        p = Player("Player Name", "Character Name", input_func = lambda : "[2, 3, 6]")
        with self.assertRaises(RuntimeError):
            tile = p._determine_move()

if __name__ == '__main__':
    unittest.main()