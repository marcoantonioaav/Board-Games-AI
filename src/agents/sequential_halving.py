from copy import deepcopy
from math import ceil, floor, log
import random
from agents.agent import Agent

import math
class SequentialHalvingAgent(Agent):
    def make_playout(self, context, starting_player):
        new_context = deepcopy(context)
        current_player = starting_player
        while not self.game.is_terminal_state(new_context):
            move = random.choice(self.game.moves(context, current_player))
            new_context = self.game.apply(move, new_context)
            current_player = self.get_opponent_of(current_player)
            
        if self.game.is_victory(new_context, self.player):
            return 1
        elif self.game.is_victory(new_context, self.get_opponent_of(self.player)):
            return -1
        return 0

    def sequential_halving(self, context, budget):
        legal_moves = self.game.moves(context, self.player)
        moves_dict = []
        for legal_move in legal_moves:
            moves_dict.append({'Move': legal_move, 'Victories': 0, 'Playouts': 0})
        while len(moves_dict) > 1:
            for move_dict in moves_dict:
                new_context = self.game.apply(move_dict['Move'], context)
                playouts = floor(budget/(len(moves_dict)*ceil(log(len(legal_moves), 2))))
                for i in range(playouts):
                    move_dict['Victories'] += self.make_playout(new_context, self.get_opponent())
                move_dict['Playouts'] += playouts
            moves_dict.sort(key=lambda move_dict: move_dict['Victories']/move_dict['Playouts'])
            moves_dict = moves_dict[floor(len(moves_dict)/2):]
        return moves_dict[0]['Move']

    def select_action(self, game, context, max_seconds=0, max_iterations=0, max_depth=0):
        return self.sequential_halving(context, 1000)

    def get_name(self):
        return "Sequential Halving Agent"


class ShotAgent(SequentialHalvingAgent):
    def __init__(self) -> None:
        self.transposition_table = {}

    def get_name(self):
        return "SHOT Agent"

    def select_action(self, game, context, max_seconds=0, max_iterations=0, max_depth=0):
        move, b_u, p, w = self.shot(context, 2048, current_player=self.player, at_root=True)
        return move

    def shot(self, board, budget, current_player, budget_used=0, playouts=0, wins=0, at_root=False):
        legal_moves = self.game.moves(board, current_player)
        left_moves = deepcopy(legal_moves)

        if self.game.is_terminal_state(board):        
            updated_wins = wins
            if self.game.is_victory(board, self.player):
                updated_wins += 1
            return None, budget_used, playouts+1, updated_wins # update playouts, wins and return
            
        if budget == 1:
            updated_wins = wins + self.make_playout(board, current_player)
            return left_moves[0], budget_used+1, playouts+1, updated_wins # update playouts, budget_used, wins and return

        if len(left_moves) == 1:
            new_board = self.game.apply(left_moves[0], board)
            move, new_budget_used, new_playouts, new_wins = self.shot(new_board, budget, self.get_opponent_of(current_player))
            return left_moves[0], budget_used+new_budget_used, playouts+new_playouts, wins+new_wins

        t = self.get_entry_in_transposition_table(board, current_player)

        #NOTE: test moves
        if t['budget_node'] <= len(left_moves):
            for move in left_moves:
                if t['playouts'][str(move)] == 0:
                    new_board = self.game.apply(move, board)
                    win = self.make_playout(new_board, self.get_opponent_of(current_player))
                    playouts += 1
                    budget_used += 1
                    wins += win
                    t['victories'][str(move)] += win
                    t['playouts'][str(move)] = 1
                    t['budget_node'] += 1
                    if playouts == budget: #return if budget playouts have been played
                        return move, budget_used, playouts, wins       
        left_moves.sort(key=lambda move: t['victories'][str(move)]/t['playouts'][str(move)])
        b = 0
        while len(left_moves) > 1:
            b += max(1, floor((t['budget_node']+budget)/(len(left_moves)*ceil(log(len(legal_moves), 2)))))
            for m in range(len(left_moves)-1, -1, -1):
                if t['playouts'][str(left_moves[m])] < b:
                    # get budget
                    b1 = b - t['playouts'][str(left_moves[m])]
                    if at_root and len(left_moves) == 2 and m == 0:
                        b1 = budget - budget_used - (b - t['playouts'][str(left_moves[1])])
                    b1 = min(b1, budget - budget_used)
                    # end
                    new_board = self.game.apply(left_moves[m], board)
                    move, new_budget_used, new_playouts, new_wins = self.shot(new_board, b1, self.get_opponent_of(current_player))
                    playouts += new_playouts
                    budget_used += new_budget_used
                    wins += new_wins
                    t['playouts'][str(left_moves[m])] += new_playouts
                    t['victories'][str(left_moves[m])] += new_wins
                    t['budget_node'] += new_budget_used
                if budget_used >= budget:
                    break 
            left_moves.sort(key=lambda move: t['victories'][str(move)]/t['playouts'][str(move)])
            left_moves = left_moves[floor(len(left_moves)/2):]
            if budget_used >= budget:
                break 
        #t['budget_node'] += budget_used
        return left_moves[0], budget_used, playouts, wins

    def get_entry_in_transposition_table(self, board, player):
        if self.transposition_table.keys().isdisjoint([self.get_tt_key(board, player)]):
            playouts_dict = {}
            victories_dict = {}
            for legal_move in self.get_legal_moves(board, player):
                playouts_dict[str(legal_move)] = 0
                victories_dict[str(legal_move)] = 0
            self.transposition_table[self.get_tt_key(board, player)] = {'budget_node': 0, 'playouts': playouts_dict, 'victories': victories_dict}
        return self.transposition_table[self.get_tt_key(board, player)]

    def get_tt_key(self, board, player):
        return str(board)+str(player)

    def get_legal_moves(self, board, player):
        return self.game.moves(board, player)


class ShotTreeAgent(Agent):
    def __init__(self) -> None:
        self.transposition_table = {}

    def get_name(self):
        return "SHOT Tree Agent"

    def select_action(self, game, context, max_seconds=0, max_iterations=0, max_depth=0):
        shot_tree = self.ShotNode(self.transposition_table, self.player, game, context, 2048, current_player=self.player)
        return shot_tree.get_best_move()

    class ShotNode(SequentialHalvingAgent):
        def __init__(self, transposition_table, player, game, board, budget, current_player, father=None) -> None:
            self.father = father
            
            self.transposition_table = transposition_table
            self.player = player
            self.game = game
            self.board = board
            self.budget = budget
            self.current_player = current_player
            
            self.budget_used = 0
            self.playouts = 0
            self.wins = 0
            
            self.legal_moves = self.game.moves(board, current_player)
            self.left_moves = deepcopy(self.legal_moves)
            self.t = self.get_entry_in_transposition_table(self.board, self.current_player)

            self.shot()

        def get_best_move(self):
            if len(self.left_moves) > 0:
                return self.left_moves[0]
            return None

        def shot(self):
            if self.game.is_terminal_state(self.board) or self.budget == 1:        
                self.make_shot_playout()
                return

            if len(self.left_moves) == 1:
                self.expand_tree(self.left_moves[0], self.budget)
                return 

            self.make_one_playout_per_move()
            if self.playouts == self.budget:
                return
                
            b = 0
            while len(self.left_moves) > 1:
                b += max(1, floor((self.t['budget_node']+self.budget)/(len(self.left_moves)*ceil(log(len(self.legal_moves), 2)))))
                for m in range(len(self.left_moves)-1, -1, -1):
                    if self.t['playouts'][str(self.left_moves[m])] < b:
                        # get budget
                        b1 = b - self.t['playouts'][str(self.left_moves[m])]
                        if self.is_at_root() and len(self.left_moves) == 2 and m == 0:
                            b1 = self.budget - self.budget_used - (b - self.t['playouts'][str(self.left_moves[1])])
                        b1 = min(b1, self.budget - self.budget_used)
                        # end
                        self.expand_tree(self.left_moves[m], b1)
                    if self.budget_used >= self.budget:
                        break 
                self.left_moves.sort(key=lambda move: self.t['victories'][str(move)]/self.t['playouts'][str(move)])
                self.left_moves = self.left_moves[floor(len(self.left_moves)/2):]
                if self.budget_used >= self.budget:
                    break 
            #t['budget_node'] += budget_used

        def expand_tree(self, move, sons_budget):
            new_board = self.game.apply(move, self.board)
            son = self.__class__(self.transposition_table, self.player, self.game, new_board, sons_budget, self.get_opponent_of(self.current_player), father=self)
            self.wins += son.wins
            self.budget_used += son.budget_used
            self.playouts += son.playouts
            self.t['playouts'][str(move)] += son.playouts
            self.t['victories'][str(move)] += son.wins
            self.t['budget_node'] += son.budget_used

        def make_one_playout_per_move(self):
            if self.t['budget_node'] <= len(self.left_moves):
                for move in self.left_moves:
                    if self.t['playouts'][str(move)] == 0:
                        self.make_shot_playout(move)
                        if self.playouts == self.budget:
                            return     
            self.left_moves.sort(key=lambda move: self.t['victories'][str(move)]/self.t['playouts'][str(move)])

        def make_shot_playout(self, move=None):
            if move == None:
                new_board = self.board
            else:
                new_board = self.game.apply(move, self.board)
            win = self.make_playout(new_board, self.get_opponent_of(self.current_player))
            self.playouts += 1
            self.budget_used += 1
            self.wins += win
            if move != None:
                self.t['victories'][str(move)] += win
                self.t['playouts'][str(move)] = 1
                self.t['budget_node'] += 1

        def get_entry_in_transposition_table(self, board, player):
            if self.transposition_table.keys().isdisjoint([self.get_tt_key(board, player)]):
                playouts_dict = {}
                victories_dict = {}
                for legal_move in self.legal_moves:
                    playouts_dict[str(legal_move)] = 0
                    victories_dict[str(legal_move)] = 0
                self.transposition_table[self.get_tt_key(board, player)] = {'budget_node': 0, 'playouts': playouts_dict, 'victories': victories_dict}
            return self.transposition_table[self.get_tt_key(board, player)]

        def get_tt_key(self, board, player):
            return str(board)+str(player)

        def is_at_root(self):
            return self.father == None

#monte carlo plano (sequential halving sem halve)
#kiloton