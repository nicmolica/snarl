import sys
import json
from Snarl.src.Game.room import Room
from Snarl.src.Game.tile import Tile
from Snarl.tests.parseJson import create_room_from_json, create_point_from_json
import Snarl.src.Game.utils

test_input = ""
for line in sys.stdin.readlines():
    test_input += line

# Per the spec, we can assume that the JSON is of the required form. 
room_json, point_json = json.loads(test_input)

room = create_room_from_json(room_json)
point = create_point_from_json(point_json)

try:
    # get the traversable tiles within 1
    
    open_within_1 = room.open_tiles_around(point, 1)
    open_within_json = [[tile.y, tile.x] for tile in open_within_1]
    sys.stdout.write(json.dumps(["Success: Traversable points from ", [point.y, point.x], \
        " in room at ", [room.position.y, room.position.x] , " are ", open_within_json]))

except(ValueError):
    # Throws error when tile is not actually inside the room
    sys.stdout.write(json.dumps(["Failure: Point ", \
        [point.y, point.x], " is not in room at ", [room.position.y, room.position.x]]))