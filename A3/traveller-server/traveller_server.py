import networkx

town_networks = []
network_character_names = []
network_town_names = []

def is_valid_town(town):
    """Checks if the given town has the following key-value pairs:
        'name': str
        'neighbors': list[str]
        'characters': list[str]
    Arguments:
        town (dict): A town represented as a dictionary

    Returns
        is_valid (bool): Is the town a valid town?
    """
    has_keys = 'name' in town and 'neighbors' in town and 'characters' in town
    if not has_keys:
        return False
    else:
        values_are_correct_type = type(town['name']) is str and type(town['neighbors']) is list \
            and type(town['characters']) is list
        if not values_are_correct_type:
            return False

    return True

def create_towns(town_network):
    """Creates a network which is a simple graph and store it in a global variable
    *town_networks*. The simple graph should be represented as a list of towns, and
    each town has the key of name, neighbors and characters.

    The names given in the 'neighbors' lists must be valid town names in the network.
    
    Arguments:
        town_network (list[dict]): list of towns. Each town is a dict containing the
        keys 'name', 'neighbors', and 'characters'.

        {'name': str, 'neighbors': [], 'characters': []}

    Returns:
        None

    Throws:
        ValueError: if the town_network list contains dicts without the required keys,
        or if the given town names are not unique and the given character names are not
        unique.
    """
    if type(town_network) is not list:
        raise TypeError("The town_network email is not a list!")

    if not all([is_valid_town(town) for town in town_network]):
        raise ValueError('Missing keys found in town_network list!')
    
    # Check to see if the towns or characters have duplicate names. If so, raise error.
    town_names = [town["name"] for town in town_network]

    if len(town_names) != len(set(town_names)):
        raise ValueError('Duplicate town names provided!')
    
    character_names = []
    neighbors_names = []
    for town in town_network:
        character_names += town["characters"]
        neighbors_names += town["neighbors"]

    if not set(neighbors_names).issubset(set(town_names)):
        raise ValueError("Some neighboring towns do not exist!")

    if len(character_names) != len(set(character_names)):
        raise ValueError('Duplicate character names provided!')

    global town_networks, network_character_names, network_town_names
    town_networks = town_network
    network_character_names = character_names
    network_town_names = town_names

def place_char(char, town):
    """Takes a named character and a name of the town, and looks up the name of the
    town in the existing network and add that character into the town.

    Arguments:
        char (str): The name of a character to place in town.
        town (str): The name of the town in the network that char should be placed in.

    Returns:
        None

    Throws:
        TypeError: If the character or town name is not a string.
        ValueError: If the given town does not exist in the network, or the given town
        already has a character in it.
    """
    # Check that arguments are of proper type.
    if type(char) is not str:
        raise TypeError('Character name must be a string!')
    if type(town) is not str:
        raise TypeError('Town name must be a string!')

    # Check that the new names will still be unique within the town_network's characters.
    global network_character_names
    new_char_names = network_character_names + [char]

    if len(set(new_char_names)) != len(new_char_names):
        raise ValueError('Character names must be unique!')

    # Check that the town exists and does not have a character in it.
    global network_town_names
    if town not in network_town_names:
        raise ValueError("The town named'" + town + "' is not in the network!")
    
    # Put the character in the town
    global town_networks
    town = next(town_dict for town_dict in town_networks if town_dict['name'] == town)
    town["characters"].append(char)

    # Update the names dictionary with the new name
    network_character_names += char
    

def is_unblocked(char, town):
    """return true if the character with given name is able to find a path to the
    designated town without visiting other characters.

    Arguments:
        char (str): The name of a character to place in town.
        town (str): The name of the town in the network to check if char has a path to.

    Returns:
        has_path (bool): If char can reach town without running into other characters.

    Throws:
        TypeError: If the character or town name is not a string.
        ValueError: If the given town does not exist in the network, or the given town
        already has a character in it.

    """
    # Check that arguments are of proper type.
    if type(char) is not str:
        raise TypeError('Character name must be a string!')
    if type(town) is not str:
        raise TypeError('Town name must be a string!')

    if town not in network_town_names:
        raise ValueError("The town named'" + town + "' is not in the network!")

    # If the town network has no towns there is no path for the character
    if len(town_networks) == 0:
        return False

    g = networkx.Graph()
    for t in town_networks:
        g.add_node(t["name"], characters = t["characters"])
        if char in t["characters"]:
            start_node = t["name"]

    for t in town_networks:
        for neighbor in t["neighbors"]:
            g.add_edge(t["name"], neighbor)

    non_empty_nodes = [name for name, atts in g.nodes(data = True) if len(atts["characters"]) != 0]
    selected_nodes = set(non_empty_nodes) - set([start_node])

    empty_towns = networkx.restricted_view(g, nodes = selected_nodes, edges = [])
    
    return empty_towns.has_node(town) and \
        networkx.has_path(empty_towns, source = start_node, target = town)