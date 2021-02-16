# Snarl State Representation

## Data Definitions
- `Level`: This class contains the rooms and hallways that make up the level. It handles checking its own validity (looking for overlaps, connectedness, etc) and rendering itself. It knows when it has been beaten.
- `Room`: This reprents a room. It contains a list of open tiles, as well as its own position, dimensions, and its doors. All tiles that are not open are considered to be non-traversable.
- `Hallway`: This represents a hallway connecting two rooms. Can be 0 tiles long or longer and can optionally contain waypoints. It must connect two doors, and has fields to store the two doors it connects as well as the waypoints between them.
- `Occupant`: This represents any occupant of a tile. Can be a player, adversary, key, or level exit. The `Occupant` class can be inherited by other classes as well to allow for adding other occupants later in development.
- `Tile`: This represents a tile in a level and contains its own coordinates and (optionally) an occupant.

## Wishlist for Game State
The `Gamestate` class will contain multiple levels and will handle all operations that change the state of the game. These include player movements, beating levels, among other things. It will enforce the legality of changes, including ensuring that players don't move out of turn.

```python
class Gamestate:
    levels          # a list of all the levels in this game
    current_level   # the level players are currently playing
    # Move a player from src tile to dest tile. Throw exception for illegal move.
    def move_player(player, src, dest)

    # Move an adversary from src tile to dest tile. Throw exception for illegal move.
    def move_adversary(adversary, src, dest)

    # Move all players to the next level in the game and mark the current level as completed.
    def complete_level()

    # Does this game state represent a finished game?
    def is_game_over()

    # Return a limited portion of the current level in a specific radius around the provided center in the form of a list of lists of actual Tile objects.
    def get_partial_level(radius, center)

    # Return the entire current level in the form of a list of lists of actual Tile objects.
    def get_level()
```