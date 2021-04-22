import random
from .gamestate import Gamestate
from .rulechecker import Rulechecker
from .occupants import Entity, Character, Adversary
from .turnorder import Turnorder
from .level import Level
from .enemy import Enemy
from .tile import Tile
from .player import AbstractPlayer
from .enemy_zombie import EnemyZombie
from .enemy_ghost import EnemyGhost
import math
from .utils import grid_to_string
from .moveresult import Moveresult
from .player_impl import Player
from .observer import AbstractObserver 
import traceback

class Gamemanager:
    def __init__(self, max_players: int = 4, view_distance: int = 2, num_of_levels: int = 1, levels : list = []):
        if view_distance >= 1:
            self.view_distance = view_distance
        else:
            raise ValueError("Invalid view distance: " + str(view_distance))

        if num_of_levels >= 1:
            self.num_of_levels = num_of_levels
        else:
            raise ValueError("Invalid number of levels: " + str(num_of_levels))

        if max_players >= 1:
            self.max_players = max_players
        else:
            raise ValueError("Invalid number of players: " + str(max_players))

        self.rule_checker = Rulechecker()
        # This is populated when the game is started.
        self.game_state = None
        self.turn_order = Turnorder([])
        self.current_turn = None
        self.player_list = []
        self.enemy_list = []
        self.observers = []
        self.init_levels = levels
        self.level_num = 1

    def start_game(self, level: Level):
        """ Begin the game by placing all the players in the top left room of the first level.
        """
        # Initialize game state and begin
        self.game_state = Gamestate(level, len(self.player_list), 1, self.init_levels)
        for player in self.player_list:
            spawn_tile = self.game_state.get_random_spawn_tile()
            self.game_state.add_character(player.entity, spawn_tile)
        # First level has one zombie and no ghosts
        first_zombie = EnemyZombie("zombie", "zombie")
        self.add_enemies(first_zombie)
        for enemy in self.enemy_list:
            enemy_spawn = self.game_state.get_random_spawn_tile()
            self.game_state.add_adversary(enemy.entity, enemy_spawn)

    def add_player(self, player: AbstractPlayer):
        """ Register a new player to the game and add it to the correct spot in the turn order.
        """
        if player in set(self.player_list.copy()):
            raise ValueError("Cannot have duplicate players in a game!")
        elif len(self.player_list) == self.max_players:
            raise RuntimeError("Cannot add more than " + str(self.max_players) + " players to a game!")
        
        self.player_list.append(player)
        self.turn_order.add(player)

    def add_enemies(self, enemies):
        """ Add all the provided adversaries to the enemy_list field and put them in the correct
        place in the turn order list.
        """
        if isinstance(enemies, Enemy):
            self.enemy_list.append(enemies)
            self.turn_order.add(enemies)
        elif all([isinstance(enemy, Enemy) for enemy in enemies]):
            for enemy in enemies:
                self.enemy_list.append(enemy)
                self.turn_order.add(enemy)
        else:
            raise TypeError("All enemies must be of the type \"Enemy.\"")

    def register_observer(self, observer: AbstractObserver):
        """ Register a new Observer by adding it to the list of observers.
        """
        self.observers.append(observer)

    def _get_move(self) -> Tile:
        """ Determine the type of the entity currently moving and get the move they want to make.
        """
        if not self.game_state:
            raise RuntimeError("Cannot call get_move when the game has not started!")
        if isinstance(self.current_turn, Player):
            return self._get_player_move()
        elif isinstance(self.current_turn, Enemy):
            return self._get_enemy_move()
        else:
            raise TypeError("You're trying to move something that isn't a character or an adversary.")

    def _get_player_move(self) -> Tile:
        """ Receive the next move from a player either from STDIN or from some other entry
        method/client.
        """
        if not self.game_state:
            raise RuntimeError("Cannot call get_player_move when the game has not started!")
        current_player = next(player for player in self.player_list if player.name == self.current_turn.name)
        if current_player is None:
            raise RuntimeError("Attempted to get player move from a player who does not exist!")
        return current_player.move()

    def _get_enemy_move(self) -> Tile:
        """ Receive the next move from an adversary either from STDIN or from some other entry
        method/client.
        """
        if not self.game_state:
            raise RuntimeError("Cannot call get_enemy_move when the game has not started!")
        current_enemy = next(enemy for enemy in self.enemy_list if enemy == self.current_turn)
        if current_enemy is None:
            raise RuntimeError("Attempted to get a move from a nonexistent enemy!")
        return current_enemy.move()

    def _update_players(self):
        """ Update all the players about changes to the Gamestate surrounding them. This
        happens every time any player moves or there is an interaction that could change
        the way the level looks.
        """
        if not self.game_state:
            raise RuntimeError("Cannot call update_players when the game has not started!")
        for player in self.player_list:
            # Do not update a player that has exited or been expelled from the level
            if not self.game_state.is_character_expelled(player.entity) and not \
                player.entity in self.game_state.get_completed_characters():
                self._update_player(player)

    def _update_player(self, player: Player, update_grid = None):
        """Sends an update notification to a single player.
        """
        grid = update_grid if update_grid is not None else \
            self.game_state.get_character_surroundings(player.entity, self.view_distance)
        try: 
            position = self.game_state.get_entity_location(player.entity)
        except:
            position = None

        tile1, tile2 = self.game_state.get_character_view_range(player.entity, self.view_distance)
        actors = self.game_state.actors_in_range(tile1, tile2)
        actors = list(filter(lambda a: not a[1] == player.entity, actors))
        player.notify({"type": "update", "layout": grid, \
                    "position": position, "name": player.name, \
                    "objects": self.game_state.objects_in_range(tile1, tile2), \
                    "actors": actors, "message": None, "hitpoints": player.entity.hitpoints})

    def _notify_observers(self):
        """ Notify all Observers of a change to the Gamestate.
        """
        for observer in self.observers:
            observer.notify(self.game_state)

    def _move_and_update(self, move):
        """Check that the move is valid, execute it, notify the player, and update the player's score if
        necessary.
        """
        unlocked_before_move = self.game_state.is_current_level_unlocked()
        self.rule_checker.is_valid_move(self.current_turn.entity, move, self.game_state.current_level)
        self.game_state.move(self.current_turn.entity, move)
        result = self._get_move_result(unlocked_before_move)
        if result != Moveresult.EJECT and result != Moveresult.EXIT:
            self.current_turn.notify(self._format_move_result_notification(move, result))
        self._update_scoreboard(result)

    def _move(self, move: Tile):
        """ Determine if the provided move is valid. If so, perform it.
        """
        if not self.game_state:
            raise RuntimeError("Cannot call move when the game has not started!")
        # Adversaries are supposed to be notified of new info right before they move.
        if issubclass(type(self.current_turn), Enemy):
            current_enemy = next(enemy for enemy in self.enemy_list if enemy.entity.name == self.current_turn.entity.name)
            self._notify_adversary(current_enemy)
        # Players that are alive before this move
        pre_players = self.game_state.get_current_characters()
        completed_before_turn = self.game_state.get_completed_characters()
        if move != None:
            self._move_and_update(move)
        else:
            self.current_turn.notify(self._format_move_result_notification(None, Moveresult.OK))
        # Notify players and adversaries of changes to the gamestate, including players who were killed
        # on this turn. Note that this usually results in one rendering per move to all entities.
        self._update_players()
        self._update_adversaries()
        self._handle_completed_characters(completed_before_turn)
        self._handle_killed_players(pre_players)
        self.current_turn = self.turn_order.next()

    def _handle_completed_characters(self, completed_before_turn):
        """Notifies the characters that they exited the level, and removes them from the turn order.
        """
        completed_after_turn = self.game_state.get_completed_characters().copy()
        completed_chars = list(set(completed_after_turn).difference(set(completed_before_turn)))
        players = [player for player in self.player_list if player.entity in completed_chars]
        for player in players:
            player.notify(self._format_move_result_notification(None, Moveresult.EXIT))
            self.turn_order.eject(player)

    def _update_scoreboard(self, result):
        """ Update the scoreboard of the player whose turn it is to reflect the given move result.
        """
        if result == Moveresult.KEY:
            self.current_turn.keys_collected += 1
        elif result == Moveresult.EXIT:
            self.current_turn.successful_exits += 1
    
    def _notify_killed_players(self, players_to_notify):
        """Notifies the given list of players that they got killed.
        """
        for player in players_to_notify:
            player.notify(self._format_move_result_notification(None, Moveresult.EJECT, name=player.name))

    def _update_killed_players_eject_count(self, players_to_update):
        """Adds 1 to the times_ejected field of the given players.
        """
        for player in players_to_update:
            player.times_ejected += 1
    
    def _remove_killed_chars_from_turn_order(self, chars_to_remove):
        """Remove all of the given characters from the turn order.
        """
        for character in chars_to_remove:
            self.turn_order.eject(character)

    def _handle_killed_players(self, pre_chars):
        """Notifies the players of the characters that have died that they are dead, updates the players'
        times_ejected field, and removes the characters from the turn order.
        """
        post_chars = self.game_state.get_current_characters().copy()
        post_chars.extend(self.game_state.get_completed_characters())
        killed_chars = list(set(pre_chars).difference(set(post_chars)))
        players = [player for player in self.player_list if player.entity in killed_chars]
        self._notify_killed_players(players)
        self._update_killed_players_eject_count(players)
        self._remove_killed_chars_from_turn_order(players)
        
    def _format_move_result_notification(self, move, result, err = None, name = None):
        """Given a move result for hte current player, format a notification to send to
        that player' Actor.
        """
        return {"type": "move-result", "result": result, \
            "move" : {"type": "move", "to": None if move == None else [move.y, move.x]}, \
                "name": name if name is not None else self.current_turn.entity.name, \
                    "error": str(err) if err != None else None}

    def _get_move_result(self, unlocked_before_move : bool, err = None):
        """Gets the result of the current move
        """
        if err:
            return Moveresult.INVALID
        elif self.current_turn.entity in self.game_state.get_completed_characters():
            return Moveresult.EXIT
        elif self.game_state.is_character_expelled(self.current_turn.entity):
            return Moveresult.EJECT
        elif self.game_state.is_current_level_unlocked() and not unlocked_before_move:
            return Moveresult.KEY
        else:
            return Moveresult.OK

    def _update_adversaries(self):
        """Send game state updates to the adversaries.
        """
        for enemy in self.enemy_list:
            self._notify_adversary(enemy)

    def _notify_adversary(self, enemy):
        """Sends update to a single adversary.
        """
        loc = self.game_state.get_entity_location(enemy.entity)
        enemy.notify({"state": self.game_state, "loc": loc})

    def _notify_players_endgame(self):
        for player in self.player_list:
            if player.entity in self.game_state.current_level.characters:
                self._update_player(player, self.game_state.get_tiles())
        end_game = {"type": "end-game", "scores": [], "won": self.rule_checker.did_players_win(self.game_state)}
        for player in self.player_list:
            end_game["scores"].append({"type": "player-score", "name": player.name, "exits": player.successful_exits, \
                "ejects": player.times_ejected, "keys": player.keys_collected})
        for player in self.player_list:
            player.notify(end_game)

    def _notify_level_end(self):
        """Notifies actors of a level's ending.
        """
        exits = self.game_state.get_completed_characters()
        all_characters = list(map(lambda p : p.entity, self.player_list))
        key_picked_up_by = self.game_state.get_level_unlocked_by()
        key = None if key_picked_up_by == None else key_picked_up_by.name
        ejects = set(all_characters) - set(exits) - set(self.game_state.get_current_characters())
        ejects = list(ejects)
        # Get only the names for the notification
        ejects = list(map(lambda c : c.name, ejects))
        exits = list(map(lambda c : c.name, exits))
        notification = {"type":"end-level", "key": key, "exits": exits, "ejects": ejects}
        for player in self.player_list:
            player.notify(notification)

    def _notify_level_start(self):
        """Notifies players of the beginning of a new level. Also sends a player update notification
        with the new surroundings.
        """
        player_names = list(map(lambda p : p.name, self.player_list))
        notification = {"type":"start-level", "level":self.level_num, "players":player_names}
        for player in self.player_list:
            player.notify(notification)
            self._update_player(player)

    def _next_level(self):
        """ Switch to the next level.
        """
        if not self.game_state:
            raise RuntimeError("Cannot call begin_next_level when the game has not started!")

        self._notify_level_end()
        # switch the gamestate to the next level and iterate the level counter
        try:
            self.game_state.next_level()
            self.level_num += 1
        except IndexError:
            return

        # add all the characters to the new level
        for c in self.game_state.characters:
            random_spawn_tile = self.game_state.get_random_spawn_tile()
            self.game_state.current_level.add_character(c, random_spawn_tile)
        
        # create new adversaries
        zombies = []
        ghosts = []
        for i in range(math.floor(self.level_num / 2) + 1):
            zombies.append(EnemyZombie("zombie", "zombie"))
        for i in range(math.floor((self.level_num - 1) / 2)):
            ghosts.append(EnemyGhost("ghost", "ghost"))

        # reset the turn order, update enemy_list, add enemies to gamestate
        self.turn_order = Turnorder([])
        self.enemy_list = []
        for player in self.player_list:
            self.turn_order.add(player)
        for zombie in zombies:
            self.turn_order.add(zombie)
            self.enemy_list.append(zombie)
            spawn = self.game_state.get_random_spawn_tile()
            self.game_state.add_adversary(zombie.entity, spawn)
        for ghost in ghosts:
            self.turn_order.add(ghost)
            self.enemy_list.append(ghost)
            spawn = self.game_state.get_random_spawn_tile()
            self.game_state.add_adversary(ghost.entity, spawn)
        
        self._notify_level_start()
        self.current_turn = self.turn_order.next()

    def run(self):
        """ Main game loop.
        """
        if not self.game_state:
            raise RuntimeError("Cannot call run when the game has not started!")
        
        # set initial current turn
        self.current_turn = self.turn_order.next()
        # send initial player updates.
        self._update_players()
        self._update_adversaries()
        self._notify_observers()
        while not self.rule_checker.is_game_over(self.game_state):
            valid_move = False
            while not valid_move:
                try:
                    move = self._get_move()
                    self._move(move)
                    valid_move = True
                except Exception:
                    if isinstance(self.current_turn, Enemy):
                        self.current_turn = self.turn_order.next()
            if self.game_state.is_current_level_completed() and not self.rule_checker.is_game_over(self.game_state):
                self._next_level()
                self._update_players()
                self._update_adversaries()
            self._notify_observers()
        
        self._notify_players_endgame()
