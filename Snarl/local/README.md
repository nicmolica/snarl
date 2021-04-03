# How to Play Our Local Snarl

You should be able to run the `localSnarl` executable. It supports the necessary optional flags.
We've attached our default `snarl.levels` file that we used to do testing. For now, because we
are rendering to console, __we support only one player__, which is allowed as per the milestone spec. 

# The Game Interface

Our Snarl renders a grid of ASCI characters representing a level. Here are the meanings of each character:
- ` ` : An empty space. This is traversable by all entities
- `P` : The player
- `|` and `-` : Wall tiles of a room
- `X` : void (impassable) tiles
- `K` : The level key
- `E` : The level exit
- `D` : A room door
- `Z` : A zombie
- `G` : A ghost

The player will be given a 5x5 view of their surroundings. If they are close to the edges of the level,
the view may be accordingly truncated.

If the `--observe` flag is present, the game will render a grid of the whole level, and will _suppress_
player output. The game will still run, and player moves may still be provided, but the normal interface
will disappear in favor of the observer.

Messages will be displayed according to the assignment spec when the player picks up a key, exits the level,
or is expelled. 

# Making Moves
In order to make a move, enter `[x, y]` in the console when prompted. If you make an invalid move, you will
be prompted to re-enter your move. 

If adversaries make an invalid move, their turn is skipped.

If you wish to end the program prematurely, enter `q`. This feature is present for ease of testing, but will
probably be removed in production. 

## Known Issues
Here are the known bugs that we did not have time to fix. For the most part, these
are minor and do not affect functionality.

- When a player makes an invalid move, the error message may be printed twice
- Player is told that they were expelled and exited when they had just exited
- Right after moving to the second level, the Zombie from the first level makes an invalid move
