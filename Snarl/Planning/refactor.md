# Refactoring Wish List

### `open_tiles` on Room
This field may be unnecessary (or at least very cumbersome) because we have to update it all the time. Perhaps it would be better to bring back Posns so that we have a datatype that we can use simply for identifying locations. This will eliminate the confusion of remembering which Tiles need to be updated and make it clear which fields exist to be read-only and which fields represent the actual Gamestate.

### put `testLevel` methods in Level
Determine which methods from testLevel.py would be helpful to have in Level and move them there. Refactor code in testLevel to import these methods from their new location.

### fix all exceptions to be more appropriate
Right now we pretty much just throw ValueErrors and TypeErrors, so we should define our own exceptions or at the very least raise more appropriate ones.

### Add other predicates for tile occupants to Tile class
Things like `has_character` or `has_adversary` could be pretty useful. 

### Proper packaging of files
Right now, neither our source files nor our test files are packaged. This has been causing issues with running tests, as well as making it more difficult to import things from a parent directory in any of our files. We should create packages `Snarl.src` and `Snarl.test` in order to make this easier. We should also figure out how sub-packaging works. 