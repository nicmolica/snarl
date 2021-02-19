# WARNING: THIS DOCUMENT IS AN UNFINISHED WISHLIST. MAY BE SPLIT INTO MULTIPLE COMPONENTS.
# The GameManager Class

The `GameManager` class runs a game of SNARL. We may want to split some of these methods
up into different components; for example, rather than having a function `move_adversaries`
on the game manager, the main function of the game manager could call a `AdversaryAI.move_adversaries`
function.

This file will be revised later.

## Fields

### `rule_checker: RuleChecker`
Validates player movement and interactions for the game.
Alternatively, we could make a singleton since we really only need one of these,
and it's useful to call it from more than one component. 

### `game_state: GameState`
The current state of the game. This field is modified when game actions occur.

## Methods

### `start_game() -> None`
Begins a game of SNARL. Places all players at the beginning of the first level.

### `get_player_move() -> None`
Gets a move for the current player from STDIN.

### `move_adversaries() -> None`
Moves all the adversaries in the current level.

### `render() -> None`
Returns an ASCII representation of the current game state.

### `begin_next_level() -> None`
Begins the next level of the dungeon. Moves all players to the beginning of the level.
If the game should end, quits the game via `self.quit_game()`. 

### `quit_game() -> None`
Ends the game program. Outputs a message indicating whether or not the players won. 