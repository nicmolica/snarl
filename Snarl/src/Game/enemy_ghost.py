from .enemy import Enemy
from .occupants import Ghost

class EnemyGhost(Enemy):
    def __init__(self, enemy_name : str, entity_name : str) -> None:
        super().__init__(enemy_name, Ghost, entity_name)

    def _move_with_input(self, input_func):
        """Returns a player move given the input string representing the player
        input.
        """
        requested_input = input_func()
        input_json = json.loads(requested_input)
        if not type(input_json) == list or len(input_json) != 2:
            raise RuntimeError("User move input not valid: " + requested_input)
        x, y = input_json
        return Tile(x, y)
    
    def _determine_move(self):
        pass