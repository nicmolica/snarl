from Snarl.src.Game.enemy_zombie import EnemyZombie
from Snarl.src.Game.enemy_ghost import EnemyGhost
from Snarl.src.Game.tile import Tile
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

    def test_expel_marks_as_expelled(self):
        z = EnemyZombie("Zomb", "Karl")
        z.expel()
        self.assertTrue(z.expelled)

    def test_get_entity_returns_entity(self):
        z = EnemyZombie("Zomb", "Karl")
        self.assertEqual(type(z.get_entity()), Zombie)

if __name__ == '__main__':
    unittest.main()