import sys
sys.path.append('../../src/Game')
import json
from room import Room
from tile import Tile
import utils

def get_tiles_from_layout(position, layout, tile_type):
    """Returns a list of Tile objects with absolute coordinates corresponding to all
    tiles in layout with the matching tile_type.
    """
    tiles = []
    for row in range(len(layout)):
        for col in range(len(layout[0])):
            if layout[row][col] == tile_type:
                tiles.append(Tile(position.x + col, position.y + row))
    return tiles

def get_room_doors_from_layout(position, layout):
    """Given a 2D layout array of a room, return the indices for the room doors.
    """
    return get_tiles_from_layout(position, layout, 2)

def get_open_tiles_from_layout(position, layout):
    """Given a 2D layout array of a room, return the indices for the open tiles.
    """
    return get_tiles_from_layout(position, layout, 1)


def create_room_from_json(room_json):
    """Parses room_json into one of our room objects. Assume that the room_json is of the form
    {
        "type": "room",
        "origin": [Integer, Integer],
        "bounds": {
            "rows": Integer,
            "columns": Integer
        },
        "layout": [[0, 2, 1, 0]...]
    }
    See the Milestone 3 spec for more details.
    """
    position = Tile(room_json["origin"][1], room_json["origin"][0])
    width = room_json["bounds"]["columns"]
    height = room_json["bounds"]["rows"]
    layout = room_json["layout"]
    room_doors = get_room_doors_from_layout(position, layout)
    open_tiles = get_open_tiles_from_layout(position, layout)
    room = Room(position, width, height, room_doors, open_tiles)
    return room

def create_point_from_json(point_json):
    """Given a JSON array with two elements [row, column], output a Tile object with
    those coordinates.
    """
    return Tile(point_json[1], point_json[0])

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
