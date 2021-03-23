from Snarl.src.Game.room import Room
from Snarl.src.Game.tile import Tile
from Snarl.src.Game.hallway import Hallway
from Snarl.src.Game.level import Level
from Snarl.src.Game.occupants import LevelKey
from Snarl.src.Game.player_impl import PlayerImpl
from Snarl.src.Game.gamemanager import Gamemanager
from Snarl.src.Game.rulechecker import Rulechecker

room1 = Room(Tile(0, 0), 10, 10, [Tile(3, 9), Tile(9, 5)], [Tile(5, 5), Tile(7, 5)])
hallway1 = Hallway([], Tile(3, 9), Tile(3, 20))
room2 = Room(Tile(0, 20), 10, 10, [Tile(3, 20)])
hallway2 = Hallway([Tile(12, 5), Tile(12, 2), Tile(15, 2)], Tile(9, 5), Tile(18, 2))
room3 = Room(Tile(18, 0), 5, 5, [Tile(18, 2)])
level = Level([room1, room2, room3], [hallway1, hallway2])
level.get_tile(Tile(7, 5)).add_occupant(LevelKey())
player = PlayerImpl("Nic Molica", "Nic")
player2 = PlayerImpl("Ty Nichols", "Ty")
manager = Gamemanager()
manager.add_player(player)
manager.add_player(player2)
rulechecker_mock = Rulechecker()

f = rulechecker_mock.is_valid_move
class counter:
    def ivm(self, a,b,c):
        print("Fake count is now " + str(self.count))
        self.count += 1
        return f(a,b,c)
    def done(self):
        return self.count > 10
ctr = counter()
ctr.count = 0
rulechecker_mock.is_valid_move = lambda a, b, c : ctr.ivm(a, b, c)
rulechecker_mock.is_game_over = lambda _ : ctr.done()
manager.rule_checker = rulechecker_mock
manager.start_game(level)
manager.run()