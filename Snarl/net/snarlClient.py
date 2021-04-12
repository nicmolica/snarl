import sys
import socket
import argparse
import json

parser = argparse.ArgumentParser(description = "socket connection info")
parser.add_argument("--address", type = str, nargs = 1)
parser.add_argument("--port", type = int, nargs = 1)
args = parser.parse_args()

args.address = args.address[0] if not args.address == None else "127.0.0.1"
args.port = args.port[0] if not args.port == None else 45678

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((args.address, args.port))

def receive():
    packet = sock.recv(32768)
    msg = packet.decode('utf-8')
    return msg

def send(msg):
    sock.sendall(msg.encode())

def process_move():
    """ Verify that a user-entered move has valid syntax before sending it to the server.
    """
    valid_input = False
    input_json = None
    while not valid_input:
        input_json = json.loads(requested_input)
        if type(input_json) == list and len(input_json) == 2:
            valid_input = True
    x, y = input_json
    send(json.dumps([x, y]))


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
    print(f'Level has ended. Player {msg["key"]} picked up the key.')
    print(f'Players {exited} exited the level.')
    print(f'Players {ejected} were ejected from the level.')

def end_game(msg):
    """ Let the player know that we've ended the game and give them the relevant information.
    Expects message of the form:
    { "type": "end-game",
    "scores": (player-score-list)
    }
    (player-score-list) is a list of
    { "type": "player-score",
    "name": (name),
    "exits": (natural),
    "ejects": (natural),
    "keys": (natural)
    }
    """
    print("Game has ended.")
    print("PLAYER NAME      EXITS   KEYS    EJECTS")
    for player in sorted(msg["scores"], key=lambda p : float(str(p["exits"]) + str(p["keys"]))):
        print(f'{player["name"]}                {player["exits"]}   {player["keys"]}    {player["ejects"]}')

def print_layout(layout, objects, actors, position):
    """Given a tile layout, a list of objects, a list of actors, and the player's position,
    render an ASCII grid representing the layout.
    """
    # Convert object indices relative to player indices. Player should be in the middle of the
    # layout.
    def transform_coords(o):
        absolute_posn = o["position"]
        new_y = position[0] - absolute_posn[0] + 2
        new_x = position[1] - absolute_posn[1] + 2
        o["position"] = [new_y, new_x]
        return o
    object_posns = list(map(objects, transform_coords))
    actor_posns = list(map(actors, transform_coords))
    for row in range(len(layout)):
        for col in range(len(row)):
            # Do we need to render the player?
            if row == 2 and col == 2:
                print("P")
                break
            # Do we need to render an actor?
            for actor in actor_posns:
                if actor["position"] == [row, col]:
                    if actor["type"] == "player":
                        print("O")
                    elif actor["type"] == "zombie":
                        print("Z")
                    elif actor["type"] == "ghost":
                        print("G")
                    break
            # Do we need to render an object?
            for obj in object_posns:
                if obj["position"] == [row, col]:
                    if obj["type"] == "key":
                        print("K")
                    elif obj["type"] == "exit":
                        print("E")
                    break
            
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
    message = msg["message"]
    print(f'You are now at [{position[0]}, {position[1]}]')
    print_layout(layout, objects, actors, position)
    if message is not none:
        print(message)
    pass

def handle_string(msg):
    """ Deal with server messages that are only a single string, rather than dicts.
    """
    if msg == "name":
        print("What is your name?")
        send(input())
    elif msg == "move":
        print("Please provide a move in the form [x, y], or enter \"skip\" if you wish to skip your move.")
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
    else:
        print("Malformed server message:")
        print(msg)
        raise RuntimeError(f"Invalid server message: {msg}")

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
        pass
    elif msg["type"] == "start-level":
        start_level(msg)
    elif msg["type"] == "end-level":
        end_level(msg)
    elif msg["type"] == "end-game":
        end_game(msg)
    elif msg["type"] == "player-update":
        player_update(msg)
    else:
        print("Malformed server message:")
        print(msg)
        raise RuntimeError(msg)

# main loop for client functionality
while True:
    msg = receive()
    handle_server_message(msg)