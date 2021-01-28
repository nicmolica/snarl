import sys
import json

# Specifies valid flags for the program.
valid_flags = ["--sum", "--product"]

# End program if the user forgot the argument.
if len(sys.argv) == 1:
    print("No operation provided as command-line input!")
    exit(1)

# This should be --sum or --product
flag = sys.argv[1]
# End program if the flag isn't what we expect.
if flag not in valid_flags:
    print("Invalid operation flag" + "'" + flag + "'!")
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
        jsons = jsons[error_index:]
    # When error, cut off a character and try again.
    except(json.decoder.JSONDecodeError):
        # Remove whitespace
        jsons = jsons[1:]

def mult(iter):
    """Multiply all elements of the given iterable, treating strings as unit.

        Parameters:
            iter (iterable): An iterable object.

        Returns:
            prod (number): The product of all entries of iter.
    """
    prod = 1
    for i in iter:
        if type(i) is str:
            i = 1
        prod *= i
    return prod

def sum(iter):
    """Add all elements of the given iterable, treating strings as unit.

        Parameters:
            iter (iterable): An iterable object.

        Returns:
            acc (number): The sum of all entries of iter.
    """
    acc = 0
    for i in iter:
        if type(i) is str:
            i = 0
        acc += i
    return acc

unit = 0 if flag == "--sum" else 1
func = sum if flag == "--sum" else mult

def calculate_total(obj):
    """Calculates the total for the given NumJSON expression; the operation depends
    on the command-line flag that was given by the user.

        Parameters:
            obj (NumJSON): A NumJSON expression.
        
        Returns:
            total (number): The total calculated value for obj.
    """
    if type(obj) is int or type(obj) is float:
        total = obj
    elif type(obj) is list:
        total = func(obj)
    elif type(obj) is str:
        total = unit
    else: #calculate total for payload and ignore other keys in the object.
        total = calculate_total(obj["payload"])
    return total

def process(items):
    """Calculates the total for every NumJSON expression in the list, and returns a
    JSON object representing the total value for each.

        Parameters:
            items (list[NumJSON]): A list of NumJSON expressions.

        Returns:
            processed (list[dict]): A list of JSON objects that store the total value
            for each given NumJSON expression in items. Given a NumJSON expression n,
            the form of each object in this list is {"object": n, "total": calculate_total(n)}
    """
    processed = [] 

    for n in items:
        processed.append({ "object": n, "total": calculate_total(n)})

    return processed

print(process(numjsons))
