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

class SHOT(Agent):
    
    #not sure if I update parameters from TTable or from the stack
    #not sure whats node's body (it looks like each node has a list of legal movements)
    def sh_over_trees(board, budget, u_budget, playouts, wins, player):

        legal_moves = tictactoe.list_legal_moves(board, player)
        
        # if is terminal check who the outcome and update variables
        if tictactoe.is_terminal_state(board):
            TTable[board].wins += 1 if tictactoe.is_victory(board, self.player) else 0
            TTable.playouts +=1 # idk why it suposed to update these variables
            return
        
        # if there is only one playout left, roll it and update variables
        if bugdget == 1:
            result = playout(board)
            wins += result
            playouts+=1
            u_budget+=1

            TTable[board].wins += result
            TTable[board].playouts+=1
            TTable[board].u_budget+=1
            budget -= 1
            return

        # if there is only one move to make, make it and then update variables.
        if len(legal_moves) == 1:
            u=0, p=0, w=0
            n_board = tictactoe.make_move(board, legal_moves[0])
            sh_over_trees(n_board, budget, u, p, w, player*-1)
            TTable[n_board].playouts+=1
            TTable[n_board].u_budget+=1
            budget -=1
            # Here I have to update wins but idk how
            return legal_moves[0]


    
        t = TTable[board] # not sure (key?)
        # if there is less legal_moves than playout budgets distribute it beetwen new legal_moves
        if t.budget_node <= len(legal_moves):
            M_zero = [m for m in legal_moves if m not in TTable]
            count = 0
            for m in M_zero:
                count += 1
                n_board = tictactoe.make_move(board, m) 
                result = playout(n_board)
                TTable[n_board].playouts+=1
                TTable[n_board].u_budget+=1
                TTable[n_board].wins += (1 if result == self.player else 0)
                
                if budget == count:
                    break
        sort_moves()

        # Sequential Halving
        b = 0
        while len(legal_moves)>1:
            b = b + max(1, floor( (t.budget_node + budget) / (len(legal_moves)* log(tictactoe.list_legal_moves(board, player)) )
            for m in legal_moves:
                if t.playouts[m] < b:
                    bl = b - t.playouts[m]
                    
                    # ??? idk
                    if t == root and len(legal_moves) == 2 and m == S[0]:
                        bl = budget - u_budget - (b - t.playouts[b[1]])
                    
                        bl = min(bl, budget - budgetUsed)
                    u = 0, p = 0, w = 0
                    n_board = tictactoe.make_move(board, m)
                    sh_over_trees(n_board, bk, u, p, w, agent*-1)
                    playouts += 1
                    u_used += 1
                    # wins = ?
                    # have to update t too
            if u_budget >= budget:
                break
            sort_moves(legal_moves)
            halve(legal_moves)
        #update t.budgetNode
        return legal_moves[0]
