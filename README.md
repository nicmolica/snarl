Nicholas Molica (nicmolica) and Ty Nichols (nichols-t), April 2021

# SNARL
SNARL is an ASCII-based command line game developed between January and April 2021. It can support between 1 and 4 players, who can be playing on a single machine or on multiple machines. It is structured like a dungeon crawler game, with zombies and ghosts to avoid, a key to collect, and a dungeon exit to locate.

## Technology Used
Throughout the duration of the project, we used Visual Studio Code as our main development environment and Unix shells as our integration testing environment. With the exception of several very basic Bash scripts, the entire codebase is in Python. We made frequent use of the `json` and `socket` libraries, as well as other general-use libraries.

## Development Process
Ty and I collaborated on the project using the Agile development framework to stay on schedule and deliver features as they were requested. We also both performed and were subject to bi-weekly code reviews by our peers at Northeastern to ensure that our code was high-quality and up to spec.

## How To Run
To run a single player game, open 2 shells. In both shells, navigate to the `Snarl/net` directory and run the command `export PYTHONPATH=$(cd ../../ && pwd)$PYTHONPATH`. In one of the shells, run the command `python3 snarlServer.py --clients 1 --observe` and in the other, run the command `python3 snarlClient.py`. This will start a playable game in the client shell. The `--observe` argument allows you to view the entire level from the server's perspective, since the client will have a restricted view. If desired, you can play with adding more clients or adding remote clients. To run a remote client, you can specify the IP and port of the server using the `--address` and `--port` command line arguments. These are configurable for both the server and client.

## How to Play
Gameplay is relatively simple. Each game consists of a number of levels (the preloaded games only have 2 or 3). You want to pick up the key and use the exit, all while avoiding ghosts and zombies. To do this, you'll need to explore rooms in each level. You can move around by providing the coordinates of the tile you want to move to. Between your turns, other players, zombies and ghosts will have the opportunity to move, but zombies and ghosts can only move a single tile at a time, while you can move up to 2. Ghosts, however, have the ability to randomly teleport to another room as part of their turn! Thankfully, neither ghosts nor zombies can enter a hallway. Once you've collected the key, head to the exit to progress to the next level or end the game. In the ASCII rendering, a Z represents a zombie, a G represents a ghost, a P is you or another player, K is the key, E is the exit, - is a horizontal wall, | is a vertical wall, and X is an impassible tile. These representations will make more sense when you see what the rendering looks like.
