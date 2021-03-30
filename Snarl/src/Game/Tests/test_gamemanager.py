import sys
import unittest
import random
from Snarl.src.Game.tile import Tile
from Snarl.src.Game.room import Room
from Snarl.src.Game.hallway import Hallway
from Snarl.src.Game.level import Level
from Snarl.src.Game.player_impl import PlayerImpl
from Snarl.src.Game.occupants import Zombie
from Snarl.src.Game.enemy import Enemy
from Snarl.src.Game.gamemanager import Gamemanager

class TestGamemanager(unittest.TestCase):
    def test_constructor_error_when_view_distance_nonpositive(self):
        with self.assertRaises(ValueError):
            Gamemanager(3, -423, 1)

    def test_constructor_error_when_max_players_nonpositive(self):
        with self.assertRaises(ValueError):
            Gamemanager(-31232)

    def test_constructor_error_when_num_levels_nonpositive(self):
        with self.assertRaises(ValueError):
            Gamemanager(num_of_levels=-123)

    def test_add_player_adds_successfully(self):
        manager = Gamemanager()
        player = PlayerImpl("Ty", "Tulkas Astaldo")
        manager.add_player(player)
        self.assertEqual(len(manager.player_list), 1)
    
    def test_add_player_cannot_add_duplicate_player_names(self):
        manager = Gamemanager()
        player = PlayerImpl("Ty", "Tulkas Astaldo")
        player_same = PlayerImpl("Ty", "Tulkas Astaldo")
        manager.add_player(player)
        with self.assertRaises(ValueError):
            manager.add_player(player_same)
    
    def test_add_player_cannot_add_more_than_max_players(self):
        manager = Gamemanager(1)
        player = PlayerImpl("Ty", "Tulkas Astaldo")
        player2 = PlayerImpl("Nic", "Morgoth Bauglir")
        manager.add_player(player)
        with self.assertRaises(RuntimeError):
            manager.add_player(player2)

    def test_add_player_registers_observer(self):
        manager = Gamemanager(1)
        player = PlayerImpl("Ty", "Tulkas Astaldo")
        manager.add_player(player)
        self.assertEqual(len(manager.observers), 1)

    def test_register_observer_registers_observer(self):
        manager = Gamemanager(1)
        # for now, since players are observers, just add one of these
        # (do not do this if you want the player as an actual player)
        player = PlayerImpl("Ty", "Tulkas Astaldo")
        manager.register_observer(player)
        self.assertEqual(len(manager.observers), 1)

    def test_add_adversary_adds_one_adversary(self):
        manager = Gamemanager(1)
        manager.add_enemies(Enemy("enemy", Zombie, "zomb"))
        self.assertEqual(len(manager.enemy_list), 1)

    def test_add_adversary_adds_list_of_adversaries(self):
        manager = Gamemanager(1)
        l = [Enemy("enemy 1", Zombie, "zomb 1"), Enemy("enemy 2", Zombie, "zomb 3")]
        manager.add_enemies(l)
        self.assertEqual(len(manager.enemy_list), len(l))
    
    def test_add_adversary_errors_when_not_adding_adversary(self):
        manager = Gamemanager(1)
        with self.assertRaises(TypeError):
            manager.add_enemies({"i'm": "not", "an": "adversary"})

    def test_start_game_starts(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2])
        player = PlayerImpl("Ty", "Tulkas Astaldo")
        manager = Gamemanager()
        manager.add_player(player)
        manager.start_game(level)

    def test_start_game_errors_when_not_enough_space_in_first_room(self):
        room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5)])
        hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
        room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
        hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
        room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
        level = Level([room1, room2, room3], [hallway1, hallway2])
        player = PlayerImpl("Ty", "Tulkas Astaldo")
        player2 = PlayerImpl("Nic", "Morgoth Bauglir")
        player3 = PlayerImpl("Ferd", "Túrin Turambar Neithan Gorthol Agarwaen Adanedhel Mormegil")
        manager = Gamemanager()
        manager.add_player(player)
        manager.add_player(player2)
        manager.add_player(player3)
        with self.assertRaises(RuntimeError):
            manager.start_game(level)

    def test_run_raises_error_when_called_before_game_start(self):
        manager = Gamemanager()
        with self.assertRaises(RuntimeError):
            manager.run()

    def test_get_move_raises_error_when_called_before_game_start(self):
        manager = Gamemanager()
        with self.assertRaises(RuntimeError):
            manager.move(Tile(3, 4))

    def test_quit_game_raises_error_when_called_before_game_start(self):
        manager = Gamemanager()
        with self.assertRaises(RuntimeError):
            manager.quit_game()
        
    def test_begin_next_level_raises_error_when_called_before_game_start(self):
        manager = Gamemanager()
        with self.assertRaises(RuntimeError):
            manager.begin_next_level()
    
    def test_render_raises_error_when_called_before_game_start(self):
        manager = Gamemanager()
        with self.assertRaises(RuntimeError):
            manager.render()
    
    def test_update_players_raises_error_when_called_before_game_start(self):
        manager = Gamemanager()
        with self.assertRaises(RuntimeError):
            manager.update_players()

    def test_get_adversary_move_raises_error_when_called_before_game_start(self):
        manager = Gamemanager()
        with self.assertRaises(RuntimeError):
            manager.get_enemy_move()

    def test_get_player_move_raises_error_when_called_before_game_start(self):
        manager = Gamemanager()
        with self.assertRaises(RuntimeError):
            manager.get_player_move()


if __name__ == '__main__':
    unittest.main()