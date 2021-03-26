import sys
import json
from Snarl.tests.parseJson import *
from Snarl.src.Game.tile import Tile
from Snarl.src.Game.level import Level
from Snarl.src.Game.gamestate import Gamestate
from Snarl.src.Game.gamemanager import Gamemanager
from Snarl.src.Game.player_impl import PlayerImpl

test_input = ""
for line in sys.stdin.readlines():
    test_input += line

# per the assignment spec, we can assume that the json is well-formed
name_list, json_level, num_of_turns, locations, turns = json.loads(test_input)

# make all the players
players = []
for i in range(len(name_list)):
    new_player = {}
    new_player["type"] = "player"
    new_player["name"] = name_list[i]
    new_player["position"] = locations[i]
    players.append(create_entity_from_json(new_player))

# make the level
level = create_level_from_json(json_level)

# make the gamemanager and start the game
manager = Gamemanager(4, 2, 1)

# register the players
for player in players:
    manager.add_player(PlayerImpl(player.name, player.name))

# start the game
manager.start_game(level)

# move the players to their correct initial locations
for i in range(len(players)):
    level.move_occupant(players[i], create_point_from_json(locations[i]))

# make the adversaries and add them to the game (they're all zombies right now but this doesn't need to be the case)
adversaries = []
for i in range(len(name_list), len(locations)):
    json_new_adversary = {}
    json_new_adversary["type"] = "zombie"
    json_new_adversary["name"] = "zombie"
    json_new_adversary["position"] = locations[i]
    new_adversary = create_entity_from_json(json_new_adversary)
    adversaries.append(new_adversary)
    level.add_adversary(new_adversary, create_point_from_json(locations[i]))

manager.add_adversaries(adversaries)

# make moves until we've reached the max number of turns
for i in range(num_of_turns):
    turn_list_i = i % len(turns)

    # if we've run out of turns to make or the game is over, we're done
    if len(turns[turn_list_i]) == 0 or manager.rule_checker.is_game_over(manager.game_state):
        break

    # attempt a turn
    to = create_point_from_json(turns[turn_list_i][0]["to"])
    turns[turn_list_i].pop(0)
    try:
        manager.move(to)
    except:
        pass

state = create_dict_from_state(manager.game_state)
print(json.dumps(state))