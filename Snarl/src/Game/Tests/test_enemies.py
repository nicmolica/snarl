from Snarl.src.Game.enemy_zombie import EnemyZombie
from Snarl.src.Game.enemy_ghost import EnemyGhost
import unittest
import json

class OutTrace:
    def write(self, output):
        self.output = output

class TestEnemies(unittest.TestCase):
    def test_enemies_get_state(self):
        z = EnemyZombie("name", "name")
        grid = [[3]]
        z.notify({"state": grid})
        self.assertEqual(z.state, grid)

if __name__ == '__main__':
    unittest.main()