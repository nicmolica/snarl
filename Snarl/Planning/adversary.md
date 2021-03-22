# The Adversary Class

The `Adversary` class represents an adversary in a game of SNARL. It recieves information about the current state from the `Gamemanager` in the form of a grid of
tiles representing the level right before it makes a turn. At the beginning of each level it is given the entire level grid. If adversaries are too powerful in the
finished game, they may be modified to be given less information. 

## Data Types
### `Grid`
This is a list of lists of `Tiles`. It will not be an actual class within our partonomy, but it is referenced for the sake of simplicity throughout this spec document.

## Fields

### `location: Tile`
The current location of the adversary on the level.

### `vicinity: Grid`
A grid of tiles around the `Adversary` in a certain radius. This is provided by a `Gamemanager` and updated every time this `Adversary` is about to move.

### `expelled: bool`
Boolean representing whether or not the `Adversary` has been expelled from the `Level`. This can happen if the adversary is ever removed from the level. Right now,
no game mechanics support this but we expect that some may be added in the future.

## Methods

### `update_surroundings(vicinity: Grid) -> None`
Change the `vicinity`. This method is called by `Gamemanager` right before this `Adversary` moves. We are choosing to represent the level information as a grid
because we expect that the information given to the adversary may be restricted more in the future; representing the level state as a grid allows us to easily
restrict the tiles that this `Adversary` has information about. 

### `relocate(location: Tile) -> None`
Change the `location`. This is called by `Gamemanager` every time the `Adversary` moves.

### `expel() -> None`
Notify the `Adversary` that they've been expelled from the `Level` by updating the `expelled` field to `True`. This method is not used with the current game rules,
but we expect it might be in the future.

### `move() -> Tile`
Returns a `Tile` that this `Adversary` should try to move to. The `Gamemanager` is reponsible for validating and executing the move.