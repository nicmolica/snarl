# The `Observer` Class

The `Observer` class observes a `Gamemanager` for the purpose of debugging SNARL and presenting a game to stakeholders. This class recieves information about the `Gamestate` through the `Gamemanager` and processes it so that it's easily useable for these purposes.

## Fields

### `gamestate: Gamestate`
The `gamestate` field will be the only field in this class. It will be a copy of the `Gamestate` managed by the `Gamemanager` this `Observer` is observing. The `Gamestate` class already has methods for extracting information, such as `get_tiles()` and `get_tiles_range()`, so methods in this class will be able to use this field to get all the information they need.

## Methods

### `notify(gamestate: Gamestate)`
This is essentially a setter. It sets the `gamestate` field of this `Observer` object to the current `Gamestate` of the `Gamemanager` that is being observed. This will be called every time there is a change to the `Gamestate` so that the `Observer` will always have up-to-date information.

### `render()`
Returns an ASCII representation of the current `Gamestate`. This is useful for displaying the game to stakeholders. It also means that the game visualization can be easily sent to an external server, if so desired.

### `transmit_view(ip: str)`
Given an IP address, creates a socket that transmits the current view of the `Gamestate` to a server. It obtains the current view by calling the `render()` method. This view may be either total or partial, depending on what the `Observer` ends up being used for.

# Changes to `Gamemanager`

The fields and methods enumerated below are also in the spec for `Gamemanager` (in the game-manager.md file), but are here as well to make it easier to see which methods the `Gamemanager` class uses to be observed by `Observer`s. The information below only includes things added to accomodate `Observer`s; it excludes all fields and methods that `Gamemanager` already had.

## Fields

### `observers: list`
A list of `Observer`s observing this `Gamemanager`.

## Methods

### `register_observer(observer: Observer)`
Adds the provided `Observer` to the list of `Observers` this `Gamemanager` needs to update each time there's a change.

### `notify_observers()`
Loop through all the registered `Observer`s and update them about changes to the `Gamestate` via their `notify()` methods.