# Traveller
Source Code: traveller.py

This module allows the user to create a simple graph which represents the map of the towns. The user can specify the name of towns, place a named character in a town and knowing if someone can travel from one town to the other without encountering other characters in the path.

 - traveller.**create_towns**(town_network)
Creates a network which is a simple graph and store it in a global variable *town_networks*. The simple graph should be represented as a list of towns, and each town has the key of name, neighbors and characters.

 - traveller.**place_char**(char, town)
Takes a named character and a name of the town, and looks up the name of the town in the existing network and add that character into the town.  

 - traveller.**is_unblocked**(char, town)
return true if the character with given name is able to find a path to the designated town without visiting other characters.
 