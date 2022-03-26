from copy import deepcopy
from math import ceil, floor, log
import random

from numpy import Inf
import tictactoe

class Agent:
    def __init__(self, player) -> None:
        self.player = player

    def get_move(self, board):
        pass

    def get_opponent(self):
        if self.player == 1:
            return 2
        else:
            return 1

    def get_opponent_of(self, player):
        if player == 1:
            return 2
        else:
            return 1


class RandomAgent(Agent):
    def get_move(self, board):
        return random.choice(tictactoe.list_legal_moves(board, self.player))


class MinimaxAgent(Agent):
    def get_heuristc_value(self, board):
        if tictactoe.is_victory(board, self.player):
            return 1
        elif tictactoe.is_victory(board, self.get_opponent()):
            return -1
        else:
            return 0
    
    def minimax(self, board, depth, maximizingMoveer):
        if depth == 0 or tictactoe.is_terminal_state(board):
            return self.get_heuristc_value(board), None
        if maximizingMoveer:
            max_value = -Inf
            max_move = None
            for legal_move in tictactoe.list_legal_moves(board, self.player):
                new_board = tictactoe.make_move(legal_move, board)
                new_value, move = self.minimax(new_board, depth - 1, False)
                if new_value > max_value:
                    max_value = new_value
                    max_move = legal_move
            return max_value, max_move
        else:
            min_value = Inf
            min_move = None
            for legal_move in tictactoe.list_legal_moves(board, self.get_opponent()):
                new_board = tictactoe.make_move(legal_move, board)
                new_value, move = self.minimax(new_board, depth - 1, True)
                if new_value < min_value:
                    min_value = new_value
                    min_move = legal_move
            return min_value, min_move

    def get_move(self, board):
        value, move = self.minimax(board, 4, True)
        return move


class SequentialHalvingAgent(Agent):
    def make_playout(self, board):
        new_board = deepcopy(board)
        current_player = self.get_opponent()
        while not tictactoe.is_terminal_state(new_board):
            move = random.choice(tictactoe.list_legal_moves(board, current_player))
            new_board = tictactoe.make_move(move, new_board)
            current_player = self.get_opponent_of(current_player)
        if tictactoe.is_victory(new_board, self.player):
            return 1
        return 0

    def sequential_halving(self, board, budget):
        legal_moves = tictactoe.list_legal_moves(board, self.player)
        moves_dict = []
        for legal_move in legal_moves:
            moves_dict.append({'Move': legal_move, 'Victories': 0, 'Playouts': 0})
        while len(moves_dict) > 1:
            for move_dict in moves_dict:
                new_board = tictactoe.make_move(move_dict['Move'], board)
                playouts = floor(budget/(len(moves_dict)*ceil(log(len(legal_moves), 2))))
                for i in range(playouts):
                    move_dict['Victories'] += self.make_playout(new_board)
                move_dict['Playouts'] += playouts
            moves_dict.sort(key=lambda move_dict: move_dict['Victories']/move_dict['Playouts'])
            moves_dict = moves_dict[floor(len(moves_dict)/2):]
        return moves_dict[0]['Move']

    def get_move(self, board):
        return self.sequential_halving(board, 200)

    
