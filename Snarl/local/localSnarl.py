import sys
import argparse
import json
from Snarl.src.Game.gamemanager import Gamemanager
from Snarl.src.Game.player_impl import PlayerImpl
from Snarl.src.Game.enemy_zombie import EnemyZombie
from Snarl.src.Game.enemy_ghost import EnemyGhost
from Snarl.src.Game.observer_impl import ObserverImpl
from Snarl.tests.parseJson import create_level_from_json
from Snarl.src.Game.utils import grid_to_string
from Snarl.src.Game.moveresult import Moveresult

# set up argument parser and parse the arguments
parser = argparse.ArgumentParser(description = "game info")
parser.add_argument("--levels", metavar = "levels", type = str, nargs = 1)
parser.add_argument("--players", metavar = "players", type = int, nargs = 1)
parser.add_argument("--start", metavar = "start", type = int, nargs = 1)
parser.add_argument("--observe", metavar = "observer", nargs = "?", const = True)
args = parser.parse_args()

args.players = args.players[0] if not args.players == None else 1
# take in the levels and parse them
args.levels = args.levels[0] if not args.levels == None else "snarl.levels"
args.start = args.start[0] if not args.start == None else 0

f = open(args.levels)
levels_string = f.read()
levels_len = len(levels_string)
level_jsons = []
decoder = json.JSONDecoder()
error_index = 0
while error_index < levels_len and len(levels_string) > 0:
    try: 
        leveljson_obj, error_index = decoder.raw_decode(levels_string)
        level_jsons.append(leveljson_obj)
        levels_string = levels_string[error_index:]
    except(json.decoder.JSONDecodeError):
        levels_string = levels_string[1:]

# instantiate a gamemanager
num_of_levels = level_jsons.pop(0)
levels = list(map(create_level_from_json, level_jsons))
gm = Gamemanager(args.players, num_of_levels = num_of_levels, levels = levels)

# don't allow more than 1 player right now (spec said we could do this until networking is implemented)
if args.players > 1:
    print("More than 1 player is currently not supported!")
    exit(0)

class PlayerOut:
    def __init__(self, output):
        """Instantiate instance of this output object, with a boolean of whether or not
        to actually print anything.
        """
        self.output = output
    
    def write(self, arg):
        """Write the argument, properly formatted, via print if self.output is True;
        otherwise do nothing.
        """
        if self.output:
            self._write(arg)

    def _write(self, arg):
        """Writes the arg to standard output with proper formatting.
        """
        if type(arg) is dict:
            if "error" in arg and arg["error"] is not None:
                print(arg["error"])
            if arg["type"] == "update":
                self._print_update(arg)
            elif arg["type"] == "move-result":
                self._print_result(arg)
            elif arg["type"] == "end":
                won = arg["won"]
                failed_in = arg["failed-in"]
                if won:
                    print("You won the game!")
                    print(f"Keys collected: {failed_in - 1}")
                else:
                    print(f"You lost in level {failed_in}")
        else:
            print(arg)
    
    def _print_result(self, arg):
        """Prints an update notifcation when the player EXITS, IS EJECTED, or LANDS ON THE KEY.
        Otherwise, will print nothing.
        """
        result = arg["result"]
        res_string = f"Player {arg['name']} "
        if result == Moveresult.EXIT:
            print(res_string + "exited")
        if result == Moveresult.EJECT:
            print(res_string + "was expelled")
        if result == Moveresult.KEY:
            print(res_string + "found the key")

    def _print_update(self, arg):
        """Prints an update notification. This will show the player's current position as well as
        the player's surroundings.
        """
        tiles = arg["layout"]
        posn = arg["position"]
        posn_string = "null"
        if posn is not None:
            posn_string = f"[{posn.x}, {posn.y}]"
        print(f"Player Position:{posn_string}")
        print(grid_to_string(list(map(lambda row: map(lambda tile : tile.render(), row), tiles))))
        print("\n")


# If the --observe flag is present, this is set to false to disable player output in favor of
# observer's view.
player_output = True
# register an observer if the observe flag is passed
# we will override the player's view if this flag is present.
if args.observe:
    observer = ObserverImpl()
    gm.register_observer(observer)
    player_output = False
    # TODO make sure this works right-should be able to see entire level.

# get usernames from players (right now that's just 1) and register them
for i in range(args.players):
    print("Please enter username for player " + str(i + 1) + ":")
    name = input()
    player = PlayerImpl(name, name, out = PlayerOut(player_output))
    gm.add_player(player)

# TODO: When player exits, next level does not seem to start properly.
# TODO: Verify that game ends with player victory or defeat as appropriate.
first_level = levels.pop(args.start)
gm.start_game(first_level)
gm.run()