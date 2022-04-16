from copy import deepcopy
from math import ceil, floor, log
import random
from agents.agent import Agent


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

    def select_action(self, game, context, max_seconds=0, max_iterations=2000, max_depth=0):
        return self.sequential_halving(context, max_iterations)

    def get_name(self):
        return "Sequential Halving Agent"


'''
transposition_table structure:
    key: boardHash + player
    values:
        budget_node: int
        playouts: dictionary
                [
                    key: legal_move
                    values: int
                ]
        victories: dictionary
                [
                    key: legal_move
                    values: int
                ]
'''

class ShotAgent(SequentialHalvingAgent):
    def __init__(self) -> None:
        self.transposition_table = {}

    def shot(self, board, budget, current_player, budget_used=0, playouts=0, wins=0, at_root=False):
        legal_moves = self.game.moves(board, current_player)
        moves = deepcopy(legal_moves)

        # terminal state: verify if its a win and return updated variables
        if self.game.is_terminal_state(board):        
            updated_wins = wins
            if self.game.is_victory(board, self.player):
                updated_wins += 1
            return None, budget_used, playouts+1, updated_wins # update playouts, wins and return
            
        # budget is over: only 1 playout left, make it and return the result
        if budget == 1:
            updated_wins = wins + self.make_playout(board, current_player)
            return moves[0], budget_used+1, playouts+1, updated_wins # update playouts, budget_used, wins and return

        # only one move: make it and return whats the new values
        if len(moves) == 1:
            new_board = self.game.apply(moves[0], board)
            move, new_budget_used, new_playouts, new_wins = self.shot(new_board, budget, self.get_opponent_of(current_player))
            return moves[0], budget_used+new_budget_used, playouts+new_playouts, wins+new_wins

        # check if it needs to add a new node to the transposition table * I think it adds only when has already more than one playout
        
        if self.transposition_table.keys().isdisjoint([str(board)+str(current_player)]):
            playouts_dict   = {}
            victories_dict  = {}
            for legal_move in legal_moves:
                playouts_dict[str(legal_move)]  = 0
                victories_dict[str(legal_move)] = 0
            self.transposition_table[str(board)+str(current_player)] = {'budget_node': 0, 'playouts': playouts_dict, 'victories': victories_dict}
        t = self.transposition_table[str(board)+str(current_player)]

        # if the budget is less then the number of legal moves, start to roll playouts only with moves not tried yet
        if t['budget_node'] <= len(moves):
            for move in moves:
                if t['playouts'][str(move)] == 0:
                    
                    new_board   = self.game.apply(move, board)
                    win         = self.make_playout(new_board, self.get_opponent_of(current_player))
                    playouts    += 1
                    budget_used += 1
                    wins        += win
                    t['victories'][str(move)]   += win
                    t['playouts'][str(move)]     = 1
                    t['budget_node']            += 1
                    
                    if playouts == budget: #return if budget playouts have been played
                        return move, budget_used, playouts, wins   

        moves.sort(key=lambda move: t['victories'][str(move)]/t['playouts'][str(move)])
        
        current_budget = 0  # total budget that each move m in moves M should include

        # Sequential Halving
        while len(moves) > 1:
            # current_budget considers the already allocated budget t['budget_node'] and the budget parameter
            # Victor: não sei o que o 2 faz em math.floor mas se for um valor minimo não faz sentido ter min entre (1,2)
            current_budget += max(1, floor((t['budget_node']+budget)/(len(moves)*ceil(log(len(legal_moves), 2)))))
            
            for m in range(len(moves)-1, -1, -1):

                if t['playouts'][str(moves[m])] < current_budget:
                    #  number of playouts allocated for a move m at the current round
                    #    given:
                    #           the current budget
                    #           the playouts already allocated to a move in previous rounds
                    allocated_playouts = current_budget - t['playouts'][str(moves[m])]
                    
                    if at_root and len(moves) == 2 and m == 0:
                        allocated_playouts = budget - budget_used - (current_budget - t['playouts'][str(moves[1])])
                    
                    # Victor: Aqui força allocated_playouts não ultrapassar o budget
                    #  se allocated playouts for maior que o número de playouts faltantes, pega o número de playouts faltantes
                    #  então acho que o budget_used em t não deve ultrapassar o budget
                    allocated_playouts  = min(allocated_playouts, budget - budget_used)
                    new_board           = self.game.apply(moves[m], board)
                    move, new_budget_used, new_playouts, new_wins = self.shot(new_board, allocated_playouts, self.get_opponent_of(current_player))
                    playouts    += new_playouts
                    budget_used += new_budget_used
                    wins        += new_wins
                    
                    t['playouts'][str(moves[m])]  += new_playouts
                    t['victories'][str(moves[m])] += new_wins
                    t['budget_node']              += new_budget_used
                
                if budget_used >= budget:
                    break 


            moves.sort(key=lambda move: t['victories'][str(move)]/t['playouts'][str(move)])
            moves = moves[floor(len(moves)/2):]
            if budget_used >= budget:
                break 
        t['budget_node'] += budget_used

        #Victor: achei estranho, no final na realidade t.budget_used realiza 4096 playouts, não 2048.#
        return moves[0], budget_used, playouts, wins

    def select_action(self, game, context, max_seconds=0, max_iterations=0, max_depth=0):
        move, b_u, p, w = self.shot(context, 2048, current_player=self.player, at_root=True)
        #move, b_u, p, w = self.shot([[0, -1, 1],[1, 1, -1],[-1, -1, 1]], 2048, current_player=self.player, at_root=True)
        return move

    def get_name(self):
        return "SHOT Agent"
