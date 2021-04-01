import sys
import unittest
import random
from Snarl.src.Game.tile import Tile
from Snarl.src.Game.room import Room
from Snarl.src.Game.hallway import Hallway
from Snarl.src.Game.level import Level
from Snarl.src.Game.player_impl import PlayerImpl
from Snarl.src.Game.occupants import Character, Adversary, Zombie, LevelKey, LevelExit
from Snarl.src.Game.rulechecker import Rulechecker
from Snarl.src.Game.gamestate import Gamestate

class TestRulechecker(unittest.TestCase):
    def test_valid_move_player(self):
        p = PlayerImpl("player name", "character name")
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        level.add_character(p.entity, Tile(2, 6))
        is_valid = rulechecker.is_valid_move(p, Tile(1, 7), level)

    def test_valid_move_adversary(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        adv = Adversary()
        level.add_adversary(adv, Tile(2, 6))
        is_valid = rulechecker.is_valid_move(adv, Tile(1, 7), level)


    def test_is_not_open_when_player_moves_to_player_tile(self):
        rulechecker = Rulechecker()
        is_open = rulechecker.is_open_tile(Tile(3, 4, [Character("Character 1")]), None)
        self.assertFalse(is_open)

    def test_is_open_when_adversary_moves_to_player_tile(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4), Tile(3, 3)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1], Tile(3, 4), Tile(3, 20))

        is_open = rulechecker.is_open_tile(Tile(3, 3, [Character("Character 1")]), level, Adversary)
        self.assertTrue(is_open)

    def test_valid_player_move_2_steps_diagonal(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        character = Character("char")
        level.add_character(character, Tile(2, 6))
        is_valid = rulechecker._is_valid_player_move(character, Tile(1, 7), level)
        self.assertTrue(is_valid)
    
    def test_valid_player_move_2_steps_same_dir(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        character = Character("char")
        level.add_character(character, Tile(1, 9))
        is_valid = rulechecker._is_valid_player_move(character, Tile(1, 7), level)
        self.assertTrue(is_valid)

    def test_invalid_player_move_too_far(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        character = Character("char")
        level.add_character(character, Tile(1, 13))
        with self.assertRaises(RuntimeError):
            rulechecker._is_valid_player_move(character, Tile(1, 7), level)
        
    def test_invalid_player_move_blocked_dest(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        character = Character('name')
        level.add_character(character, Tile(0, 0))
        with self.assertRaises(RuntimeError):
            rulechecker._is_valid_player_move(character, Tile(0, 2), level)

    def test_valid_adversary_move(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1], Tile(3, 4), Tile(3, 20))
        adv = Zombie()
        level.add_adversary(adv, Tile(1, 8))
        is_valid = rulechecker._is_valid_zombie_move(adv, Tile(1, 7), level)
        self.assertTrue(is_valid)
    
    def test_invalid_adversary_move_too_far(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1], Tile(3, 4), Tile(3, 20))
        adv = Zombie()
        level.add_adversary(adv, Tile(1, 11))
        is_valid = rulechecker._is_valid_zombie_move(adv, Tile(1, 7), level)
        self.assertFalse(is_valid)

    def test_invalid_adversary_move_blocked_dest(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1], Tile(3, 4), Tile(3, 20))
        adv = Zombie()
        level.add_adversary(adv, Tile(0, 0))
        is_valid = rulechecker._is_valid_zombie_move(adv, Tile(1, 0), level)
        self.assertFalse(is_valid)
        
    def test_players_won_when_players_won(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        state = Gamestate(level, 2, 0)
        players_won = rulechecker.did_players_win(state)
        self.assertTrue(players_won)

    def test_players_lost_when_players_lost(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        state = Gamestate(level, 1, 0)
        # Manually remove all players from current level; this will happen elsewhere when players
        # defeated.
        state.current_level.characters = []
        players_won = rulechecker.did_players_win(state)
        self.assertFalse(players_won)

    def test_is_level_over_when_level_not_over(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        character = Character("John Wick")
        level.add_character(character, Tile(3, 4))
        level_over = rulechecker.is_level_over(level)
        self.assertFalse(level_over)

    def test_is_level_over_when_level_not_over(self):
        rulechecker = Rulechecker()
        room1 = Room(Tile(0, 0), 5, 5, [Tile(3, 4)])
        hallway1 = Hallway([Tile(3, 6), Tile(1, 6), Tile(1, 18), Tile(3, 18)], Tile(3, 4), Tile(3, 20))
        room2 = Room(Tile(0, 20), 5, 10, [Tile(3, 20)])
        level = Level([room1, room2], [hallway1])
        level_over = rulechecker.is_level_over(level)
        self.assertTrue(level_over)

if __name__ == '__main__':
    unittest.main()