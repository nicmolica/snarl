import sys
sys.path.append('../src/Game')
import json
from room import Room
from tile import Tile
from level import Level
from hallway import Hallway
from occupants import LevelExit, LevelKey
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

def create_object_from_json(obj_json):
    """Parses obj_json into a level key or level exit.
    """
    objType = obj_json["type"]
    position = create_point_from_json(obj_json["position"])
    occupant = None;
    if (objType == "exit"):
        occupant = LevelExit()
    if (objType == "key"):
        occupant = LevelKey()
    return Tile(position.x, position.y, occupant)

def create_hallway_from_json(hall_json):
    """Create a Hallway object from the hall_json object. Hallway JSON is of the form
        { 
            "type": "hallway",
            "from": (point),
            "to": (point),
            "waypoints": (point-list)
        }
    """
    doorFrom = create_point_from_json(hall_json["from"])
    doorTo = create_point_from_json(hall_json["to"])
    waypoints = [create_point_from_json(wp) for wp in hall_json["waypoints"]]
    return Hallway(waypoints, doorFrom, doorTo)

def create_level_from_json(level_json):
    """Parses room_json into one of our room objects. Assume that the room_json is of the form
        {
            "type": "level",
            "rooms": (room-list),
            "hallways": (hall-list),
            "objects": [ { "type": "key", "position": (point) }, 
               { "type": "exit", "position": (point) } ]
        }

    See the Milestone 4 spec for more details.
    """
    # Create partial rooms. These do not have objects, but we can use them to check if the object
    # coordinates are inside the rooms.
    rooms = [create_room_from_json(room_json) for room_json in level_json["rooms"]]
    # Need to place objects in the rooms. For each object, place it in the room that contains it.
    # But this means we need to re-create the room.
    # For now, these are only two objects but they could be more general in the future.
    object_tiles = [create_object_from_json(obj) for obj in level_json["objects"]]
    # Put the level key and exit in the rooms
    for tile in object_tiles:
        for i in range(len(rooms)):
            er = rooms[i]
            if er.contains(tile):
                rooms[i] = Room(er.position, er.width, er.height, er.room_doors, [tile])
    
    hallways = [create_hallway_from_json(hallway) for hallway in level_json["hallways"]]
    return Level(rooms, hallways)
    

def create_point_from_json(point_json):
    """Given a JSON array with two elements [row, column], output a Tile object with
    those coordinates.
    """
    return Tile(point_json[1], point_json[0])