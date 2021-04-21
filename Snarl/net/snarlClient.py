import sys
import socket
import argparse
import json
import time
from netutils import send, receive
from Snarl.src.Game.utils import grid_to_string

parser = argparse.ArgumentParser(description = "socket connection info")
parser.add_argument("--address", type = str, nargs = 1)
parser.add_argument("--port", type = int, nargs = 1)
args = parser.parse_args()

args.address = args.address[0] if not args.address == None else "127.0.0.1"
args.port = args.port[0] if not args.port == None else 45678

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((args.address, args.port))

def process_move():
    """ Verify that a user-entered move has valid syntax before sending it to the server.
    """
    valid_input = False
    input_json = None
    while not valid_input:
        to_send = None
        coords = input()
        try:
            input_json = json.loads(coords)
            if type(input_json) == list and len(input_json) == 2:
                valid_input = True
                y, x = input_json
                to_send = [y, x]
        except:
            if coords == "skip":
                valid_input = True
    
    send(sock, json.dumps(to_send))

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

def end_game(msg, running_totals = False):
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
    if running_totals:
        print("Running total of scores are as follows:")
    else:
        print("Game has ended. " + ("Players" if bool(msg["game-won"]) else "Monsters") + " have won!")
    headers = ["PLAYER NAME", "EXITS", "KEYS", "EJECTS"]
    data = []
    for player in sorted(msg["scores"], key=lambda p : float(str(p["exits"]) + str(p["keys"]))):
        data.append([player["name"], player["exits"], player["keys"], player["ejects"]])
    format_row = "{:<15}" * (len(headers) + 1)
    print(format_row.format("", *headers).lstrip())
    for row in data:
        print(format_row.format("", *row).lstrip())

def map_tiles_nums_to_str(tile):
    """Given a 0-1-2 tile, return the character used to render it.
    """
    if tile == 1:
        return ' '
    if tile == 2:
        return 'D'
    return 'X'

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

def handle_string(msg):
    """ Deal with server messages that are only a single string, rather than dicts.
    """
    if msg == "name":
        print("What is your name?")
        send(sock, input())
    elif msg == "move":
        print("Please provide a move in the form [y, x], or enter \"skip\" if you wish to skip your move.")
        process_move()
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
    elif msg == "server-shutdown":
        print("Server has shut down, terminating this client")
        exit(0)
    else:
        print("Malformed server message:")
        print(msg)

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
    elif msg["type"] == "player-update":
        player_update(msg)
    elif msg["type"] == "stat-totals":
        end_game(msg, True)
    else:
        print("Malformed server message:")
        print(msg)

# main loop for client functionality
while True:
    msg = receive(sock)
    if msg != "":
        handle_server_message(msg)