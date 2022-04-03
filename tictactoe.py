from copy import deepcopy
from random import shuffle

class Game:
    def __init__(self):
        str = "gambiarra weeeeeew"
    class Move:
        def __init__(self, x, y, player) -> None:
            self.x = x
            self.y = y
            self.player = player

    def get_initial_board(self):
        return [[0, 0, 0],[0, 0, 0],[0, 0, 0]]

    def apply(self, move:Move, board):
        new_board = deepcopy(board)
        new_board[move.x][move.y] = move.player
        return new_board

    def is_legal_move(self, move:Move, board):
        return board[move.x][move.y] == 0

    def moves(self, board, player):
        moves = []
        for y, line in enumerate(board):
            for x, piece in enumerate(line):
                new_move = self.Move(x, y, player)
                if self.is_legal_move(new_move, board):
                    moves.append(new_move)
        shuffle(moves)
        return moves 

    def is_diagonal_victory(self, board, player):
        return (board[0][0] == board[1][1] == board[2][2] == player) or (board[0][2] == board[1][1] == board[2][0] == player)

    def is_column_victory(self,board, player):
        return (board[0][0] == board[1][0] == board[2][0] == player) or (board[0][1] == board[1][1] == board[2][1] == player) or (board[0][2] == board[1][2] == board[2][2] == player)

    def is_line_victory(self, board, player):
        for line in board:
            if line.count(player) == 3:
                return True
        return False

    def is_victory(self, board, player):
        return self.is_line_victory(board, player) or self.is_column_victory(board, player) or self.is_diagonal_victory(board, player)

    def is_draw(self, board):
        for line in board:
            for piece in line:
                if piece == 0:
                    return False
        return not self.is_victory(board, 1) and not self.is_victory(board, -1)

    def is_terminal_state(self, board):
        return self.is_victory(board, 1) or self.is_victory(board, -1) or self.is_draw(board)

    def state_name(self, board):
        if self.is_victory(board, 1):
            return 'Player 1 victory'
        elif self.is_victory(board, -1):
            return 'Player 2 victory'
        elif self.is_draw(board):
            return 'Draw'
        else:
            return 'Ongoing'

    def get_winner(self, board):
        if self.is_victory(board, 1):
            return 1
        elif self.is_victory(board, -1):
            return -1
        else:
            return 0
