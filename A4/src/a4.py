import sys
import socket
import subprocess
import json

# defaults for the host, port and username
host = "127.0.0.1"
port = 8000
username = "Glorifrir Flintshoulder"

# read command line input if user specified host, port or username
if len(sys.argv) > 2:
    username = sys.argv[2]
elif len(sys.argv) > 1:
    port = sys.argv[1]
elif len(sys.argv) > 0:
    host = sys.argv[0]

# Recieve a message from the server by looping on recv
# until the message constitutes a valid JSON object.
def recieve(sock):
    response = ""
    while True:
        packet = sock.recv(8192)
        response = response + packet.decode('utf-8')
        try:
            json.loads(response)
            break
        except:
            pass
    return response

# def read_json_input():
    # user_input = ""
#     for line in sys.stdin:
#         if :
            
#             break
#     return user_input

# Transform the user input for network creation
# into a valid create command to send to the server.
def transform_create_cmd(cmd):
    create_cmd = json.loads(cmd)
    output = {"roads": create_cmd["params"], "towns": []}
    for road in create_cmd["params"]:
        if road["to"] not in output["towns"]:
            output["towns"].append(road["to"])
        if road["from"] not in output["towns"]:
            output["towns"].append(road["from"])
    return output


# open a server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # try to connect to server, throw error and exit if unsuccessful
    try:
        sock.connect((host, port))
    except:
        print("Failed to connect to the server")
        exit(1)

    # startup steps
    sock.sendall(username.encode())
    session_id = recieve(sock)
    # recieve network spec from user
    # send create request to server

    # processing phase
    while True:
        print("Enter JSON input:")
        json_input = read_json_input()
        sock.sendall(json_input.encode())

        # keep reading from server until a newline character is found
        response = recieve(sock)
        print(response)

    # shutdown steps
    