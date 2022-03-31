
from math import ceil, floor, log
import random
from numpy import Inf
import tictactoe
from agents import Agent

class SHOT(Agent):
    __init__(self):
        self.TTable = {}
    #not sure if I update parameters from TTable or from the stack
    #not sure whats node's body (it looks like each node has a list of legal movements)
    def sh_over_trees(self, context, budget, u_budget, playouts, wins, player):

        legal_moves = tictactoe.moves(context, player)
        
        # if is terminal check who the outcome and update variables
        if tictactoe.is_terminal_state(context):
            self.TTable[context].wins += 1 if tictactoe.is_victory(context, self.player) else 0
            self.TTable.playouts +=1 # idk why it suposed to update these variables
            return
        
        # if there is only one playout left, roll it and update variables
        if budget == 1:
            result = self.playout(context)
            wins += result
            playouts+=1
            u_budget+=1

            self.TTable[context].wins += result
            self.TTable[context].playouts+=1
            self.TTable[context].u_budget+=1
            budget -= 1
            return

        # if there is only one move to make, make it and then update variables.
        if len(legal_moves) == 1:
            u=0, p=0, w=0
            n_context = tictactoe.apply(context, legal_moves[0])
            self.sh_over_trees(n_context, budget, u, p, w, player*-1)
            self.TTable[n_context].playouts+=1
            self.TTable[n_context].u_budget+=1
            budget -=1
            # Here I have to update wins but idk how
            return legal_moves[0]


    
        t = self.TTable[context] # not sure (key?)
        # if there is less legal_moves than playout budgets distribute it beetwen new legal_moves
        if t.budget_node <= len(legal_moves):
            M_zero = [m for m in legal_moves if m not in self.TTable]
            count = 0
            for m in M_zero:
                count += 1
                n_context = tictactoe.apply(context, m) 
                result = playout(n_context)
                self.TTable[n_context].playouts+=1
                self.TTable[n_context].u_budget+=1
                self.TTable[n_context].wins += (1 if result == self.player else 0)
                
                if budget == count:
                    break
        sort_moves()

        # Sequential Halving
        b = 0
        while len(legal_moves)>1:
            b = b + max(1, floor( (t.budget_node + budget) / (len(legal_moves)* log(tictactoe.moves(context, player)) )
            for m in legal_moves:
                if t.playouts[m] < b:
                    bl = b - t.playouts[m]
                    
                    # ??? idk
                    if t == root and len(legal_moves) == 2 and m == S[0]:
                        bl = budget - u_budget - (b - t.playouts[b[1]])
                    
                        bl = min(bl, budget - budgetUsed)
                    u = 0, p = 0, w = 0
                    n_context = tictactoe.apply(context, m)
                    sh_over_trees(n_context, bk, u, p, w, agent*-1)
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

