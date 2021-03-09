from occupants import Character

class Player:
    def __init__(self, player_name, character_name):
        self.player_name = player_name
        self.character = Character(character_name)