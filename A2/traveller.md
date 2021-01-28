## Data Definitions

The `Town` class contains two instance variables `name` and `character`. The value of the `'name'` attribute is a string representing the name of the town. The value of the `'character'` attribute is one of `None` or a `Character`.

`Character` is a class that has an instance variable `name`, which is a string representing the name of a character. 

## The TownNetworkInterface Methods

### `createTownNetwork(towns : list[Town], roads : list[(str, str)]) -> TownNetwork`
When given a list of `Town` objects and a list of pairs of strings, produces
a TownNetwork that contains the given towns and the given roads between them. 

This function will throw a `TypeError` when:
- `towns` is not a list, or contains an element that is not an instance of `Town`.
- `roads is not a list, or contains an element that is not of the form `(str, str)`.

This function will throw a `ValueError` when:
- `roads` contains a pair with a string that is not equal to the `name` of 
any town in `towns`.

### `addCharacterToTown(character : Character, town_name : str) -> None`
When given a `Character` object and a string representing a town name, modifies
the TownNetwork so that the given character is present in the given town.

This function will throw a `TypeError` when:
- `character` is not an instance of `Character`, or `town_name` is not a string.

This function will throw a `ValueError` when:
- `town_name` is not the name of a town in the TownNetwork.

### `reachableWithoutCollision(character_name : str, town_name : str) -> bool`
When given a string representing a character name and a string representing a
town name, returns whether or not it is possible for the given character to reach the given town without running into other characters.

This function returns false when the destination town contains a different character. 

This function will throw a `TypeError` when:
- `character_name` or `town_name` are not strings.

This function will throw a `ValueError` when:
- `character_name` does not correspond to a character in the TownNetwork.
- `town_name` does not correspond to a town in the TownNetwork.