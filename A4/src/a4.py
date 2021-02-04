#!/usr/bin/env python3
import sys
import socket
import json

# defaults for the host, port and username
host = "localhost"
port = 8000
username = "Glorifrir Flintshoulder"

# read command line input if user specified host, port or username
if len(sys.argv) > 3:
    username = sys.argv[3]
elif len(sys.argv) > 2:
    port = sys.argv[2]
elif len(sys.argv) > 1:
    host = sys.argv[1]

# Recieve a message from the server by looping on recv
# until we find a newline. Complain if it's invalid JSON.
def recieve(sock):
    response = ""
    while response == "" or response[len(response) - 1] != "\n":
        packet = sock.recv(8192)
        response += packet.decode('utf-8')
    try:
        json.loads(response)
    except:
        print("Message from server is invalid JSON")
        exit(1)
    return response

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
    return json.dumps(output)

def transform_batch_cmds(cmds):
    # should already be list of jsons
    batch_req = { "characters": [], "query": {}}
    for json_cmd in cmds:
        cmd_type = json_cmd["command"]
        cmd_params = json_cmd["params"]
        if cmd_type == "place":
            batch_req["characters"].append( \
                {"name": cmd_params["character"], \
                    "town": cmd_params["town"]})
        elif cmd_type == "passage-safe?":
            batch_req["query"]["character"] = cmd_params["character"]
            batch_req["query"]["destination"] = cmd_params["town"]
    return json.dumps(batch_req)

def process_response(response, character_request):
    response_json = json.loads(response)
    for invalid_item in response_json["invalid"]:
        print('["invalid placement", ' + json.dumps(invalid_item) + ']')
    
    request_json = json.loads(character_request)["params"]
    print('["the response for", { "character" : ' + request_json["character"] + \
         ', "destination" : ' + request_json["town"] + '} , "is", ' + \
             json.dumps(response_json["response"]) + ']')

def print_not_request(json_input):
    print('{"error" : "not a request", "object" : ' + json_input.strip() + ' }')

def startup(sock):
    sock.sendall(username.encode())
    session_id = recieve(sock)
    print('["the server will call me", ' + session_id.strip() + ']')
    print("Please enter JSON for road network:")
    valid = False
    create_cmd = ""
    while not valid:
        try:
            json_input = sys.stdin.readline()
            create_cmd = transform_create_cmd(json_input)
            valid = True
        except:
            print_not_request(json_input)
    
    sock.sendall(create_cmd.encode())

def validate_batch_cmd(json_input):
    try:
        dict_input = json.loads(json_input)
        is_cmd = "command" in dict_input and "params" in dict_input
        params = dict_input["params"]
        has_params = type(params) is dict and "character" in params and "town" in params
        is_place = dict_input["command"] == "place" and has_params
        is_safe = dict_input["command"] == "passage-safe?" and has_params
        return is_place or is_safe
    except:
        return False

def process(sock):
    batch = []
    for line in sys.stdin:
        cmd = ""
        valid = False
        while not valid:
            json_input = sys.stdin.readline()
            valid = validate_batch_cmd(json_input)
            if not valid:
                print_not_request(json_input)

        batch.append(json.loads(cmd))

        if json.loads(cmd)["command"] == "passage-safe?":
            sock.sendall(transform_batch_cmds(batch).encode())
            response = recieve(sock)
            process_response(response, cmd)
            batch = []

def shutdown(sock):
    sock.close()

# open a server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # try to connect to server, throw error and exit if unsuccessful
    try:
        sock.connect((host, port))
    except:
        print("Failed to connect to the server")
        exit(1)

    # run the three phases of the program
    # (startup steps, processing phase, shutdown steps)
    startup(sock)
    process(sock)
    shutdown(sock)
