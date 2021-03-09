# The Character Class

The `Character` class represents a human player in a game of SNARL. It recieves limited information from the `Gamemanager` and only works as a very simple interface between the human and the game. Its view is restricted to a certain number of tiles in all directions, but it knows its absolute position within the current `Level`.

## Data Types
### `Grid`
This is a list of lists of `Tiles`. It will not be an actual class within our partonomy, but it is referenced for the sake of simplicity throughout this spec document.

## Fields

### `location: Tile`
The current location of the player on the level.

### `vicinity: Grid`
A grid of tiles around the `Character` in a certain radius. This is provided by a `Gamemanager` and updated every time there's a change to the `Gamestate`.

### `expelled: bool`
Boolean representing whether or not the `Character` has been expelled from the `Level`. This can happen when the `Character` is killed by an `Adversary`. This field is modified by the `Gamemanager`.

## Methods

### `update_surroundings(vicinity: Grid) -> None`
Change the `vicinity`. This happens every time there's a change to the `vicinity` of the `Character` in the `Gamestate` and every time the `Character` moves.

### `relocate(location: Tile) -> None`
Change the `location`. This happens every time the `Character` moves.

### `expell() -> None`
Notify the `Character` that they've been expelled from the `Level` by updating the `expelled` field to `True`.

### `move() -> Tile`
Takes input from the human player and passes it back to the `Gamemanager` in the form of a `Tile` that the `Character` wants to move to.

### `interact() -> bool`
Asks the human player if they would like to interact and returns their decision to the `Gamemanager`. This method may end up being deprecated depending on the finalized rules of the game.