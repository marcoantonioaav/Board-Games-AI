from copy import deepcopy
from math import ceil, floor, log
import random

from numpy import Inf
from tictactoe import Game

class Agent:
    def __init__(self, player) -> None:
        self.player = player

    
    def select_action(self, game, context, max_seconds, max_iterations, max_depth):
        pass

    def supports_game(self, game):
        return True
    
    def close_ai(self):
        pass

    def get_opponent(self):
        if self.player == 1:
            return -1
        else:
            return 1

    def get_opponent_of(self, player):
        if player == 1:
            return -1
        else:
            return 1


class RandomAgent(Agent):
    def select_action(self, game, context, max_seconds=0, max_iterations=0, max_depth=0):
        return random.choice(game.moves(context, self.player))


class MinimaxAgent(Agent):
    def get_heuristc_value(self, game, context):
        if game.is_victory(context, self.player):
            return 1
        elif game.is_victory(context, self.get_opponent()):
            return -1
        else:
            return 0
    
    def minimax(self, game, context, depth, maximizingMoveer):
        if depth == 0 or game.is_terminal_state(context):
            return self.get_heuristc_value(game, context), None
        if maximizingMoveer:
            max_value = -Inf
            max_move = None
            for legal_move in game.moves(context, self.player):
                new_context = game.apply(legal_move, context)
                new_value, move = self.minimax(game, new_context, depth - 1, False)
                if new_value > max_value:
                    max_value = new_value
                    max_move = legal_move
            return max_value, max_move
        else:
            min_value = Inf
            min_move = None
            for legal_move in game.moves(context, self.get_opponent()):
                new_context = game.apply(legal_move, context)
                new_value, move = self.minimax(game, new_context, depth - 1, True)
                if new_value < min_value:
                    min_value = new_value
                    min_move = legal_move
            return min_value, min_move

    def select_action(self, game, context, max_second=0, max_iterations=0, max_depth=4):
        value, move = self.minimax(game, context, max_depth, True)
        return move


class SequentialHalvingAgent(Agent):
    def make_playout(self, game, context):
        new_context = deepcopy(context)
        current_player = self.get_opponent()
        while not game.is_terminal_state(new_context):
            move = random.choice(game.moves(context, current_player))
            new_context = game.apply(move, new_context)
            current_player = self.get_opponent_of(current_player)
        if game.is_victory(new_context, self.player):
            return 1
        return 0

    def sequential_halving(self, game, context, budget):
        legal_moves = game.moves(context, self.player)
        moves_dict = []
        for legal_move in legal_moves:
            moves_dict.append({'Move': legal_move, 'Victories': 0, 'Playouts': 0})
        while len(moves_dict) > 1:
            for move_dict in moves_dict:
                new_context = game.apply(move_dict['Move'], context)
                playouts = floor(budget/(len(moves_dict)*ceil(log(len(legal_moves), 2))))
                for i in range(playouts):
                    move_dict['Victories'] += self.make_playout(game, new_context)
                move_dict['Playouts'] += playouts
            moves_dict.sort(key=lambda move_dict: move_dict['Victories']/move_dict['Playouts'])
            moves_dict = moves_dict[floor(len(moves_dict)/2):]
        return moves_dict[0]['Move']

    def select_action(self, game, context, max_seconds=0, max_iterations=0, max_depth=0):
        return self.sequential_halving(game, context, 5000)
