import sys
import socket
import argparse
import json
from Snarl.src.Game.gamemanager import Gamemanager
from Snarl.tests.parseJson import create_level_from_json
from Snarl.src.Game.utils import grid_to_string
from Snarl.src.Game.moveresult import Moveresult
from Snarl.src.Game.occupants import LevelExit, LevelKey, Character, Zombie

parser = argparse.ArgumentParser(description = "socket connection info")
parser.add_argument("--levels", type = str, nargs = 1)
parser.add_argument("--clients", type = int, nargs = 1)
parser.add_argument("--wait", type = int, nargs = 1)
parser.add_argument("--observe", nargs = "?", const = True)
parser.add_argument("--address", type = str, nargs = 1)
parser.add_argument("--port", type = int, nargs = 1)
args = parser.parse_args()

args.levels = args.levels[0] if not args.levels == None else "snarl.levels"
if args.clients[0] == None:
    args.clients = 4
elif args.clients[0] < 1 or args.clients[0] > 4:
    raise ValueError("There must be between 1 and 4 players in a game.")
args.wait = args.wait[0] if not args.wait == None else 60
args.address = args.address[0] if not args.address == None else "127.0.0.1"
args.port = args.port[0] if not args.port == None else 45678

socks = []
players = {}
for i in range(args.clients):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
    sock.bind((args.address, args.port))
    sock.setblocking(0)
    sock.listen()
    socks.append(sock)

def send(sock, msg):
    sock.sendall(msg.encode())

def receive(sock):
    packet = sock.recv(32768)
    msg = packet.decode('utf-8')
    return msg

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

class PlayerOut:
    def __init__(self, output):
        """Instantiate instance of this output object, with a boolean of whether or not
        to actually print anything.
        """
        self.output = output
    
    def write(self, arg):
        """Write the argument, properly formatted, via print if self.output is True;
        otherwise do nothing.
        """
        send(self.output, arg)

    def _write(self, arg):
        """Writes the arg to standard output with proper formatting.
        """
        if type(arg) is dict:
            if "error" in arg and arg["error"] is not None:
                print(arg["error"])
            if arg["type"] == "update":
                self._send_update(arg)
            elif arg["type"] == "move-result":
                self._print_result(arg)
            elif arg["type"] == "end":
                self._print_end(arg)
            elif arg["type"] == "error":
                self._print_error(arg)
        else:
            print(arg)
    
    def _print_error(self, arg):
        err = arg["error"]
        print(err)

    def _print_end(self, arg):
        """Prints endgame info to console.
        """
        won = arg["won"]
        failed_in = arg["failed-in"]
        if won:
            print("You won the game!")
            print(f"Keys collected: {failed_in - 1}")
        else:
            print(f"You lost in level {failed_in}")

    def _print_result(self, arg):
        """Prints an update notifcation when the player EXITS, IS EJECTED, or LANDS ON THE KEY.
        Otherwise, will print nothing.
        """
        result = arg["result"]
        res_string = f"Player {arg['name']} "
        if result == Moveresult.EXIT:
            print(res_string + "exited")
        if result == Moveresult.EJECT:
            print(res_string + "was expelled")
        if result == Moveresult.KEY:
            print(res_string + "found the key")

    def _send_update(self, arg):
        """Prints an update notification. This will show the player's current position as well as
        the player's surroundings.
        """
        update_msg = {"type": "player-update", "layout": arg["layout"], "position": [arg["postion"].x, arg["postion"].y], \
            "objects": list(map(lambda x: {"type": "key" if isinstance(x[1], LevelKey) else "exit", "position": \
                [x[0].y, x[0].x]}, arg["objects"])),
            "actors": list(map(lambda x: {"type": "player" if isinstance(x[1], Character) else "zombie" if \
                isinstance(x[1], Zombie) else "ghost", "position": [x[0].y, x[0].x]}, arg["objects"])),
            "message": None}
        send(self.output, update_msg)

for client in socks:
    msg = {}
    msg["type"] = "welcome"
    msg["info"] = "a meme" # TODO
    send(client, json.dumps(msg))

for client in socks:
    name_valid = False
    while not name_valid:
        send(client, "\"name\"")
        name = receive(client)
        if not name in set(players.keys):
            players[name] = client
            name_valid = True