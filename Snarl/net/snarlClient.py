import sys
import socket
import argparse

parser = argparse.ArgumentParser(description = "socket connection info")
parser.add_argument("--address", type = str, nargs = 1)
parser.add_argument("--port", type = int, nargs = 1)
args = parser.parse_args()

args.address = args.address[0] if not args.address == None else "127.0.0.1"
args.port = args.port[0] if not args.port == None else 45678

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((args.address, args.port))

def receive():
    msg = ''
    packet = None
    while packet != b'':
        packet = sock.recv(8192)
        msg = msg + packet.decode('utf-8')
    return msg

def send(msg):
    sock.sendall(msg.encode())

def process_move(move):
    """ Verify that a user-entered move has valid syntax before sending it to the server.
    """
    # TODO
    pass

def start_level(msg):
    """ Let the player know that we've started a new level and give them the relevant information.
    """
    # TODO
    pass

def end_level(msg):
    """ Let the player know that we've ended the level and give them the relevant information.
    """
    # TODO
    pass

def end_game(msg):
    """ Let the player know that we've ended the game and give them the relevant information.
    """
    # TODO
    pass

def player_update(msg):
    """ Update the player on what the dungeon looks like after another entity has made a move.
    """
    # TODO
    pass

def handle_string(msg):
    """ Deal with server messages that are only a single string, rather than dicts.
    """
    if msg == "name":
        print("What is your name?")
        send(input())
    elif msg == "move":
        print("Please provide a move in the form [x, y], or enter \"skip\" if you wish to skip your move.")
        process_move(input())
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
        # TODO change this to raise an exception or something

def handle_server_message(msg):
    if isinstance(msg, str):
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
        # TODO change this to raise an exception or something

# main loop for client functionality
while True:
    msg = receive()
    handle_server_message(msg)