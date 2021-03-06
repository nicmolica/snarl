# Milestone 6 - Refactoring Report

**Team members:**
Nicholas Molica, Ty nichols

**Github team/repo:**
[Nimrasea](https://github.ccs.neu.edu/CS4500-S21/Nimrasea)


## Plan

### `open_tiles` on Room
This field may be unnecessary (or at least very cumbersome) because we have to update it all the time. Perhaps it would be better to bring back Posns so that we have a datatype that we can use simply for identifying locations. This will eliminate the confusion of remembering which Tiles need to be updated and make it clear which fields exist to be read-only and which fields represent the actual Gamestate.

### check all fields of classes and change some to protected if needed
We already changed all methods to protected, but should still go over all fields to make sure they're used correctly (and add getters to ensure mutation safety).

### put `testLevel` methods in Level
Determine which methods from testLevel.py would be helpful to have in Level and move them there. Refactor code in testLevel to import these methods from their new location.

### fix all exceptions to be more appropriate
Right now we pretty much just throw ValueErrors and TypeErrors, so we should define our own exceptions or at the very least raise more appropriate ones.

### Add other predicates for tile occupants to Tile class
Things like `has_character` or `has_adversary` could be pretty useful.

### Proper packaging of files
Right now, neither our source files nor our test files are packaged. This has been causing issues with running tests, as well as making it more difficult to import things from a parent directory in any of our files. We should create packages `Snarl.src` and `Snarl.test` in order to make this easier. We should also figure out how sub-packaging works. 

## Changes
- Created a top-level package inside the `Snarl` folder, and subpackages for subfolders that need imports from other places, such as the `Snarl/tests` scripts. All files have been changed to use imports given this new package structure.
- Changed methods that are only used internally to be marked as "protected" status in all classes via prefixing them with `_`. Did the same for fields, and added getters that copy them to ensure mutation safety.
    - This includes the `open_tiles` field of room, which resolves that issue.
- Added some utility methods (`has_character/has_adversary`) to the Tile class.
- Changed many exceptions to be `RuntimeError`s rather than `ValueErrors`. 
- Moved the `get_adjacent_rooms` method from `testLevel` into `Level`. Also copied over all necessary helpers as "protected" `_` methods.

## Future Work

At this time, we do not have any outstanding refactoring work planned.

## Conclusion

Thanks for the refactoring week!
