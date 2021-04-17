from Snarl.src.Game.enemy_zombie import EnemyZombie
from Snarl.src.Game.enemy_ghost import EnemyGhost
from Snarl.src.Game.tile import Tile
from Snarl.src.Game.room import Room
from Snarl.src.Game.level import Level
from Snarl.src.Game.hallway import Hallway
from Snarl.src.Game.gamestate import Gamestate
from Snarl.src.Game.occupants import Zombie, Character
import unittest
import json

class TestEnemies(unittest.TestCase):
    def test_enemies_get_state(self):
        z = EnemyZombie("name", "name")
        grid = [[3]]
        z.notify({"state": grid})
        self.assertEqual(z.state, grid)

    def test_enemy_name_must_be_string(self):
        with self.assertRaises(TypeError):
            EnemyZombie({"This is": "not a string"}, "This one is")

    def test_enemy_notify_must_be_dict(self):
        z = EnemyZombie("Zomb", "Karl")
        with self.assertRaises(RuntimeError):
            z.notify("I am not a dict")

    def test_enemy_notify_loc_stores_location(self):
        z = EnemyZombie("Zomb", "Karl")
        loc_val = Tile(23, 2)
        z.notify({ "loc": loc_val })
        self.assertEqual(z.location, loc_val)

    def test_enemy_not_equal_to_other_types(self):
        z = EnemyZombie("Zomb", "Karl")
        self.assertNotEqual(z, "I am a string")

    def test_enemies_with_equal_name_and_entities_are_equal(self):
        e1 = EnemyGhost("Ghast", "Karl")
        e2 = EnemyGhost("Ghast", "Karl")
        e2.entity = e1.entity
        self.assertEqual(e1, e2)

    def test_hash_returns_hash(self):
        z = EnemyZombie("Zomb", "Karl")
        self.assertEqual(type(z.__hash__()),int)

    def test_get_entity_returns_entity(self):
        z = EnemyZombie("Zomb", "Karl")
        self.assertEqual(type(z.get_entity()), Zombie)

    def test_get_cardinal_moves_returns_none_when_no_moves(self):
        room1 = Room(Tile(0, 0), 3, 3, [Tile(1, 2)], [Tile(1, 1)])
        room2 = Room(Tile(0, 8), 4, 4, [Tile(1, 8)], [Tile(1, 9), Tile(2, 9)])
        hall = Hallway([], Tile(1,2), Tile(1,8))
        level = Level([room1, room2], [hall], Tile(1,9), Tile(2, 9))
        z = EnemyZombie("Zombi", "Zombo")
        state = Gamestate(level, 1, 1)
        state.add_adversary(z.entity, Tile(1, 1))
        z.notify({"state": state, "loc": Tile(1, 1)})
        self.assertIsNone(z._get_valid_cardinal_moves())
    
    def test_get_cardinal_moves_returns_left_when_left_is_possible(self):
        room1 = Room(Tile(0, 0), 6, 3, [Tile(1, 2)], [Tile(1, 1), Tile(2, 1)])
        room2 = Room(Tile(0, 8), 4, 4, [Tile(1, 8)], [Tile(1, 9), Tile(2, 9)])
        hall = Hallway([], Tile(1,2), Tile(1,8))
        level = Level([room1, room2], [hall], Tile(1,9), Tile(2, 9))
        z = EnemyZombie("Zombi", "Zombo")
        state = Gamestate(level, 1, 1)
        state.add_adversary(z.entity, Tile(2, 1))
        z.notify({"state": state, "loc": Tile(2, 1)})
        self.assertNotEqual(z._get_valid_cardinal_moves(), [])

    def test_get_players_in_room_returns_empty_list_when_no_players(self):
        room1 = Room(Tile(0, 0), 6, 3, [Tile(1, 2)], [Tile(1, 1), Tile(2, 1)])
        room2 = Room(Tile(0, 8), 4, 4, [Tile(1, 8)], [Tile(1, 9), Tile(2, 9)])
        hall = Hallway([], Tile(1,2), Tile(1,8))
        level = Level([room1, room2], [hall], Tile(1,9), Tile(2, 9))
        z = EnemyZombie("Zombi", "Zombo")
        state = Gamestate(level, 1, 1)
        state.add_adversary(z.entity, Tile(2, 1))
        z.notify({"state": state, "loc": Tile(2, 1)})
        self.assertEqual(z._get_players_in_room(), [])

    def test_get_players_in_room_returns_players_in_room(self):
        room1 = Room(Tile(0, 0), 6, 3, [Tile(1, 2)], [Tile(1, 1), Tile(2, 1)])
        room2 = Room(Tile(0, 8), 4, 4, [Tile(1, 8)], [Tile(1, 9), Tile(2, 9)])
        hall = Hallway([], Tile(1,2), Tile(1,8))
        level = Level([room1, room2], [hall], Tile(1,9), Tile(2, 9))
        z = EnemyZombie("Zombi", "Zombo")
        state = Gamestate(level, 1, 1)
        state.add_adversary(z.entity, Tile(2, 1))
        character = Character("char")
        character_loc = Tile(1, 1)
        state.add_character(character, character_loc)
        z.notify({"state": state, "loc": Tile(2, 1)})
        players_in_room = z._get_players_in_room()
        self.assertNotEqual(players_in_room, [])
        self.assertTrue(players_in_room[0].coordinates_equal(character_loc))

    def test_determine_move_returns_move_not_farther_than_player_in_room(self):
        room1 = Room(Tile(0, 0), 6, 3, [Tile(1, 2)], [Tile(1, 1), Tile(2, 1)])
        room2 = Room(Tile(0, 8), 4, 4, [Tile(1, 8)], [Tile(1, 9), Tile(2, 9)])
        hall = Hallway([], Tile(1,2), Tile(1,8))
        level = Level([room1, room2], [hall], Tile(1,9), Tile(2, 9))
        z = EnemyZombie("Zombi", "Zombo")
        state = Gamestate(level, 1, 1)
        state.add_adversary(z.entity, Tile(2, 1))
        character = Character("char")
        character_loc = Tile(1, 1)
        state.add_character(character, character_loc)
        z.notify({"state": state, "loc": Tile(2, 1)})
        move = z._determine_move()
        self.assertTrue(move.coordinates_equal(character_loc))

    def test_cannot_move_before_being_notified_of_game_state(self):
        with self.assertRaises(RuntimeError):
            EnemyZombie("Zombi", "Zombo")._determine_move()

    def test_move_moves_in_random_open_dir_when_no_player_in_room(self):
        room1 = Room(Tile(0, 0), 6, 3, [Tile(1, 2)], [Tile(1, 1), Tile(2, 1)])
        room2 = Room(Tile(0, 8), 4, 4, [Tile(1, 8)], [Tile(1, 9), Tile(2, 9)])
        hall = Hallway([], Tile(1,2), Tile(1,8))
        level = Level([room1, room2], [hall], Tile(1,9), Tile(2, 9))
        z = EnemyZombie("Zombi", "Zombo")
        state = Gamestate(level, 1, 1)
        state.add_adversary(z.entity, Tile(2, 1))
        open_loc = Tile(1, 1)
        z.notify({"state": state, "loc": Tile(2, 1)})
        move = z._determine_move()
        self.assertTrue(move.coordinates_equal(open_loc))

    def test_ghost_moves_to_closest_wall_when_no_player_in_range(self):
        room1 = Room(Tile(0, 0), 6, 3, [Tile(1, 2)], [Tile(1, 1), Tile(2, 1)])
        room2 = Room(Tile(0, 8), 4, 4, [Tile(1, 8)], [Tile(1, 9), Tile(2, 9)])
        hall = Hallway([], Tile(1,2), Tile(1,8))
        level = Level([room1, room2], [hall], Tile(1,9), Tile(2, 9))
        g = EnemyGhost("El Ghost", "gost")
        state = Gamestate(level, 1, 1)
        state.add_adversary(g.entity, Tile(2, 1))
        g.notify({"state": state, "loc": Tile(2, 1)})
        move = g._determine_move()
        self.assertTrue(move.coordinates_equal(Tile(3, 1)))

    def test_ghost_moves_to_player_when_player_in_room(self):
        room1 = Room(Tile(0, 0), 6, 3, [Tile(1, 2)], [Tile(1, 1), Tile(2, 1)])
        room2 = Room(Tile(0, 8), 4, 4, [Tile(1, 8)], [Tile(1, 9), Tile(2, 9)])
        hall = Hallway([], Tile(1,2), Tile(1,8))
        level = Level([room1, room2], [hall], Tile(1,9), Tile(2, 9))
        g = EnemyGhost("El Ghost", "gost")
        state = Gamestate(level, 1, 1)
        state.add_adversary(g.entity, Tile(2, 1))
        character = Character("char")
        character_loc = Tile(1, 1)
        state.add_character(character, character_loc)
        g.notify({"state": state, "loc": Tile(2, 1)})
        move = g._determine_move()
        self.assertTrue(move.coordinates_equal(character_loc))


if __name__ == '__main__':
    unittest.main()