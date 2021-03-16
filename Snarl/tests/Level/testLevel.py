import sys
sys.path.append('../../src/Game')
sys.path.append('../')
import json
from parseJson import create_level_from_json, create_point_from_json
from tile import Tile
from level import Level
from occupants import LevelExit, LevelKey
import utils

test_input = ""
for line in sys.stdin.readlines():
    test_input += line

# Per the spec, we can assume that the JSON is of the required form. 
level_json, point_json = json.loads(test_input)

level = create_level_from_json(level_json)
point = create_point_from_json(point_json)

def tile_has_level_key_or_exit(tile):
    """Returns a string either "key", "exit" or null if the tile contains neither.
    """
    has_key = any([isinstance(occ, LevelKey) for occ in tile.occupants])
    has_exit = any([isinstance(occ, LevelExit) for occ in tile.occupants])
    if has_key:
        return "key"
    elif has_exit:
        return "exit"
    else:
        return None

def tile_in_room_or_hallway(level, tile):
    """Given a level and a tile, check whether or not the tile is inside a room, hallway,
    or neither. Return "room", "hallway", or "void", respectively.
    """
    in_room = any([room.contains(tile) for room in level.rooms])
    in_hallway = any([hallway.contains(tile) for hallway in level.hallways])
    if in_room:
        return "room"
    elif in_hallway:
        return "hallway"
    else:
        return "void"

def get_rooms_from_hallway(hallway, rooms):
    """Given a hallway and a list of rooms, determine which rooms form the endpoint of the hallway.
    Returns the room origins as a 2-element list of 2-element lists representign coordinates.
    """
    room1 = None
    room2 = None
    for room in rooms:
        if room.contains(hallway.door1):
            room1 = room.position
        if room.contains(hallway.door2):
            room2 = room.position
    return [[room1.y, room1.x], [room2.y, room2.x]]


def get_rooms_from_tile_in_hallway(level, tile):
    """Given a tile in a hallway, return the origins of the rooms that the hallway connects.
    """
    hallway = None
    for hall in level.hallways:
        if hall.contains(tile):
            hallway = hall

    # Get the room origins from the doors
    return get_rooms_from_hallway(hallway, level.rooms)

def coordinates_equal(tile1, tile2):
    """Returns True if the x-y coordinates are equal, false otherwise.
    """
    return tile1.x == tile2.x and tile1.y == tile2.y

def remove_duplicates(list):
    """Removes duplicates from this list.
    """
    []

def get_rooms_from_tile_in_room(level, tile):
    """Gets the rooms that are connected by 1 hallway to the room containing the current tile.
    Assumes that the current tile is inside a room.
    """
    origin_room = None
    for room in level.rooms:
        if room.contains(tile):
            origin_room = room
    
    origin_room_coords = [origin_room.position.y, origin_room.position.x]

    doors = origin_room.get_room_doors()
    room_own_neighbor = False
    adjacent_halls = []
    for hall in level.hallways:
        door1_in_room = False
        if any([coordinates_equal(hall.door1, door) for door in doors]):
            adjacent_halls.append(hall)
            door1_in_room = True
        door2_in_room = False
        if any([coordinates_equal(hall.door2, door) for door in doors]):
            adjacent_halls.append(hall)
            door2_in_room = True
        # Check that room is or is not its own neighbor
        if door1_in_room and door2_in_room:
            room_own_neighbor = True

    adjacent_rooms = []
    for hallway in adjacent_halls:
        adjacent_rooms.extend(get_rooms_from_hallway(hallway, level.rooms))

    unique_rooms = []
    [unique_rooms.append(x) for x in adjacent_rooms if x not in unique_rooms]
    # Must remove the room containing the tile, unless it is its own neighbor.
    if not room_own_neighbor:
        unique_rooms.remove(origin_room_coords)
    return unique_rooms

def get_reachable_rooms(level, tile):
    """Get the origins of the rooms that are "immediately reachable" from the given tile.
    If the tile is in a room, it returns the origins of any rooms connected by a single
    hallway to the tile's room.
    If the tile is in a hallway, it returns the rooms at either end of the hallway.
    If the tile is not in a room and not in a hallway, return the empty array.
    """
    tile_type = tile_in_room_or_hallway(level, tile)
    if tile_type == "void":
        return []
    elif tile_type == "hallway":
        return get_rooms_from_tile_in_hallway(level, tile)
    else: #type is "room"
        return get_rooms_from_tile_in_room(level, tile)

# get the level tiles
tile_in_level = level.get_tile(point)
output = {
    "traversable": not tile_in_level.has_block(),
    "object": tile_has_level_key_or_exit(tile_in_level),
    "type": tile_in_room_or_hallway(level, tile_in_level),
    "reachable": get_reachable_rooms(level, tile_in_level)
}

sys.stdout.write(json.dumps(output))

