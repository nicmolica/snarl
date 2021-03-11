import sys
sys.path.append('../src/Game')
import json
from room import Room
from tile import Tile
from level import Level
from hallway import Hallway
from occupants import LevelExit, LevelKey, Ghost, Zombie, Character
from gamestate import Gamestate
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
    occupant = None
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
                new_open = []
                for ot in er.open_tiles:
                    if ot.x != tile.x or ot.y != tile.y:
                        new_open.append(ot)
                new_open.append(tile)
                rooms[i] = Room(er.position, er.width, er.height, er.room_doors, new_open)
    
    hallways = [create_hallway_from_json(hallway) for hallway in level_json["hallways"]]
    return Level(rooms, hallways)

def create_state_from_json(state_json):
    """ Parses state_json into a Gamestate object. Assume that state_json is of the form:
    {
        "type": "state",
        "level": (level),
        "players": (actor-position-list),
        "adversaries": (actor-position-list),
        "exit-locked": (boolean)
    }
    """
    level = create_level_from_json(state_json["level"])
    level.set_level_exit_status(state_json["exit-locked"])

    players = {}
    for player in state_json["players"]:
        # per the milestone, we're assuming all actors in the "player" field are of the "player" type
        # and just adding them without verifying the type
        loc = create_point_from_json(player["position"])
        entity = create_entity_from_json(player)
        players[loc] = entity

    adversaries = {}
    for adversary in state_json["adversaries"]:
        # per the milestone, we're assuming all actors in the "adversaries" field are of the "ghost" or
        # "zombie" type and just adding them without verifying the type
        loc = create_point_from_json(adversary["position"])
        entity = create_entity_from_json(adversary)
        adversaries[loc] = entity

    # create the actual Gamestate object and add all the players and adversaries to it
    state = Gamestate(level, len(players), len(adversaries))
    for player in players.items():
        state.add_character(player[1], player[0])
    for adversary in adversaries.items():
        state.add_adversary(adversary[1], adversary[0])
    
    return state

def create_entity_from_json(player_json):
    """ Parses player_json into an Entity object. Assume that player_json is of the form:
    {
        "type": (actor-type),
        "name": (string),
        "position": (point)
    }
    """
    if player_json["type"] == "player":
        return Character(player_json["name"])
    elif player_json["type"] == "zombie":
        return Zombie(player_json["name"])
    elif player_json["type"] == "ghost":
        return Ghost(player_json["name"])

def create_point_from_json(point_json):
    """Given a JSON array with two elements [row, column], output a Tile object with
    those coordinates.
    """
    return Tile(point_json[1], point_json[0])