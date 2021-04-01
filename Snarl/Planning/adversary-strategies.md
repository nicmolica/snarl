# Ghost Movement Strategies

The ghost should always move towards the nearest player within 10 units. If no player is within 1/5 of the longest dimenions of the level,
 the ghost runs into a wall in order to be teleported to a random room. The ghost cannot move on top of another Actor, the level key, 
 or the level exit.

## Examples

### Example 1: Move Towards Player
```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
|         | X X X X X X X X X X X |               |
|      P  D   G                   D               |
|         | X X X X X X X X X X X |               |
- - - - - - X X X X X X X X X X X - - - - - - - - -
```

In the above example, since the player is within 5 units, the ghost will move towards the player like so:

```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
|         | X X X X X X X X X X X |               |
|      P  D G                     D               |
|         | X X X X X X X X X X X |               |
- - - - - - X X X X X X X X X X X - - - - - - - - -
```

### Example 2: Move Into Wall
```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
|         | X X X X X X X X X X X |               |
|      P  D                       D               |
|         | X X X X X X X X X X X | G             |
- - - - - - X X X X X X X X X X X - - - - - - - - -
```

In the above example, since the player is further than 5 units away, the ghost will move into a wall, hoping to be
teleported closer to the player:

```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
|         | X X X X X X X X X X X |               |
|      P  D                       D               |
|         | X X X X X X X X X X X G               |
- - - - - - X X X X X X X X X X X - - - - - - - - -
```

This will then move the ghost into a random room:
```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
|         | X X X X X X X X X X X |               |
|      P  D                       D               |
|   G     | X X X X X X X X X X X |               |
- - - - - - X X X X X X X X X X X - - - - - - - - -
```

# Zombie Movement Strategies

A zombie moves toward the nearest player inside its own room. If there is no player within its own room, it moves
in a random valid cardinal direction. The zombie cannot move on top of another Actor, the level key, 
 or the level exit.

## Examples

### Example 1: Move Towards Player
```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
|    Z    | X X X X X X X X X X X |               |
|      P  D                       D               |
|         | X X X X X X X X X X X |               |
- - - - - - X X X X X X X X X X X - - - - - - - - -
```

In the above example, since the player is in the same room as the zombie,
the zombie will move towards the player:

```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
|         | X X X X X X X X X X X |               |
|    Z P  D G                     D               |
|         | X X X X X X X X X X X |               |
- - - - - - X X X X X X X X X X X - - - - - - - - -
```

### Example 2: Move Randomly
```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
|         | X X X X X X X X X X X |               |
|      P  D                       D               |
|         | X X X X X X X X X X X | Z             |
- - - - - - X X X X X X X X X X X - - - - - - - - -
```

In the above example, since the player is not in the same room as the zombie,
the zombie will pick a random valid cardinal direction to move in:

```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
|         | X X X X X X X X X X X |               |
|      P  D                       D Z             |
|         | X X X X X X X X X X X |               |
- - - - - - X X X X X X X X X X X - - - - - - - - -
```