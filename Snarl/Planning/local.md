```
+-----------------------------+                +-----------+             +-----------------+         +----------------------+
|                             |                |           |             |                 |         |                      |
|       Dungeon Manager       |                |   Level   |             |     Player(s)   |         |     Adversaries      |
|                             |                |           |             |                 |         |                      |
+--------------+--------------+                +-----+-----+             +--------+--------+         +-----------+----------+
               | start game                          |                            |                              |
               |         generate level              |                            |                              |
               +------------------------------------>+begin turn sequence         |                              |
               |                                     |send surroundings           |                              |
               |                                     +--------------------------->+                              |
               |                                     |           send destination |                              |
               |                                     +<---------------------------+                              |
               |                                     |determine effect of player  |                              |
               |                                     |movement                    |                              |
               |                                     |send level info and object  |                              |
               |                                     |locations                   |                              |
               |                                     +---------------------------------------------------------->+
               |                                     |                            |            send destination  |
               |                                     +<----------------------------------------------------------+
               |                                     |determine effect of         |                              |
               |                                     |adversary movement          |                              |
               ...                                   ...                          ...                            ...
               |                 send level complete |if a player reaches exit:   |                              |
               +<------------------------------------+                            |                              |
               |         start new level             |                            |                              |
               +------------------------------------>+                            |                              |
               ...                                   ...                          ...                            ...
               |if all levels complete:              |                            |                              |
               |end game                             |                            |                              |
               +                                     +                            +                              +
```