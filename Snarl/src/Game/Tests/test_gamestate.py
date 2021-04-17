import sys
import unittest
from Snarl.src.Game.gamestate import Gamestate
from Snarl.src.Game.level import Level
from Snarl.src.Game.hallway import Hallway
from Snarl.src.Game.room import Room
from Snarl.src.Game.tile import Tile
from Snarl.src.Game.occupants import Character, Adversary, LevelKey, LevelExit, Block

class TestGamestate(unittest.TestCase):
    def test_gamestate_rejects_too_many_players(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(2, 2), Tile(3, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1], Tile(2, 2), Tile(3, 3))
        with self.assertRaises(ValueError):
            Gamestate(level, 5, 10)

    def test_gamestate_rejects_too_few_players(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(2, 2), Tile(3, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1], Tile(2, 2), Tile(3, 3))
        with self.assertRaises(ValueError):
            Gamestate(level, 0, 10)

    def test_gamestate_rejects_too_few_adversaries(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(2, 2), Tile(3, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1], Tile(2, 2), Tile(3, 3))
        with self.assertRaises(ValueError):
            Gamestate(level, 1, -1)

    def test_move_player(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(2, 2), Tile(3, 3), Tile(1, 1), Tile(1, 2)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1], Tile(1, 1), Tile(1, 2))
        gs = Gamestate(level, 1, 0)
        character = Character("Dumbledore")
        gs.add_character(character, Tile(2, 2))
        gs.move(character, Tile(3, 3))
        # player was successfully added to new tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 3)).get_character(), character)
        # player was successfully removed from old tile
        self.assertEqual(gs.current_level.get_tile(Tile(2, 2)).get_character(), None)
    
    def test_move_player_through_doorway(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        gs = Gamestate(level, 1, 0)
        character = Character("Dumbledore")
        gs.current_level.add_character(character, Tile(3, 4))
        gs.move(character, Tile(3, 6))
        # player was successfully added to new tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 6)).get_character(), character)
        # player was successfully removed from old tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 4)).get_character(), None)

    def test_move_player_in_hallway(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        gs = Gamestate(level, 1, 0)
        character = Character("Dumbledore")
        gs.current_level.add_character(character, Tile(3, 6))
        gs.move(character, Tile(1, 6))
        # player was successfully added to new tile
        self.assertEqual(gs.current_level.get_tile(Tile(1, 6)).get_character(), character)
        # player was successfully removed from old tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 6)).get_character(), None)

    def test_move_adversary(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(2, 2), Tile(3, 2), Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        gs = Gamestate(level, 1, 0)
        adv = Adversary()
        gs.current_level.add_adversary(adv, Tile(2, 2))
        gs.move(adv, Tile(3, 2))
        # player was successfully added to new tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 2)).get_adversary(), Adversary())
        # player was successfully removed from old tile
        self.assertEqual(gs.current_level.get_tile(Tile(2, 2)).get_character(), None)

    def test_move_adversary_through_doorway(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(3, 3), Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        gs = Gamestate(level, 1, 0)
        adv = Adversary()
        gs.current_level.add_adversary(adv, Tile(3, 3))
        gs.move(adv, Tile(3, 4))
        # player was successfully added to new tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 4)).get_adversary(), Adversary())
        # player was successfully removed from old tile
        self.assertEqual(gs.current_level.get_tile(Tile(3, 3)).get_character(), None)

    def test_move_adversary_through_hallway(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        gs = Gamestate(level, 1, 0)
        adv = Adversary()
        gs.current_level.add_adversary(adv, Tile(1, 6))
        gs.move(adv, Tile(1, 7))
        # player was successfully added to new tile
        self.assertEqual(gs.current_level.get_tile(Tile(1, 7)).get_adversary(), Adversary())
        # player was successfully removed from old tile
        self.assertEqual(gs.current_level.get_tile(Tile(1, 6)).get_character(), None)

    def test_get_tiles_gets_current_level_tiles(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        gs = Gamestate(level, 1, 0)
        gs_tiles = gs.get_tiles()
        level_tiles = level.get_tiles()
        self.assertEqual(level_tiles, gs_tiles)

    def test_get_tiles_range_gets_correct_tiles(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        gs = Gamestate(level, 1, 0)
        tiles = gs.get_tiles_range(Tile(0, 0), Tile(4, 4))
        flattened_tiles = [tile for row in tiles for tile in row]
        tiles_in_x_range = all([tile.x >= 0 and tile.x <= 4 for tile in flattened_tiles])
        tiles_in_y_range = all([tile.y >= 0 and tile.y <= 4 for tile in flattened_tiles])
        self.assertTrue(tiles_in_x_range)
        self.assertTrue(tiles_in_y_range)

    def test_get_character_surroundings_gets_character_tiles_range(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
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
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        adv = Adversary()
        gs = Gamestate(level, 1, 0)
        gs.add_adversary(adv, Tile(0, 0))

    def test_render_renders_current_level(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        gs = Gamestate(level, 1, 0)
        render_gs = gs.render()
        render_lvl = level.render()
        self.assertEqual(render_gs, render_lvl)

    def test_next_level(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level1 = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))

        room1_1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(2, 2), Tile(3, 3), Tile(1, 1), Tile(1, 2)])
        hallway1_1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2_1 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level2 = Level([room1_1, room2_1], [hallway1_1], Tile(1, 1), Tile(1, 2))

        gs = Gamestate(level1, 1, 0, [level2])
        gs.next_level()
        self.assertEqual(level2, gs.current_level) # new level is level2
        self.assertEqual(1, gs.num_levels_completed) # num_levels_completed was incremented properly
        self.assertFalse(bool(gs.levels)) # list of levels is empty now

    def test_is_current_level_completed(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level1 = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        gs = Gamestate(level1, 1, 0)

        self.assertTrue(gs.is_current_level_completed())

    def test_get_top_left_room(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level1 = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        gs = Gamestate(level1, 1, 0)

        self.assertEqual(room1, gs.get_top_left_room())

    def test_all_players_expelled(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level1 = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        gs = Gamestate(level1, 1, 0)

        self.assertTrue(gs.all_players_expelled())
        character = Character("Dumbledore")
        gs.add_character(character, Tile(2, 2))
        self.assertFalse(gs.all_players_expelled())

    def test_is_character_expelled(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level1 = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        gs = Gamestate(level1, 1, 0)
        character = Character("Dumbledore")
        gs.add_character(character, Tile(2, 2))

        self.assertFalse(gs.is_character_expelled(character))

    def test_game_complete(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level1 = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        gs = Gamestate(level1, 1, 0)

        self.assertFalse(gs.game_complete())
        gs.current_level.is_completed = True
        self.assertTrue(gs.game_complete())

    def test_is_current_level_unlocked(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level1 = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        gs = Gamestate(level1, 1, 0)

        self.assertFalse(gs.is_current_level_unlocked())
        gs.current_level.level_exit_unlocked = True
        self.assertTrue(gs.is_current_level_unlocked())

    def test_get_completed_characters(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level1 = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        gs = Gamestate(level1, 1, 0)

        self.assertFalse(bool(gs.get_completed_characters()))
        list_of_characters = [Character("Dumbledore"), Character("Heidi Klum")]
        gs.current_level.completed_characters = list_of_characters
        self.assertEqual(list_of_characters, gs.get_completed_characters())

    def test_objects_in_range(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level1 = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        gs = Gamestate(level1, 1, 0)
        key_tile = Tile(1, 2)
        key_tile.add_occupant(LevelKey())
        exit_tile = Tile(2, 3)
        exit_tile.add_occupant(LevelExit())

        self.assertEqual([(key_tile, LevelKey())], gs.objects_in_range(Tile(1, 1), Tile(1, 3)))
        self.assertEqual([(key_tile, LevelKey()), (exit_tile, LevelExit())], gs.objects_in_range(Tile(0, 0), Tile(5, 5)))

    def test_actors_in_range(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level1 = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        gs = Gamestate(level1, 1, 0)
        dumbledore = Character("Dumbledore")
        gs.get_tile(Tile(3, 3)).add_occupant(dumbledore)
        dumbledore_tile = Tile(3, 3)
        dumbledore_tile.add_occupant(Block())
        dumbledore_tile.add_occupant(dumbledore)

        self.assertEqual([(dumbledore_tile, dumbledore)], gs.actors_in_range(Tile(0, 0), Tile(3, 3)))

    def test_get_level_unlocked_by(self):
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 2), Tile(2, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level1 = Level([room1, room2], [hallway1], Tile(1, 2), Tile(2, 3))
        gs = Gamestate(level1, 1, 0)
        dumbledore = Character("Dumbledore")
        gs.current_level.level_exit_unlocked = True
        gs.current_level.unlocked_by = dumbledore

        self.assertEqual(dumbledore, gs.get_level_unlocked_by())

if __name__ == '__main__':
    unittest.main()