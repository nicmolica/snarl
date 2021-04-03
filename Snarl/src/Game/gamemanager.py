import random
from .gamestate import Gamestate
from .rulechecker import Rulechecker
from .occupants import Entity, Character, Adversary
from .turnorder import Turnorder
from .level import Level
from .enemy import Enemy
from .tile import Tile
from .player import Player
from .enemy_zombie import EnemyZombie
from .enemy_ghost import EnemyGhost
import math
from .utils import grid_to_string
from .moveresult import Moveresult
from .player_impl import PlayerImpl
from .observer import Observer 

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
        first_zombie = EnemyZombie("Zombie", "Zomb")
        self.add_enemies(first_zombie)
        for enemy in self.enemy_list:
            enemy_spawn = self.game_state.get_random_spawn_tile()
            self.game_state.add_adversary(enemy.entity, enemy_spawn)
                    
    def get_move(self) -> Tile:
        """ Determine the type of the entity currently moving and get the move they want to make.
        """
        if not self.game_state:
            raise RuntimeError("Cannot call get_move when the game has not started!")
        if isinstance(self.current_turn, PlayerImpl):
            return self.get_player_move()
        elif isinstance(self.current_turn, Enemy):
            return self.get_enemy_move()
        else:
            raise TypeError("You're trying to move something that isn't a character or an adversary.")

    def get_player_move(self) -> Tile:
        """ Receive the next move from a player either from STDIN or from some other entry
        method/client.
        """
        if not self.game_state:
            raise RuntimeError("Cannot call get_player_move when the game has not started!")
        current_player = next(player for player in self.player_list if player.name == self.current_turn.name)
        if current_player is None:
            raise RuntimeError("Attempted to get player move from a player who does not exist!")
        return current_player.move()

    def get_enemy_move(self) -> Tile:
        """ Receive the next move from an adversary either from STDIN or from some other entry
        method/client.
        """
        if not self.game_state:
            raise RuntimeError("Cannot call get_enemy_move when the game has not started!")
        current_enemy = next(enemy for enemy in self.enemy_list if enemy.name == self.current_turn.name)
        if current_enemy is None:
            raise RuntimeError("Attempted to get a move from a nonexistent enemy!")
        return current_enemy.move()

    def update_players(self):
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
                self.update_player(player)

    def update_player(self, player: PlayerImpl, update_grid = None):
        """Sends an update notification to a single player.
        """
        grid = update_grid if update_grid is not None else \
            self.game_state.get_character_surroundings(player.entity, self.view_distance)
        try: 
            position = self.game_state.get_entity_location(player.entity)
        except:
            position = None
        player.notify({"type":"update", "layout": grid, \
                    "position": position, "name": player.name })

    def render(self) -> str:
        """ Return an ASCII representation of the current game state.
        """
        if not self.game_state:
            raise RuntimeError("Cannot call render when the game has not started!")

        return self.game_state.render()

    def quit_game(self):
        """ Quit the game.
        """
        # TODO: Implement later; per milestone spec this can be a stub for now.
        if not self.game_state:
            raise RuntimeError("Cannot call quit_game when the game has not started!")

    def add_player(self, player: Player):
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

    def register_observer(self, observer: Observer):
        """ Register a new Observer by adding it to the list of observers.
        """
        self.observers.append(observer)

    def notify_observers(self):
        """ Notify all Observers of a change to the Gamestate.
        """
        for observer in self.observers:
            observer.notify(self.game_state)

    def move(self, move: Tile):
        """ Determine if the provided move is valid. If so, perform it.
        """
        if not self.game_state:
            raise RuntimeError("Cannot call move when the game has not started!")
        if issubclass(type(self.current_turn), Adversary):
            current_enemy = next(enemy for enemy in self.enemy_list if enemy.name == self.current_turn.name)
            self.notify_adversary(current_enemy)
        # Players that are alive before this move
        pre_players = self.game_state.get_current_characters()
        if not self.game_state.is_character_expelled(self.current_turn.entity) and \
            not self.current_turn.entity in self.game_state.get_completed_characters(): 
            if move != None:
                unlocked_before_move = self.game_state.is_current_level_unlocked()
                try:
                    self.rule_checker.is_valid_move(self.current_turn.entity, move, self.game_state.current_level)
                    self.game_state.move(self.current_turn.entity, move)
                    result = self._get_move_result(unlocked_before_move)
                    self.current_turn.notify(self._format_move_result_notification(move, result))
                except Exception as e:
                    result = self._get_move_result(unlocked_before_move, e)
                    self.current_turn.notify(self._format_move_result_notification(move, result, e))
            else:
                self.current_turn.notify(self._format_move_result_notification(None, Moveresult.OK))
            # Notify players and adversaries of changes to the gamestate, including players who were killed
            # on this turn. Note that this usually results in one rendering per move to all entities.
            self.update_players()
            self.update_adversaries()
            post_players = self.game_state.get_current_characters()
            self.notify_killed_players(list(set(pre_players).difference(set(post_players))))
        self.current_turn = self.turn_order.next()
    
    def notify_killed_players(self, chars_to_notify):
        """Notifies the players of the characters that have died that they are dead.
        """
        players = [player for player in self.player_list if player.entity in chars_to_notify]
        for player in players:
            player.notify(self._format_move_result_notification(None, Moveresult.EJECT, name=player.name))

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

    def update_adversaries(self):
        """Send game state updates to the adversaries.
        """
        for enemy in self.enemy_list:
            self.notify_adversary(enemy)

    def notify_adversary(self, enemy):
        """Sends update to a single adversary.
        """
        loc = self.game_state.get_entity_location(enemy.entity)
        enemy.notify({"state": self.game_state, "loc": loc})

    def notify_players_endgame(self):
        for player in self.player_list:
            self.update_player(player, self.game_state.get_tiles())
        lvls_complete = self.game_state.num_levels_completed
        won = not self.game_state.all_players_expelled()
        failed_in = lvls_complete + 1
        # TODO : Keep track of player keys; for now, not broken bc only one player locally.
        notify = {"type": "end", "won": won, "failed-in": failed_in}
        for player in self.player_list:
            player.notify(notify)

    def next_level(self):
        """ Switch to the next level.
        """
        if not self.game_state:
            raise RuntimeError("Cannot call begin_next_level when the game has not started!")

        # switch the gamestate to the next level and iterate the level counter
        try:
            self.game_state.next_level()
            self.level_num += 1
        except IndexError:
            return

        # add all the characters to the new level
        for c in self.game_state.characters:
            self.game_state.current_level.add_character(c, self.game_state.current_level.random_spawn_tile())
        
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

    def run(self):
        """ Main game loop.
        """
        if not self.game_state:
            raise RuntimeError("Cannot call run when the game has not started!")
        
        # set initial current turn
        self.current_turn = self.turn_order.next()
        # send initial player updates.
        self.update_players()
        self.update_adversaries()
        self.notify_observers()
        while not self.rule_checker.is_game_over(self.game_state):
            valid_move = False
            while not valid_move:
                try:
                    move = self.get_move()
                    self.move(move)
                    valid_move = True
                except Exception as e:
                    self.current_turn.notify({"type": "error", "error": e})
                    if isinstance(self.current_turn, Enemy):
                        print(f"Enemy {self.current_turn.name} provided invalid move: {e}")
                        self.current_turn = self.turn_order.next()
                        #raise e
            if self.game_state.is_current_level_completed() and not self.rule_checker.is_game_over(self.game_state):
                self.next_level()
                self.update_players()
                self.update_adversaries()
            self.notify_observers()
        
        # TODO: Send endgame information
        self.notify_players_endgame()
