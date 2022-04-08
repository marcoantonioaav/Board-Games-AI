from agents.agent import Agent

class Game:
    class Move:
        pass

    def __init__(self):
        pass

    def get_initial_board(self):
        pass

    def is_victory(self, board, player):
        pass

    def is_draw(self, board):
        pass

    def is_legal_move(self, move:Move, board):
        pass

    def apply(self, move:Move, board):
        pass

    def moves(self, board, player):
        pass

    def is_terminal_state(self, board):
        return self.is_victory(board, Agent.PLAYER_1) or self.is_victory(board, Agent.PLAYER_2) or self.is_draw(board)

    def state_name(self, board):
        if self.is_victory(board, Agent.PLAYER_1):
            return 'Player 1 victory'
        elif self.is_victory(board, Agent.PLAYER_2):
            return 'Player 2 victory'
        elif self.is_draw(board):
            return 'Draw'
        else:
            return 'Ongoing'

    def get_winner(self, board):
        if self.is_victory(board, Agent.PLAYER_1):
            return Agent.PLAYER_1
        elif self.is_victory(board, Agent.PLAYER_2):
            return Agent.PLAYER_2
        else:
            return 0
