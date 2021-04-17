import sys
import unittest
from Snarl.src.Game.level import Level
from Snarl.src.Game.room import Room
from Snarl.src.Game.hallway import Hallway
from Snarl.src.Game.tile import Tile
from Snarl.src.Game.occupants import Character, Adversary, LevelKey, LevelExit, Ghost
from Snarl.src.Game.utils import grid_to_string

class TestLevel(unittest.TestCase):
    def test_rooms_field_rejects_nonrooms(self):
        with self.assertRaises(TypeError):
            Level(["I am not a room", "I am not a room either"], [Hallway([], Tile(1, 0), Tile(10, 0))], Tile(1, 1), Tile(2, 2))
    
    def test_hallways_field_rejects_nonhallways(self):
        with self.assertRaises(TypeError):
            Level([], ["I am not a hallway", "I am not a hallway either"], Tile(1, 1), Tile(2, 2))

    def test_rejects_overlapping_rooms(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)])
        room2 = Room(Tile(9, 9), 10, 10, [Tile(9, 9), Tile(19, 19)])
        with self.assertRaises(ValueError):
            Level([room1, room2], [], Tile(1, 1), Tile(2, 2))

    def test_rejects_overlapping_hallways(self):
        hallway1 = Hallway([], Tile(0, 5), Tile(10, 5))
        hallway2 = Hallway([], Tile(5, 10), Tile(5, 0))
        with self.assertRaises(ValueError):
            Level([], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
    
    def test_rejects_overlapping_room_and_hallway(self):
        room = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(1, 1), Tile(2, 2)])
        hallway = Hallway([], Tile(0, 5), Tile(10, 5))
        with self.assertRaises(ValueError):
            Level([room], [hallway], Tile(1, 1), Tile(2, 2))

    def test_rejects_disconnected_hallway(self):
        hallway = Hallway([], Tile(0, 5), Tile(10, 5))
        with self.assertRaises(ValueError):
            Level([], [hallway], Tile(1, 1), Tile(2, 2))

    def test_any_overlaps_accepts_valid_level(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        try:
            Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        except:
            self.fail("Level.any_overlaps improperly rejected valid level!")

    def test_zero_length_hallway(self):
        try:
            room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)], [Tile(1, 1), Tile(2, 2)])
            hallway1 = Hallway([], Tile(3, 4), Tile(3, 5))
            room2 = Room(Tile(0, 5), 5, 5, [Tile(3, 5)])
            level = Level([room1, room2], [hallway1], Tile(1, 1), Tile(2, 2))
        except:
            self.fail("Could not create level with zero-length hallway!")

    def test_add_player(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        level.add_character(Character("Nic"), Tile(5, 5))
        self.assertEqual(level.get_tile(Tile(5, 5)).get_character(), Character("Nic"))

    def test_add_adversary(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        level.add_adversary(Adversary(), Tile(5, 5))
        self.assertEqual(level.get_tile(Tile(5, 5)).get_adversary(), Adversary())

    def test_locate_occupant_adversary(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        level.add_adversary(Adversary(), Tile(5, 5))
        self.assertEqual(level.locate_entity(Adversary()), level.get_tile(Tile(5, 5)))

    def test_locate_occupant_player(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        level.add_character(Character("Nic"), Tile(5, 5))
        self.assertEqual(level.locate_entity(Character("Nic")), level.get_tile(Tile(5, 5)))

    def test_move_occupant_player(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        level.add_character(Character("Nic"), Tile(5, 5))
        level.move_occupant(Character("Nic"), Tile(7, 5))
        # player is now in correct position
        self.assertEqual(level.get_tile(Tile(7, 5)).get_character(), Character("Nic"))
        # player is removed from old position
        self.assertEqual(level.get_tile(Tile(5, 5)).get_character(), None)

    def test_move_occupant_adversary(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        level.add_adversary(Adversary(), Tile(5, 5))
        level.move_occupant(Adversary(), Tile(7, 5))
        # player is now in correct position
        self.assertEqual(level.get_tile(Tile(7, 5)).get_adversary(), Adversary())
        # player is removed from old position
        self.assertEqual(level.get_tile(Tile(5, 5)).get_adversary(), None)

    def test_interact_with_key(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        level.add_character(Character("Nic"), Tile(5, 5))
        level.get_tile(Tile(7, 5)).add_occupant(LevelKey())
        # exit is locked prior to interaction
        self.assertFalse(level.level_exit_unlocked)
        level.move_occupant(Character("Nic"), Tile(7, 5))
        # exit is unlocked after interaction
        self.assertTrue(level.level_exit_unlocked)

    def test_interact_with_exit(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(8, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        level.add_character(Character("Nic"), Tile(5, 5))
        level.get_tile(Tile(7, 5)).add_occupant(LevelKey())
        level.get_tile(Tile(8, 5)).add_occupant(LevelExit())
        level.move_occupant(Character("Nic"), Tile(7, 5))
        # level is not completed prior to reaching exit
        self.assertEqual(len(level.completed_characters), 0)
        self.assertEqual(len(level.characters), 1)
        level.move_occupant(Character("Nic"), Tile(8, 5))
        # level is completed after reaching exit
        self.assertEqual(len(level.completed_characters), 1)
        self.assertEqual(len(level.characters), 0)

    def test_interact_with_adversary(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(8, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        level.add_character(Character("Nic"), Tile(5, 5))
        level.add_adversary(Adversary(), Tile(7, 5))
        level.get_tile(Tile(7, 5)).add_occupant(LevelKey())
        level.get_tile(Tile(8, 5)).add_occupant(LevelExit())
        level.move_occupant(Character("Nic"), Tile(7, 5))
        self.assertEqual(len(level.characters), 0)
        self.assertFalse(level.level_exit_unlocked)

    def test_cannot_create_level_with_key_on_door(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(8, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        with self.assertRaises(RuntimeError):
            level = Level([room1, room2, room3], [hallway1, hallway2], Tile(3, 9), Tile(2, 2))

    def test_cannot_create_level_with_exit_on_door(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(8, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        with self.assertRaises(RuntimeError):
            level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(9, 5))
    
    def test_cannot_create_level_with_key_and_exit_on_same_tile(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(8, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        with self.assertRaises(RuntimeError):
            level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(1, 1))

    def test_level_cannot_move_non_entities(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(8, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        with self.assertRaises(RuntimeError):
            level.move_occupant(LevelKey(), Tile(2, 2))

    def test_ghost_on_block_interacts_with_teleportation(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(8, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        g = Ghost()
        blocked_tile = Tile(10, 10)
        level.add_adversary(g, blocked_tile)
        level.interact(blocked_tile)
        teleported_location = level.locate_entity(g)
        self.assertFalse(blocked_tile.coordinates_equal(teleported_location))

    def test_can_only_set_level_exit_status_to_bool(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(8, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        with self.assertRaises(TypeError):
            level.set_level_exit_status("This is not a boolean")

    def test_set_level_exit_status_changes_level_exit_lock_status(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(8, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        level.set_level_exit_status(True)
        self.assertTrue(level.level_exit_unlocked)
    
    def test_cannot_add_duplicate_character(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(8, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        character = Character("This is a character")
        location = Tile(5, 5)
        level.add_character(character, location)
        with self.assertRaises(ValueError):
            level.add_character(character, location)

    def test_top_left_room_gets_top_left_room(self):
        origin = Tile(0, 0)
        room1 = Room(origin, 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(8, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        top_left_room = level.get_top_left_room()
        self.assertTrue(origin.coordinates_equal(top_left_room.position))

    def test_get_rooms_from_hallway_gets_correct_rooms(self):
        origin = Tile(0, 0)
        room1 = Room(origin, 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(8, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        down20 = Tile(0, 20)
        room2 = Room(down20, 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        room_posns = level._get_rooms_from_hallway(hallway1)
        self.assertEqual(room_posns, [[origin.y, origin.x], [down20.y, down20.x]])

    def test_get_rooms_from_tile_in_room_gets_adjacent_rooms_when_tile_is_in_room(self):
        origin = Tile(0, 0)
        room1 = Room(origin, 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(8, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        down20 = Tile(0, 20)
        room2 = Room(down20, 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        across18 = Tile(18, 0)
        room3 = Room(across18, 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        rooms = level._get_rooms_from_tile_in_room(Tile(1, 1))
        self.assertEqual([[down20.y, down20.x], [across18.y, across18.x]], rooms)

    def test_get_rooms_from_tile_in_room_gets_adjacent_rooms_when_tile_is_in_hallway(self):
        origin = Tile(0, 0)
        room1 = Room(origin, 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(8, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        down20 = Tile(0, 20)
        room2 = Room(down20, 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        across18 = Tile(18, 0)
        room3 = Room(across18, 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        rooms = level._get_rooms_from_tile_in_hallway(Tile(12, 5))
        self.assertEqual([[origin.y, origin.x], [across18.y, across18.x]], rooms)
    
    def test_get_reachable_rooms_returns_rooms_when_tile_in_hallway(self):
        origin = Tile(0, 0)
        room1 = Room(origin, 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(8, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        down20 = Tile(0, 20)
        room2 = Room(down20, 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        across18 = Tile(18, 0)
        room3 = Room(across18, 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        rooms = level.get_reachable_rooms_from_tile(Tile(12, 5))
        self.assertEqual([[origin.y, origin.x], [across18.y, across18.x]], rooms)
    
    def test_get_reachable_rooms_returns_rooms_when_tile_in_room(self):
        origin = Tile(0, 0)
        room1 = Room(origin, 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5), Tile(8, 5), Tile(1, 1), Tile(2, 2)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        down20 = Tile(0, 20)
        room2 = Room(down20, 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        across18 = Tile(18, 0)
        room3 = Room(across18, 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2], Tile(1, 1), Tile(2, 2))
        rooms = level.get_reachable_rooms_from_tile(Tile(1, 1))
        self.assertEqual([[down20.y, down20.x], [across18.y, across18.x]], rooms)

if __name__ == '__main__':
    unittest.main()