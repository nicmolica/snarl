from .occupants import Character

class Player:
    def __init__(self, player_name, character_name):
        self.player_name = player_name
        self.character = Character(character_name)
        self.expelled = False
        self.surroundings = None

    def move(self):
        """Given the current state of their surroundings, get a move from this
        player and return the coordinates of the desired move.
        """
        # TODO: Implement later; per milestone spec this can be a stub for now.
        pass

    def update_surroundings(self, grid):
        """Send a new grid of surrounding tiles to this player.
        """
        self.surroundings = grid

    def expel(self):
        """Tell this player that they were expelled from the level.
        """
        self.expelled = True

    def __hash__(self):
        return hash((self.player_name, self.character))
    
    def __eq__(self, other):
        if not isinstance(other, Player):
            return false
        return self.player_name == other.player_name and self.character == other.character