import sys
import json
from Snarl.src.Game.room import Room
from Snarl.src.Game.tile import Tile
from Snarl.src.Game.level import Level
from Snarl.src.Game.hallway import Hallway
from Snarl.src.Game.occupants import LevelExit, LevelKey, Ghost, Zombie, Character, Entity, Occupant, Block, Door
from Snarl.src.Game.gamestate import Gamestate
import Snarl.src.Game.utils

def get_tiles_from_layout(position: Tile, layout: list, tile_type: int):
    """Returns a list of Tile objects with absolute coordinates corresponding to all
    tiles in layout with the matching tile_type.
    """
    tiles = []
    for row in range(len(layout)):
        for col in range(len(layout[0])):
            if layout[row][col] == tile_type:
                tiles.append(Tile(position.x + col, position.y + row))
    return tiles

def get_room_doors_from_layout(position: Tile, layout: list):
    """Given a 2D layout array of a room, return the indices for the room doors.
    """
    return get_tiles_from_layout(position, layout, 2)

def get_open_tiles_from_layout(position: Tile, layout: list):
    """Given a 2D layout array of a room, return the indices for the open tiles.
    """
    return get_tiles_from_layout(position, layout, 1)


def create_room_from_json(room_json: dict):
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

def create_object_from_json(obj_json: dict):
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

def create_hallway_from_json(hall_json: dict):
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

def create_level_from_json(level_json: dict):
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
    hallways = [create_hallway_from_json(hallway) for hallway in level_json["hallways"]]
    # Need to place objects in the rooms. For each object, place it in the room that contains it.
    # But this means we need to re-create the room.
    # For now, these are only two objects but they could be more general in the future.
    object_tiles = [create_object_from_json(obj) for obj in level_json["objects"]]
    # Put the level key and exit in the rooms
    return Level(rooms, hallways, object_tiles[0], object_tiles[1])

def create_state_from_json(state_json: dict):
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
    level.set_level_exit_status(not state_json["exit-locked"])

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

def create_entity_from_json(player_json: dict):
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

def create_point_from_json(point_json: dict):
    """Given a JSON array with two elements [row, column], output a Tile object with
    those coordinates.
    """
    return None if json.dumps(point_json) == "null" else Tile(point_json[1], point_json[0])

def create_dict_from_state(state: Gamestate) -> dict:
    """ Converts a Gamestate into a JSON representation matching the following format:
    {
        "type": "state",
        "level": (level),
        "players": (actor-position-list),
        "adversaries": (actor-position-list),
        "exit-locked": (boolean)
    }
    """
    json_state = {}
    json_state["type"] = "state"
    json_state["level"] = create_dict_from_level(state.current_level)
    json_state["players"] = list(map(lambda x: create_dict_from_entity(x, state.current_level.locate_entity(x)), \
        state.current_level.characters))
    json_state["adversaries"] = list(map(lambda x: create_dict_from_entity(x, state.current_level.locate_entity(x)), \
        state.current_level.adversaries))
    json_state["exit-locked"] = not state.current_level.level_exit_unlocked
    return json_state

def create_dict_from_entity(entity: Entity, position: Tile) -> dict:
    """ Converts an Entity into a JSON representation matching the following format:
    {
        "type": (actor-type),
        "name": (string),
        "position": (point)
    }
    """
    json_entity = {}
    if isinstance(entity, Character):
        json_entity["type"] = "player"
    elif isinstance(entity, Zombie):
        json_entity["type"] = "zombie"
    elif isinstance(entity, Ghost):
        json_entity["type"] = "ghost"
    else:
        raise TypeError("Cannot parse entity of unkown type to JSON representation.")
    
    json_entity["name"] = entity.name
    json_entity["position"] = create_dict_from_point(position)
    return json_entity

def create_dict_from_level(level: Level) -> dict:
    """ Converts a Level into a JSON representation matching the following format:
    {
        "type": "level",
        "rooms": (room-list),
        "hallways": (hall-list),
        "objects": [ { "type": "key", "position": (point) }, 
                    { "type": "exit", "position": (point) } ]
    }
    """
    json_level = {}
    json_level["type"] = "level"
    json_level["rooms"] = list(map(lambda x: create_dict_from_room(x), level.rooms))
    json_level["hallways"] = list(map(lambda x: create_dict_from_hallway(x), level.hallways))
    json_level["objects"] = []
    json_level["objects"].append(create_dict_from_object(level.get_level_key()))
    json_level["objects"].append(create_dict_from_object(level.get_level_exit()))
    return json_level

def create_array_from_layout(grid):
    layout = []
    for row in grid:
        r = []
        for tile in row:
            if tile.has_occupant(Block):
                r.append(0)
            elif tile.has_occupant(Door):
                r.append(2)
            else:
                r.append(1)
        layout.append(r)
    return layout

def create_dict_from_room(room: Room) -> dict:
    """ Converts a Room into a JSON representation matching the following format:
    {
        "type": "room",
        "origin": [Integer, Integer],
        "bounds": {
            "rows": Integer,
            "columns": Integer
        },
        "layout": [[0, 2, 1, 0]...]
    }
    """
    json_room = {}
    json_room["type"] = "room"
    json_room["origin"] = create_dict_from_point(room.position)
    json_room["bounds"] = {"rows": room.width, "columns": room.height}
    json_room["layout"] = create_array_from_layout(room.tiles)
    return json_room

def create_dict_from_hallway(hall: Hallway) -> dict:
    """ Converts a Hallway into a JSON representation matching the following format:
    { 
        "type": "hallway",
        "from": (point),
        "to": (point),
        "waypoints": (point-list)
    }
    """
    json_hall = {}
    json_hall["type"] = "hallway"
    json_hall["from"] = create_dict_from_point(hall.door1)
    json_hall["to"] = create_dict_from_point(hall.door2)
    waypoints = hall.waypoints.copy()
    waypoints.pop(0)
    waypoints.pop()
    point_list = []
    for point in waypoints:
        point_list.append(create_dict_from_point(point))
    json_hall["waypoints"] = point_list
    return json_hall

def create_dict_from_point(tile: Tile) -> dict:
    """ Converts a Tile into a JSON representation matching the following format:
    [row, column]
    """
    return [tile.y, tile.x]

def create_dict_from_object(occ: Tile) -> dict:
    """ Converts a Tile with a LevelKey or LevelExit on it into a JSON representation of the following format:
    {
        "type": ("key" or "exit"),
        "position": (point)
    }
    """
    if occ == None:
        return {"type": "key", "position": None}
    return {"type": "key" if occ.has_occupant(LevelKey) else "exit", "position": create_dict_from_point(occ)}