from Snarl.src.Game.room import Room
from Snarl.src.Game.tile import Tile
from Snarl.src.Game.hallway import Hallway
from Snarl.src.Game.level import Level
from Snarl.src.Game.occupants import LevelKey
from Snarl.src.Game.player_impl import PlayerImpl
from Snarl.src.Game.gamemanager import Gamemanager
from Snarl.src.Game.rulechecker import Rulechecker

room1 = Room(Tile(0, 0), 5, 5, [Tile(4, 1), Tile(2, 4)], [Tile(1, 1), Tile(1, 2), Tile(1, 3), Tile(2, 1), Tile(2, 2), Tile(2, 3), Tile(3, 1)])
hallway1 = Hallway([], Tile(2, 4), Tile(2, 10))
room2 = Room(Tile(0, 10), 6, 4, [Tile(2, 10)])
level = Level([room1, room2], [hallway1])
level.get_tile(Tile(1, 3)).add_occupant(LevelKey())
player = PlayerImpl("Nic Molica", "Nic")
player2 = PlayerImpl("Ty Nichols", "Ty")
player3 = PlayerImpl("Ferd", "Ferd")
manager = Gamemanager()
manager.add_player(player)
manager.add_player(player2)
manager.add_player(player3)
rulechecker_mock = Rulechecker()

f = rulechecker_mock.is_valid_move
class counter:
    def ivm(self, a,b,c):
        print("Fake count is now " + str(self.count))
        self.count += 1
        return f(a,b,c)
    def done(self):
        return self.count > 3
ctr = counter()
ctr.count = 0
rulechecker_mock.is_valid_move = lambda a, b, c : ctr.ivm(a, b, c)
rulechecker_mock.is_game_over = lambda _ : ctr.done()
manager.rule_checker = rulechecker_mock
manager.start_game(level)
manager.run()