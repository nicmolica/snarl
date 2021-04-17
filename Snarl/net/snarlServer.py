import sys
import socket
import argparse
import json
import time
from netutils import send, receive
from Snarl.src.Game.gamemanager import Gamemanager
from Snarl.tests.parseJson import create_level_from_json
from Snarl.src.Game.utils import grid_to_string
from Snarl.src.Game.moveresult import Moveresult
from Snarl.src.Game.player_impl import Player
from Snarl.src.Game.enemy_zombie import EnemyZombie
from Snarl.src.Game.occupants import LevelExit, LevelKey, Character, Zombie, Door

parser = argparse.ArgumentParser(description = "socket connection info")
parser.add_argument("--levels", type = str, nargs = 1)
parser.add_argument("--clients", type = int, nargs = 1)
parser.add_argument("--wait", type = int, nargs = 1)
parser.add_argument("--observe", nargs = "?", const = True)
parser.add_argument("--address", type = str, nargs = 1)
parser.add_argument("--port", type = int, nargs = 1)
args = parser.parse_args()

args.levels = args.levels[0] if not args.levels == None else "snarl.levels"
if args.clients == None or args.clients[0] == None:
    args.clients = 4
elif args.clients[0] < 1 or args.clients[0] > 4:
    raise ValueError("There must be between 1 and 4 players in a game.")
else:
    args.clients = args.clients[0]
args.wait = args.wait[0] if not args.wait == None else 60
args.address = args.address[0] if not args.address == None else "127.0.0.1"
args.port = args.port[0] if not args.port == None else 45678

players = {}
player_connections = []
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((args.address, args.port))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.listen()

# Allow players to connect up to a max timeout
sock.settimeout(args.wait)
try:
    for i in range(args.clients):
        conn, address = sock.accept()
        print(f"Connected to {address[0]}:{address[1]}")
        player_connections.append(conn)
except socket.timeout:
    print("No Additional Players")

# Close the listening socket when player connections are established.
sock.close()

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
gm = Gamemanager(args.clients, num_of_levels = num_of_levels, levels = levels)

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
        send(self.output, json.dumps(arg))

    def _send_error(self, arg):
        err = arg["error"]
        send(self.output, json.dumps({"error": str(err) }))

    def _send_end(self, arg):
        """Prints endgame info to console.
        """
        won = arg["won"]
        client_msg = {"type": "end-game", "scores": arg["scores"], "game-won": won}
        send(self.output, json.dumps(client_msg))
        
    def _send_result(self, arg):
        """Sends an update notifcation when the player EXITS, IS EJECTED, or LANDS ON THE KEY.
        Otherwise, will send nothing.
        """
        result = arg["result"]
        send(self.output, json.dumps(result.value))

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
        send(self.output, json.dumps(update_msg))

# Send welcome message
for client in player_connections:
    msg = {"type": "welcome", "info": "No"}
    send(client, json.dumps(msg))

def make_player_input(client):
    """Given a client socket connection, return a function that can be called to receive player input.
    This used to just be a lambda but it caused an issue with multiple clients for some reason.
    """
    def input_func():
        """This function is the input function for a Player object. Call it to get a message from the player.
        """
        return receive(client)
    return input_func

# Register players with game manager
for client in player_connections:
    name_valid = False
    while not name_valid:
        send(client, "\"name\"")
        name = receive(client)
        if not name in set(players.keys()):
            name_valid = True
            player_input = make_player_input(client)
            player = Player(name, name, out=PlayerOut(client), input_func=player_input)
            gm.add_player(player)
            
# Start and run the game
gm.start_game(levels[0])
gm.run()

# Close the client sockets
for client in player_connections:
    client.close()

# TODO fix these bugs:
"""
3. Get multiple client connections working.
    . Ferd's video https://www.youtube.com/watch?v=ZvAgjIuAvrA for networking
4. Go through Gamemanager and refactor/update comments.
    . Could possibly split it up into some smaller components.
5. Ensure unit test coverage is appropriate.
    . Ty can use the coverage tool to measure this. Make sure any obvious
    gaps are covered, but some things can probably be considered "integration-only".
"""