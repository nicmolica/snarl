# Starting the Server

To start the server, run the `snarlServer` executable with the appropriate command line arguments.

# Starting the Client

To start the client, run the `snarlClient` executable with the appropriate arguments.
To interact with the client, you will be prompted for a name, and then for moves when it is your turn.
The name should be provided without quotes. Please note that you may not select a name that another
player has already claimed.

When giving moves, give them in the form `[y, x]`. If your move is not a valid format, it will not
be sent. If it is a valid format, but not a legal move, the server will prompt you for another move.
You may type `skip` in order to skip your move.

When an actor in the game moves, if you are still in the level you will receive an update about your
surroundings. We render with the following characters: 
- walls and impassable tiles as `X`
- players as `P`
- zombies as `Z`
- ghosts as `G`
- doors as `D`
- keys as `K`
- exits as `E`
- empty traversable tiles as '` `'

Your player will always be in the center of this 5x5 view.