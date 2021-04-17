import sys
import unittest
import random
from Snarl.src.Game.tile import Tile
from Snarl.src.Game.occupants import Occupant, Entity, Character, Adversary, LevelExit, LevelKey, \
    Zombie, Ghost, Wall

class TestOccupants(unittest.TestCase):
    def test_occupant_equality_is_type_check(self):
        occ1 = Occupant()
        occ2 = Occupant()
        self.assertEqual(occ1, occ2)
    
    def test_occupant_hash_is_constant(self):
        occ = Occupant()
        self.assertEqual(1, occ.__hash__())
    
    def test_entity_equality_is_type_check(self):
        occ1 = Entity()
        occ2 = Entity()
        self.assertEqual(occ1, occ2)
    
    def test_entity_hash_is_constant(self):
        occ = Entity()
        self.assertEqual(3, occ.__hash__())

    def test_adversary_render(self):
        adv = Adversary()
        self.assertEqual(adv.render(), 'A')

    def test_zombies_equal_with_same_name(self):
        name = "zomb" 
        z1 = Zombie(name)
        z2 = Zombie(name)
        z2.name = z1.name
        self.assertEqual(z1, z2)

    def test_zombie_names_increment(self):
        z1 = Zombie()
        z2 = Zombie()
        self.assertNotEqual(z1.name, z2.name)

    def test_ghost_renders_as_g(self):
        g = Ghost()
        self.assertEqual(g.render(), "G")

    def test_wall_renders_as_pound(self):
        w = Wall()
        self.assertEqual(w.render(), "#")
        

if __name__ == '__main__':
    unittest.main()