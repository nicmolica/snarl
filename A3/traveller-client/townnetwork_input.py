import sys
import json
import townnetwork

# This fetches the user input from STDIN and concatenates it into a
jsons = ""
for line in sys.stdin.readlines():
    jsons += line

# Store the original input length because we're going to reference it a lot
original_length = len(jsons)

# Parses the NumJSON from stdin into Python objects.
# This will store the different NumJSON objects
commands = []

# Decoder
decoder = json.JSONDecoder()
# Used to record where the decoder stopped. Start at beginning of input.
error_index = 0
while error_index < original_length and len(jsons) > 0:
    try:
        command_obj, error_index = decoder.raw_decode(jsons)
        commands.append(command_obj)
        jsons = jsons[error_index:]
    # When error, cut off a character and try again.
    except(json.decoder.JSONDecodeError):
        # Remove whitespace
        jsons = jsons[1:]

def is_command_valid(command):
    """Checks if the command is valid. Requires that command is a dictionary with keys
    'command' and 'params'.

    Arguments:
        command (dict): dictionary that is hopefully a valid command of the form
        {"command":... , "params":... }
    
    Returns:
        is_valid (bool): If the command is valid.
    """
    return type(command) is dict and "command" in command and "params" in command

# Check if commands are valid
# If any command is not a dictionary with the correct keys, shut down
if any([not is_command_valid(command) for command in commands]):
    print("Invalid command given!")
    exit(1)

# First command must be roads
if len(commands) == 0 or commands[0]["command"] != "roads":
    print("First command must be creation of the town network!")
    exit(1)

# Create the town network from the first command
our_network = townnetwork.TownNetwork()
creation_command = commands[0]
creation_params = creation_command["params"]
if type(creation_params) is not list:
    print("'roads' command must have array for params!")
    exit(1)

towns = []
roads = []
for road in creation_params:
    towns.append(townnetwork.Town(road["from"]))
    towns.append(townnetwork.Town(road["to"]))
    roads.append((road["from"], road["to"]))
towns = list(set(towns))
roads = list(set(roads))

our_network.createTownNetwork(towns, roads)

# Execute the appropriate command based on the command type
for command in commands[1:]:
    # Don't let town creation happen more than once.
    command_type = command["command"]
    if command_type == "roads":
        print("Town network may only be created as the first command!")
        exit(1)
    
    if command_type == "place":
        params = command["params"]
        if "character" not in params or "town" not in params:
            print("'place' command must have character and town params")
            exit(1)
        char = townnetwork.Character(params["character"])
        our_network.addCharacterToTown(char, params["town"])

    elif command_type == "passage-safe?":
        params = command["params"]
        if "character" not in params or "town" not in params:
            print("'passage-safe?' command must have character and town params")
            exit(1)
        char = townnetwork.Character(params["character"])
        our_network.reachableWithoutCollision(char, params["town"])
    
    else:
        print("Invalid command given!")
        exit(1)
