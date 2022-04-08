class Agent:
    PLAYER_1 = 1
    PLAYER_2 = -1

    def __init__(self) -> None:
        pass

    def set_player(self, player):
        self.player = player

    def set_game(self, game):
        self.game = game
    
    def select_action(self, game, context, max_seconds, max_iterations, max_depth):
        pass

    #def supports_game(self, game):
    #    return True
    
    #def close_ai(self):
    #    pass

    def get_opponent(self):
        if self.player == self.PLAYER_1:
            return self.PLAYER_2
        else:
            return self.PLAYER_1

    def get_opponent_of(self, player):
        if player == self.PLAYER_1:
            return self.PLAYER_2
        else:
            return self.PLAYER_1

