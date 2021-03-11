import sys
sys.path.append('../../src/Game')
sys.path.append('../')
import json
from parseJson import create_level_from_json, create_point_from_json, create_state_from_json, create_entity_from_json
from tile import Tile
from level import Level
from gamestate import Gamestate
from occupants import LevelExit, LevelKey, Character
import utils

test_input = ""
for line in sys.stdin.readlines():
    test_input += line

# Per the spec, we can assume that the JSON is of the required form. 
state_json, name_json, point_json = json.loads(test_input)

state = create_state_from_json(state_json)

def get_entity(name, players):
    """ Get an actual entity from the player json.
    """
    for p in players:
        if name == p["name"]:
            return create_entity_from_json(p)
    return None

def remove_player(player, state_json):
    """ Remove the given player from the state json.
    """
    state = state_json.copy()
    for p in state_json["players"]:
        if p["name"] == player.name:
            state["players"].remove(p)
            break
    return state

def move_player(player, dest):
    """Move the given player's location to its destination in state json.
    """
    for p in state_json["players"]:
        if p["name"] == player.name:
            p["position"] = [dest.y, dest.x]

entity = get_entity(name_json, state_json["players"])
point = create_point_from_json(point_json)

dest_tile = state.get_tiles()[point.y][point.x]

if not entity:
    # case 4
    output = ["Failure", "Player ", name_json, " is not a part of the game."]
elif dest_tile.has_block() or Character in [type(occ) for occ in dest_tile.occupants]:
    # case 5
    output = ["Failure", "The destination position ", point_json, " is invalid."]
else:
    state.move(entity, point)
    if entity in state.current_level.completed_characters:
        # case 3
        state_json = remove_player(entity, state_json)
        output = ["Success", "Player ", name_json, " exited.", state_json]
    elif entity not in state.current_level.characters:
        # case 2
        state_json = remove_player(entity, state_json)
        output = ["Success", "Player ", name_json, " was ejected.", state_json]
    else:
        # case 1
        move_player(entity, point)
        output = ["Success", state_json]

sys.stdout.write(json.dumps(output))