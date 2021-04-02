# Ghost Movement Strategies

The ghost should move towards the nearest player within 10 units. The ghost will not attempt to move through walls in order
to get closer to the player unless it has no move which can bring it closer to the player. If no player is within 10 tiles, the ghost runs
into a wall in order to be teleported to a random room. The ghost cannot move on top of another Actor, the level key, or the level exit.

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

### Example 3: Move Around Wall
```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
|         | G X X X X X X X X X X |               |
|       P D                       D               |
|         | X X X X X X X X X X X |               |
- - - - - - X X X X X X X X X X X - - - - - - - - -
```

In the above example, the ghost has 2 moves that could take it closer to the player, but it does not
want to run into the wall and potentially be teleported away. So it chooses the move that does not
run into a wall: 

```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
|         | X X X X X X X X X X X |               |
|      P  D G                     D               |
|         | X X X X X X X X X X X G               |
- - - - - - X X X X X X X X X X X - - - - - - - - -
```

### Example 4: Cannot Move Closer To Player
```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
|       P | G X X X X X X X X X X |               |
|         D                       D               |
|         | X X X X X X X X X X X |               |
- - - - - - X X X X X X X X X X X - - - - - - - - -
```

In the above example, the ghost has 1 move that does not take it farther away from the player.
However, this move will land the ghost onto a wall. Since it does not have any other moves that could
take it closer, the ghost moves onto the wall and is teleported to a random room:

```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
|      P  | G X X X X X X X X X X |               |
|         D                       D               |
|         | X X X X X X X X X X X |               |
- - - - - - X X X X X X X X X X X - - - - - - - - -
```
```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
|      P  | X X X X X X X X X X X |               |
|         D                       D               |
|         | X X X X X X X X X X X | G             |
- - - - - - X X X X X X X X X X X - - - - - - - - -
```
Notice that this may not the optimal strategy for the ghost; it could have chosen to move farther away,
towards the room door. However, we feel that making adversaries slightly simpler and more greedy is acceptable.

### Example 5: Move Onto Door
```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
|       P | X X X X X X X X X X X |               |
|         D G                     D               |
|         | X X X X X X X X X X X |               |
- - - - - - X X X X X X X X X X X - - - - - - - - -
```

In the above example, the ghost can move onto the room door in order to get closer to the player:

```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
|      P  | X X X X X X X X X X X |               |
|         G                       D               |
|         | X X X X X X X X X X X |               |
- - - - - - X X X X X X X X X X X - - - - - - - - -
```

### Example 6: Move Onto BLock Aside Hallway
```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
|         | X X X X X X X X X X X |               |
|         D                 X X x |               |
|         | X X X X X X X   X X X |               |
- - - - - - X X X X X X X G X X X |               |
X X X X X X X X X X X X X   X X X |               |
X X X X X X X X X X X X X         D               |
X X X X X X X X X X X X X X X X X - - - - - - - - -
```

In the above example, the ghost will move towards the nearest wall; in this case, that tile will be the blocked
tile on the edge of the hallway:

```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
|         | X X X X X X X X X X X |               |
|         D                 X X x |               |
|         | X X X X X X X   X X X |               |
- - - - - - X X X X X X X   G X X |               |
X X X X X X X X X X X X X   X X X |               |
X X X X X X X X X X X X X         D               |
X X X X X X X X X X X X X X X X X - - - - - - - - -
```

The ghost will be teleported to a random room:

```
- - - - - - X X X X X X X X X X X - - - - - - - - - 
|         | X X X X X X X X X X X |               |
| G       | X X X X X X X X X X X |               |
|         D                 X X x |               |
|         | X X X X X X X   X X X |               |
- - - - - - X X X X X X X   X X X |               |
X X X X X X X X X X X X X   X X X |               |
X X X X X X X X X X X X X         D               |
X X X X X X X X X X X X X X X X X - - - - - - - - -
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