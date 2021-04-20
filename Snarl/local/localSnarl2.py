import sys
import argparse
import json
from Snarl.src.Game.gamemanager import Gamemanager
from Snarl.src.Game.player_impl import Player
from Snarl.src.Game.enemy_zombie import EnemyZombie
from Snarl.src.Game.enemy_ghost import EnemyGhost
from Snarl.src.Game.observer_impl import Observer
from Snarl.tests.parseJson import create_level_from_json
from Snarl.src.Game.utils import grid_to_string
from Snarl.src.Game.moveresult import Moveresult
from Snarl.src.Game.occupants import LevelExit, LevelKey, Character, Zombie, Door

# set up argument parser and parse the arguments
parser = argparse.ArgumentParser(description = "game info")
parser.add_argument("--levels", metavar = "levels", type = str, nargs = 1)
parser.add_argument("--players", metavar = "players", type = int, nargs = 1)
parser.add_argument("--start", metavar = "start", type = int, nargs = 1)
parser.add_argument("--observe", metavar = "observer", nargs = "?", const = True)
args = parser.parse_args()

args.players = args.players[0] if not args.players == None else 1
# take in the levels and parse them
args.levels = args.levels[0] if not args.levels == None else "snarl.levels"
args.start = args.start[0] if not args.start == None else 0

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

def handle_string(msg):
    """ Deal with server messages that are only a single string, rather than dicts.
    """
    if msg == "move":
        print("Please provide a move in the form [y, x], or enter \"skip\" if you wish to skip your move.")
    elif msg == "OK":
        print("Your move was successful.")
    elif msg == "Key":
        print("You picked up a key!")
    elif msg == "Exit":
        print("You exited the level!")
    elif msg == "Eject":
        print("You were ejected from the level :(")
    elif msg == "Invalid":
        print("Your move was invalid. Please enter another:")
    else:
        print("Malformed server message:")
        print(msg)

def start_level(msg):
    """ Let the player know that we've started a new level and give them the relevant information.
    Expects message to be of the form:  
    { "type": "start-level",
      "level": (natural),
      "players": (name-list)
    }
    """
    player_names = ", ".join(msg["players"])
    print(f'Beginning level {msg["level"]} with players {player_names}')

def end_level(msg):
    """ Let the player know that we've ended the level and give them the relevant information.
    Expects message of the form:
    { "type": "end-level",
    "key": (name),
    "exits": (name-list),
    "ejects": (name-list)
    }
    """
    exited = ", ".join(msg["exits"])
    ejected = ", ".join(msg["ejects"])
    if msg["key"] is not None:
        print(f'Level has ended. Player {msg["key"]} picked up the key.')
    else:
        print("No player picked up the key.")
    if exited != "":
        print(f'Players {exited} exited the level.')
    else:
        print("No players exited the level.")
    if ejected != "":
        print(f'Players {ejected} were ejected from the level.')
    else:
        print("No players were ejected from the level.")

def end_game(msg):
    """ Let the player know that we've ended the game and give them the relevant information.
    Expects message of the form:
    { "type": "end-game",
    "scores": (player-score-list)
    "won": True/False
    }
    (player-score-list) is a list of
    { "type": "player-score",
    "name": (name),
    "exits": (natural),
    "ejects": (natural),
    "keys": (natural)
    }
    """
    print("Game has ended. " + ("Players" if bool(msg["game-won"]) else "Monsters") + " have won!")
    headers = ["PLAYER NAME", "EXITS", "KEYS", "EJECTS"]
    data = []
    for player in sorted(msg["scores"], key=lambda p : float(str(p["exits"]) + str(p["keys"]))):
        data.append([player["name"], player["exits"], player["keys"], player["ejects"]])
    format_row = "{:<15}" * (len(headers) + 1)
    print(format_row.format("", *headers).lstrip())
    for row in data:
        print(format_row.format("", *row).lstrip())

def player_update(msg):
    """ Update the player on what the dungeon looks like after another entity has made a move.
    Expects a message of the form:
    { "type": "player-update",
    "layout": (tile-layout),
    "position": (point),
    "objects": (object-list),
    "actors": (actor-position-list),
    "message": (maybe-string)
    Objects is of the form
    [
        { "type": "key|exit", "position": [ y, x ] },
    ]

    }
    """
    position = msg["position"]
    objects = msg["objects"]
    actors = msg["actors"]
    layout = msg["layout"]
    print(f'You are now at [{position[0]}, {position[1]}]')
    print_layout(layout, objects, actors, position)

def print_layout(layout, objects, actors, position):
    """Given a tile layout, a list of objects, a list of actors, and the player's position,
    render an ASCII grid representing the layout.
    """
    # Convert object indices relative to player indices. Player should be in the middle of the
    # layout.
    def transform_coords(o):
        absolute_posn = o["position"]
        dy = position[0] - 2
        dx = position[1] - 2
        new_y = absolute_posn[0] - dy
        new_x = absolute_posn[1] - dx
        o["position"] = [new_y, new_x]
        return o
    object_posns = list(map(transform_coords, objects))
    actor_posns = list(map(transform_coords, actors))
    printed_layout = []
    flag = False
    for row in range(len(layout)):
        new_row = []
        for col in range(len(layout[row])):
            # Do we need to render the player?
            if row == 2 and col == 2:
                new_row.append("P")
            else:
            # Do we need to render an actor?
                for actor in actor_posns:
                    if actor["position"] == [row, col]:
                        if actor["type"] == "player":
                            new_row.append("P")
                        elif actor["type"] == "zombie":
                            new_row.append("Z")
                        elif actor["type"] == "ghost":
                            new_row.append("G")
                        flag = True
                        break
                # Do we need to render an object?
                for obj in object_posns:
                    if obj["position"] == [row, col] and not flag:
                        if obj["type"] == "key":
                            new_row.append("K")
                        elif obj["type"] == "exit":
                            new_row.append("E")
                        flag = True
                        break
                if not flag:
                    new_row.append(map_tiles_nums_to_str(layout[row][col]))
                flag = False
            
        printed_layout.append(new_row)
    
    print(grid_to_string(printed_layout))

def map_tiles_nums_to_str(tile):
    """Given a 0-1-2 tile, return the character used to render it.
    """
    if tile == 1:
        return ' '
    if tile == 2:
        return 'D'
    return 'X'

def handle_server_message(msg):
    try:
        msg = json.loads(msg)
        is_json = True
        if isinstance(msg, str):
            is_json = False
    except:
        is_json = False
    if not is_json:
        handle_string(msg)
    elif msg["type"] == "welcome":
        # Do nothing cause we don't need any server information right now. This could change.
        print("Welcome To SNARL")
    elif msg["type"] == "start-level":
        start_level(msg)
    elif msg["type"] == "end-level":
        end_level(msg)
    elif msg["type"] == "end-game":
        end_game(msg)
        exit(0)
    elif msg["type"] == "player-update":
        player_update(msg)
    else:
        print("Malformed server message:")
        print(msg)

def tile_to_num(tile):
    """Transforms the given tile into a number 0, 1, 2, as specified by assignment.
    """
    if tile.has_block():
        return 0
    elif tile.has_occupant(Door):
        return 2
    else:
        return 1

def transform_layout(tile_grid):
    """Given a tile grid and a center position, transform the grid into a 5x5 grid of 0,1,2
    as per the assignment spec.
    """
    number_layout = []
    # How many rows/cols of padding do we need on each side?
    for row in tile_grid:
        number_row = []
        for tile in row:
            number_row.append(tile_to_num(tile))
        number_layout.append(number_row)
    return number_layout

class PlayerOut:
    def __init__(self, output):
        """Instantiate instance of this output object, with a connection object to use.
        """
        self.output = output
    
    def write(self, arg):
        """Write the argument, properly formatted, via print if self.output is True;
        otherwise do nothing.
        """
        if type(arg) is dict:
            if "error" in arg and arg["error"] is not None:
                self._send_error(arg)
            if arg["type"] == "update":
                self._send_update(arg)
            elif arg["type"] == "move-result":
                self._send_result(arg)
            elif arg["type"] == "start-level":
                self._send_arg(arg)
            elif arg["type"] == "end-level":
                self._send_arg(arg)
            elif arg["type"] == "end-game":
                self._send_end(arg)
            elif arg["type"] == "error":
                self._send_error(arg)
        else:
            self._send_arg(arg)
        
    def _send_arg(self, arg):
        """Sends the serialized argument.
        """
        handle_server_message(json.dumps(arg))

    def _send_error(self, arg):
        err = arg["error"]
        handle_server_message(json.dumps({"error": str(err) }))

    def _send_end(self, arg):
        """Prints endgame info to console.
        """
        won = arg["won"]
        client_msg = {"type": "end-game", "scores": arg["scores"], "game-won": won}
        handle_server_message(json.dumps(client_msg))
        
    def _send_result(self, arg):
        """Sends an update notifcation when the player EXITS, IS EJECTED, or LANDS ON THE KEY.
        Otherwise, will send nothing.
        """
        result = arg["result"]
        handle_server_message(json.dumps(result.value))

    def _send_update(self, arg):
        """Prints an update notification. This will show the player's current position as well as
        the player's surroundings.
        """
        layout = transform_layout(arg["layout"])
        position = [arg["position"].y, arg["position"].x]
        objects = list(map(lambda x: {"type": "key" if isinstance(x[1], LevelKey) else "exit", "position": \
                [x[0].y, x[0].x]}, arg["objects"]))
        actors = list(map(lambda x: {"type": "player" if isinstance(x[1], Character) else "zombie" if \
                isinstance(x[1], Zombie) else "ghost", "position": [x[0].y, x[0].x]}, arg["actors"]))
        update_msg = {"type": "player-update", "layout": layout, "position": position, \
            "objects": objects, "actors": actors, "message": None}
        handle_server_message(json.dumps(update_msg))

# If the --observe flag is present, this is set to false to disable player output in favor of
# observer's view.
player_output = True
# register an observer if the observe flag is passed
# we will override the player's view if this flag is present.
if args.observe:
    observer = Observer()
    gm.register_observer(observer)
    player_output = False

# get usernames from players (right now that's just 1) and register them
for i in range(args.players):
    print("Please enter username for player " + str(i + 1) + ":")
    name = input()
    player = Player(name, name, out = PlayerOut(player_output))
    gm.add_player(player)

first_level = levels.pop(args.start)
gm.start_game(first_level)
gm.run()