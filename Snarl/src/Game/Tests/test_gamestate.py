import sys
import unittest
from Snarl.src.Game.gamestate import Gamestate
from Snarl.src.Game.level import Level
from Snarl.src.Game.hallway import Hallway
from Snarl.src.Game.room import Room
from Snarl.src.Game.tile import Tile
from Snarl.src.Game.occupants import Character, Adversary

class TestGamestate(unittest.TestCase):
    def test_gamestate_rejects_too_many_players(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        with self.assertRaises(ValueError):
            Gamestate(level, 5, 10)

    def test_gamestate_rejects_too_few_players(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        with self.assertRaises(ValueError):
            Gamestate(level, 0, 10)

    def test_gamestate_rejects_too_few_adversaries(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        with self.assertRaises(ValueError):
            Gamestate(level, 1, -1)

    def test_move_player(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(2, 2), Tile(3, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        gs = Gamestate(level, 1, 0)
        character = Character("Dumbledore")
        gs.current_level.add_character(character, Tile(2, 2))
        gs.move(character, Tile(3, 3))
        # player was successfully added to new tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 3)).get_character(), character)
        # player was successfully removed from old tile
        self.assertEqual(gs.current_level.get_tile(Tile(2, 2)).get_character(), None)
    
    def test_move_player_through_doorway(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        gs = Gamestate(level, 1, 0)
        character = Character("Dumbledore")
        gs.current_level.add_character(character, Tile(3, 4))
        gs.move(character, Tile(3, 6))
        # player was successfully added to new tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 6)).get_character(), character)
        # player was successfully removed from old tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 4)).get_character(), None)

    def test_move_player_in_hallway(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        gs = Gamestate(level, 1, 0)
        character = Character("Dumbledore")
        gs.current_level.add_character(character, Tile(3, 6))
        gs.move(character, Tile(1, 6))
        # player was successfully added to new tile
        self.assertEqual(gs.current_level.get_tile(Tile(1, 6)).get_character(), character)
        # player was successfully removed from old tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 6)).get_character(), None)

    def test_move_adversary(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(2, 2), Tile(3, 2)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        gs = Gamestate(level, 1, 0)
        adv = Adversary()
        gs.current_level.add_adversary(adv, Tile(2, 2))
        gs.move(adv, Tile(3, 2))
        # player was successfully added to new tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 2)).get_adversary(), Adversary())
        # player was successfully removed from old tile
        self.assertEqual(gs.current_level.get_tile(Tile(2, 2)).get_character(), None)

    def test_move_adversary_through_doorway(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(3, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        gs = Gamestate(level, 1, 0)
        adv = Adversary()
        gs.current_level.add_adversary(adv, Tile(3, 3))
        gs.move(adv, Tile(3, 4))
        # player was successfully added to new tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 4)).get_adversary(), Adversary())
        # player was successfully removed from old tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 3)).get_character(), None)

    def test_move_adversary_through_hallway(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        gs = Gamestate(level, 1, 0)
        adv = Adversary()
        gs.current_level.add_adversary(adv, Tile(1, 6))
        gs.move(adv, Tile(1, 7))
        # player was successfully added to new tile
        self.assertEqual(gs.current_level.get_tile(Tile(1, 7)).get_adversary(), Adversary())
        # player was successfully removed from old tile
        self.assertEqual(gs.current_level.get_tile(Tile(1, 6)).get_character(), None)

    def test_complete_level_marks_level_as_complete(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        gs = Gamestate(level, 1, 0)
        gs.complete_level(False)
        self.assertTrue(gs.current_level.is_completed)

    def test_get_tiles_gets_current_level_tiles(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        gs = Gamestate(level, 1, 0)
        gs_tiles = gs.get_tiles()
        level_tiles = level.get_tiles()
        self.assertEqual(level_tiles, gs_tiles)

    def test_get_tiles_range_gets_correct_tiles(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        gs = Gamestate(level, 1, 0)
        tiles = gs.get_tiles_range(Tile(0, 0), Tile(4, 4))
        flattened_tiles = [tile for row in tiles for tile in row]
        tiles_in_x_range = all([tile.x >= 0 and tile.x <= 4 for tile in flattened_tiles])
        tiles_in_y_range = all([tile.y >= 0 and tile.y <= 4 for tile in flattened_tiles])
        self.assertTrue(tiles_in_x_range)
        self.assertTrue(tiles_in_y_range)

    def test_get_character_surroundings_gets_character_tiles_range(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        character = Character("Tulkas Astaldo")
        level.add_character(character, Tile(0, 0))
        gs = Gamestate(level, 1, 0)
        tiles = gs.get_character_surroundings(character, 2)
        flattened_tiles = [tile for row in tiles for tile in row]
        tiles_in_x_range = all([tile.x >= 0 and tile.x <= 2 for tile in flattened_tiles])
        tiles_in_y_range = all([tile.y >= 0 and tile.y <= 2 for tile in flattened_tiles])
        self.assertTrue(tiles_in_x_range)
        self.assertTrue(tiles_in_y_range)

    def test_add_adversary_adds_adversary(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        adv = Adversary()
        gs = Gamestate(level, 1, 0)
        gs.add_adversary(adv, Tile(0, 0))

    def test_render_renders_current_level(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        gs = Gamestate(level, 1, 0)
        render_gs = gs.render()
        render_lvl = level.render()
        self.assertEqual(render_gs, render_lvl)

if __name__ == '__main__':
    unittest.main()