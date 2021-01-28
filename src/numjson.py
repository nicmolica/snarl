import sys
import json

# Specifies valid flags for the program.
valid_flags = ["--sum", "--product"]

# This should be --sum or --product
flag = sys.argv[1]

# End program if the flag isn't what we expect.
if flag is None or flag not in valid_flags:
    print("Invalid operation flag" + "'" + flag + "'")
    exit(1)

# This fetches the user input from STDIN and concatenates it into a
jsons = ""
for line in sys.stdin.readlines():
    jsons += line

# Store the original input length because we're going to reference it a lot
original_length = len(jsons)

# Parses the NumJSON from stdin into Python objects.
# This will store the different NumJSON objects
numjsons = []

# Decoder
decoder = json.JSONDecoder()
# Used to record where the decoder stopped. Start at beginning of input.
error_index = 0
while error_index < original_length and len(jsons) > 0:
    try: 
        numjson_obj, error_index = decoder.raw_decode(jsons)
        numjsons.append(numjson_obj)
        print(error_index)
        jsons = jsons[error_index:]
    # When error, cut off a character and try again.
    except(json.decoder.JSONDecodeError):
        # Remove whitespace
        print(len(jsons))
        jsons = jsons[1:]
        print(jsons)

# TODO: Apply the appropriate transform to the objects, then return via STDOUT probably.

# Object -> dict, Array -> list, Number-int
print(type(numjsons[0]) is dict)
print(numjsons)