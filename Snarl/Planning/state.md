# Snarl State Representation

```python
# SnarlState provides a data structure used to store all information
# necessary to check validity of Snarl moves and progress the game.
class SnarlState:
    level_tiles: Tile[][][]
    # This 3D list stores the Tiles that make up each level. The first
    # index is the level index, the second is the Cartesian x-index,
    # and the third is the Cartesian y-index. The coordinates begin
    # with the origin in the upper left of the screen.
    
    def is_valid_move(self, level, (start_x, start_y), (end_x, end_y)):
        # On the given level, check if the object at (start_x, start_y)
        # should be allowed to move to the tile at (end_x, end_y) on the
        # same level. 
```

# generate_
- information nece3ssary to check validity of moves and progress the game

