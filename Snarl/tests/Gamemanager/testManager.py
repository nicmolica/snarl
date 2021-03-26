import sys
import json
from Snarl.tests.parseJson import *
from Snarl.src.Game.tile import Tile
from Snarl.src.Game.level import Level
from Snarl.src.Game.enemy import Enemy
from Snarl.src.Game.gamestate import Gamestate
from Snarl.src.Game.gamemanager import Gamemanager
from Snarl.src.Game.player_impl import PlayerImpl
from Snarl.src.Game.utils import grid_to_string
from Snarl.src.Game.occupants import Character, Adversary, LevelKey, LevelExit

test_input = ""
for line in sys.stdin.readlines():
    test_input += line

# per the assignment spec, we can assume that the json is well-formed
name_list, json_level, num_of_turns, locations, turns = json.loads(test_input)

# make all the players
characters = []
for i in range(len(name_list)):
    new_player = {}
    new_player["type"] = "player"
    new_player["name"] = name_list[i]
    new_player["position"] = locations[i]
    characters.append(create_entity_from_json(new_player))

# make the level
level = create_level_from_json(json_level)

# make the gamemanager and start the game
manager = Gamemanager(4, 2, 1)

players = []

class TraceOutput:
    trace = []
    def write(self, s):
        self.trace.append(s)

    def to_json(self):
        """Convert this trace to a JSON representation as given in the
        Milestone 7 spec.
        """
        reformatted_arr = []

        for entry in self.trace:
            if entry["type"] == "update":
                reformatted_arr.append(self._format_update(entry))
            elif entry["type"] == "move-result":
                reformatted_arr.append(self._format_result(entry))
        
        return reformatted_arr
    
    def _format_update(self, update):
        """Formats a notification of new surroundings to JSON.
        """
        name = update["name"]
        layout = create_array_from_layout(update["layout"])
        position = update["position"]
        actors = self._actors_from_layout(update["layout"])
        objects = self._objects_from_layout(update["layout"])

        return [name, { "type": "player-update", "layout": layout, "position": create_dict_from_point(position), \
            "objects":objects, "actors": actors }]

    def _actors_from_layout(self, layout):
        """Gets all the actors in this layout.
        """
        # TODO: remove the actor that the update was sent to from this list
        actors = []
        for row in layout:
            for tile in row:
                on_tile = list(filter(lambda o : isinstance(o, Character) or isinstance(o, Adversary), tile.occupants))
                for actor in on_tile:
                    actors.append((tile, actor))
        
        actor_dicts = []
        for pair in actors:
            tile = pair[0]
            actor = pair[1]
            actor_dicts.append(create_dict_from_entity(actor, tile))
        
        return actor_dicts


    def _objects_from_layout(self, layout):
        """Gets all the actors in this layout.
        """
        objects = []
        for row in layout:
            for tile in row:
                if tile.has_occupant(LevelExit) or tile.has_occupant(LevelKey):
                    objects.append(create_dict_from_object(tile))
        return objects
    
    def _format_result(self, result):
        """Formats a notification of a move result to JSON.
        """
        name = result["name"]
        move = result["move"]
        res = result["result"].value
        return [name, move, res]

trace = TraceOutput()
# register the players
for character in characters:
    player = PlayerImpl(character.name, character.name, trace)
    manager.add_player(player)
    players.append(player)

# start the game
manager.start_game(level)

# move the players to their correct initial locations
for i in range(len(players)):
    manager.game_state.add_character(characters[i], create_point_from_json(locations[i]))

# make the adversaries and add them to the game (they're all zombies right now but this doesn't need to be the case)
adversaries = []
for i in range(len(name_list), len(locations)):
    json_new_adversary = {}
    json_new_adversary["type"] = "zombie"
    json_new_adversary["name"] = "zombie"
    json_new_adversary["position"] = locations[i]
    new_adversary = create_entity_from_json(json_new_adversary)
    adversaries.append(new_adversary)
    level.add_adversary(new_adversary, create_point_from_json(locations[i]))

manager.add_enemies(list(map(lambda adv : Enemy(adv.name, type(adv), adv.name), adversaries)))

# make moves until we've reached the max number of turns
for i in range(num_of_turns):
    turn_list_i = i % len(turns)

    # if we've run out of turns to make or the game is over, we're done
    if len(turns[turn_list_i]) == 0 or manager.rule_checker.is_game_over(manager.game_state):
        break
    # attempt a turn
    player_move_dict = turns[turn_list_i][0]
    to = create_point_from_json(player_move_dict["to"])
    # Skip Enemy moves for now
    while not isinstance(manager.current_turn, PlayerImpl):
        manager.current_turn = manager.turn_order.next()
    turns[turn_list_i].pop(0)
    manager.move(to)
    # print(grid_to_string(manager.render()))
    # print("\n")

state = create_dict_from_state(manager.game_state)
test_result = [state, trace.to_json()]
print(json.dumps(test_result))