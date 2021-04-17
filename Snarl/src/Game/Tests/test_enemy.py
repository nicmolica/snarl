from Snarl.src.Game.enemy_zombie import EnemyZombie
from Snarl.src.Game.enemy_ghost import EnemyGhost
from Snarl.src.Game.tile import Tile
from Snarl.src.Game.room import Room
from Snarl.src.Game.level import Level
from Snarl.src.Game.hallway import Hallway
from Snarl.src.Game.gamestate import Gamestate
from Snarl.src.Game.occupants import Zombie
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

if __name__ == '__main__':
    unittest.main()