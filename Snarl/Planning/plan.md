# Software Development Plan for Snarl

## Partonomies and Taxonomies
A `Player` will consist of a name and potentially health and attack points, depending on what Growl, Inc. decides they want. It will have functions that allow the player to perform movements and interactions.

An `Adversary` will consist of a type (zombie, ghost, ghoul, etc) and a function that chooses their action for the turn. It may also have health and attack points.

An `Object` will be something that a `Player` or `Adversary` can interact with, or a `Player` or `Adversary` themselves. This will include keys, exits, and potentially other things. `Objects` will have a type and a function that handles interaction with the `Player`/`Adversary`.

A `Tile` will be either a space that a `Player`/`Adversary` can occupy, or it will be a wall. Some tiles will contain an `Object`.

A `Room` will consist of a set of `Tiles`. Some of them will be open spaces and some will be walls, which together form the shape of the room. The layout will be such that a player can move from one doorway to another in the room in order to travel around the dungeon, and one doorway will not be completely cut off from another by walls.

A `Level` will be a collection of `Rooms`. One of these `Rooms` will contain the key to the exit, and one of these rooms will contain the exit. We will consider mandating that the key and the exit be in separate rooms, to keep things interesting.

A `Dungeon` will consist of multiple levels, as well as containing the main function of the software that handles game startup, play, and shutdown. The startup function will generate the levels of the dungeon, allow players to connect, and determine player and adversary spawn locations. 

## Communication Between Components
The `Dungeon` will need to know all the `Player`s and will generate the `Level`s. The `Level`s will know their layout, as well as any `Objects` (`Player`/`Adversary`/`Key`) that are present on their tiles. The Level will allow turns to
be made by giving a `Player` or `Adversary` information about their surrounding Tiles, then receiving the desired action of that entity, and
determining the consequences of that action. If a player goes through the unlocked exit portal, the `Level` will tell the `Dungeon`
that it has been completed, and the `Dungeon` will generate a new `Level` or end the game. 

## Proposed Milestones
- Milestone 1: Implement basic level structure
- Milestone 2: Implement basic player/adversary functions
- Milestone 3: Finish vertical slice containing a small playable level
- Milestone 4: Implement map generation (with adversary placement)
- Milestone 5: Implement adversary AI (and possibly add player AI depending on spec changes)
- Milestone 6: Finish release candidate
- Milestone 7: Finish release