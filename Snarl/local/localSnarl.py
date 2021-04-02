import sys
import argparse
import json
from Snarl.src.Game.gamemanager import Gamemanager
from Snarl.src.Game.player_impl import PlayerImpl
from Snarl.src.Game.enemy_zombie import EnemyZombie
from Snarl.src.Game.enemy_ghost import EnemyGhost
from Snarl.src.Game.observer_impl import ObserverImpl
from Snarl.tests.parseJson import create_level_from_json

# set up argument parser and parse the arguments
parser = argparse.ArgumentParser(description = "game info")
parser.add_argument("--levels", metavar = "levels", type = str, nargs = 1)
parser.add_argument("--players", metavar = "players", type = int, nargs = 1)
parser.add_argument("--start", metavar = "start", type = int, nargs = 1)
parser.add_argument("--observe", metavar = "observer", nargs = "?", const = True)
args = parser.parse_args()

args.players = args.players if not args.players == None else 1

# take in the levels and parse them
args.levels = args.levels if not args.levels == None else "snarl.levels"
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

# get usernames from players (right now that's just 1) and register them
for i in range(args.players):
    print("Please enter username for player " + str(i) + ":")
    name = input()
    player = PlayerImpl(name, name, sys.stdout)
    gm.add_player(player)

# register an observer if the observe flag is passed
if args.observe:
    observer = ObserverImpl()
    gm.register_observer(observer)
    # TODO make sure this works right

