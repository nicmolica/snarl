# The RuleChecker Class

The `RuleChecker` class contains functions that are used for validating SNARL interactions
and movement. 

## Methods

### `is_valid_player_move(src: Tile, dest: Tile, level: Level) -> bool`
Is the player at `src` Tile allowed to move to the given `dest` Tile? A player may move to a tile
that is at most 2 cardinal moves away. The `dest` Tile can be occupied by a key, exit,
adversary, or nothing. 

### `is_valid_adversary_move(src: Tile, dest: Tile, level: Level) -> bool`
Is the adversary at `src` Tile allowed to move to the given `dest` Tile? An adversary may move
to an adjacent tile that is traversable.

### `is_level_over(level: Level) -> (bool, bool)`
Given the current state of the level, is the level over, and did the players win?
Returns a pair of `bool`; the first is if the level is over, the second is if a player reached
the unlocked exit. The level ends when either all players are expelled, or one player
interacts with the unlocked exit. If the player interacted with the unlocked exit,
all players will be moved to the beginning of the next level. 

### `is_game_over(state: GameState) -> (bool, bool)`
Given the current state of the game, is the game over, and did the players win?
Returns a pair of `bool`; the first is if the game is over, the second is if the players won.
The game ends when either the players complete the final level or when
all players are expelled from a level. 