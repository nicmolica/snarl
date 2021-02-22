# The RuleChecker Class

The `RuleChecker` class contains functions that are used for validating SNARL interactions and movement.

## Methods

### `is_valid_player_move(src: Tile, dest: Tile, level: Level) -> bool`
Is the player at `src` Tile allowed to move to the given `dest` Tile? A player may move to a tile that is at most 2 cardinal moves away. The `dest` Tile can be occupied by a key, exit, adversary, or nothing. 

### `is_valid_adversary_move(src: Tile, dest: Tile, level: Level) -> bool`
Is the adversary at `src` Tile allowed to move to the given `dest` Tile? An adversary may move to an adjacent tile that is traversable.

### `is_level_over(level: Level) -> bool`
Given the current state of the level, is the level over? A level is over if the key has been applied to the exit and a player has used the exit.

### `is_game_over(state: GameState) -> bool`
Given the current state of the game, is the game over? A game is over if the last level is over.

### `did_players_win(state: GameState) -> bool`
Given the current state of the game, did the players win? This function assumes that the game has ended. The players win if there are still players alive after the game has ended.

### `is_open_tile(tile: Tile, entity_type: Type)`
Is the given tile open for an entity of type `enitity_type` to move to? It is open if there is not a player, wall or block on that tile already.