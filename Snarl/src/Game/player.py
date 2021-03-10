from occupants import Character

class Player:
    def __init__(self, player_name, character_name):
        self.player_name = player_name
        self.character = Character(character_name)

    def move(self):
        # TODO: Implement later; per milestone spec this can be a stub for now.
        pass

    def update_surroundings(self, grid):
        # TODO: Implement later; per milestone spec this can be a stub for now.
        pass