# Multi-Game Server Design and Implementation

## Design 

Our multi-game server was designed to behave in a nearly identical manner to the existing
SNARL network implementation. We envisioned the process as something like the following:

1. Server starts up, clients connect like normal.
2. Server runs the first game.
3. When first game is over, server "resets" any necessary information in the game manager,
then starts the next game
4. When there are no more games, the server waits for the "exit" command to shut down,
as specified in the milestone 10 description. 

### Command-line Arguments

The new SNARL server takes one additional command-line argument `--games #`,
where `#` is the number of games that the server will run. The default number
is 1. 

### Addition to SNARL Protocol

We added two server messages to the SNARL protocol:

1. `"server-shutdown"`: the server sends this message to the clients after the
server receives the `"exit"` command. The client will display a message that
the server has shut down, and then the client will also shut down. 
2. `{"type": "stat-totals", "scores": (player-score-list)}`: this message is sent at the end of every game, after the `end-game` message in the existing SNARL protocol. The `(player-score-list)` is exactly as specified in the existing protocol as well. This message contains the running total statistics
for each player over all played games. Otherwise, the client displays the statistics in a table just like the single-game statistics that are sent with
the `end-game` message. 

## Implementation
The changes to `snarlServer` were relatively straightforward. All we needed to
do was add a new argument and re-run the manager with a new game. The only 
complication was making sure that any necessary statistics and data that the
game manager stores were reset between games. To achieve this, we added a
`reset_game` method to the game manager that will reset any of the necessary
data as well as allow for a new set of levels to be passed in. However, we
decided to use the same levels for all games in our implementation for the 
sake of simplicity. 

We also had to add support on both the game manager and client for sending and
displaying the running stat total information. This was achieved very simply by
adding a new field to track the data on the game manager, and by re-using the scoreboard
display method on the client. 