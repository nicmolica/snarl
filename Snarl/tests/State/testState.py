import sys
sys.path.append('../../src/Game')
sys.path.append('../')
import json
from parseJson import create_level_from_json, create_point_from_json, create_state_from_json
from tile import Tile
from level import Level
from gamestate import Gamestate
from occupants import LevelExit, LevelKey
import utils

test_input = ""
for line in sys.stdin.readlines():
    test_input += line

# Per the spec, we can assume that the JSON is of the required form. 
level_json, point_json = json.loads(test_input)