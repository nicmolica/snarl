# The Gamemanager Class

The `Gamemanager` class runs a game of SNARL. It initiates the game with a single provided `Level`, and handles the logic of deciding when `Level`s are generated thereafter. It also handles turn order for both `Character`s and `Adversary`s.

## Fields

### `view_distance: int`
A constant value that defines how far away a player can see from their current position, in any direction. For example, if the value of `view_distance` is 2, then the player can see 2 tiles up, down, to the left and to the right.

### `rule_checker: Rulechecker`
Tool to check player movements and interactions for validity before performing them.

### `game_state: Gamestate`
The current state of the game. This field is modified when game actions occur.

### `num_of_levels: int`
The number of `Level`s in the game. This field may be removed pending future spec changes.

### `turn_order: list`
A list of `Entity`s in the order in which they move. `Entity`s can be added/removed from this list as they are spawned into or expelled from the level. This list will be used cyclically.

### `current_turn: Entity`
The `Entity` whose turn it currently is. This will change with every turn.

### `player_list: list`
A list of players in this game. This list will only be added to when players join the game, and will only be removed from if players leave the game, which may or may not be allowed.

### `observers: list`
A list of `Observer`s observing this `Gamemanager`.

## Methods

### `start_game() -> None`
Begins a game of SNARL. Places all players at the beginning of the first level.

### `get_player_move() -> None`
Gets a move for the current player from STDIN.

### `move_adversaries() -> None`
Moves all the adversaries in the current level.

### `update_players() -> None`
Update all the players about changes to the `Gamestate`. This method is called every time a move is made or an interaction occurs to ensure that all players have an up-to-date view.

### `render() -> None`
Returns an ASCII representation of the current game state.

### `begin_next_level() -> None`
Begins the next level of the dungeon. Moves all players to the beginning of the level. If the game should end, quits the game via `self.quit_game()`. 

### `quit_game() -> None`
Ends the game program. Outputs a message indicating whether or not the players won. 

### `add_character(player: Character) -> bool`
Adds a `Character` to the game. Returns False if unsuccessful because the game is full or for any other reason. Adds the `Character` to the turn order.

### `register_observer(observer: Observer)`
Adds the provided `Observer` to the list of `Observers` this `Gamemanager` needs to update each time there's a change.

### `notify_observers()`
Loop through all the registered `Observer`s and update them about changes to the `Gamestate` via their `notify()` methods.