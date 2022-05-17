import random
import math
import time
from copy import deepcopy

from agents.agent import Agent

# profiling stuff
import tracemalloc
import psutil
import time
'''
 Simple MCTS-UCT implementation.

 Trying to use Ludii's nomenclature for future integration.
'''

class UCT(Agent):
    log_actions = {}
    def get_name(self):
        return "UCT Agent"

    def select_action(self, 
                      game, 
                      context, 
                      max_seconds  =   -1,
                      max_episodes =   10,
                      max_depth    =    0):
        
        # starting the monitoring
        tracemalloc.start()
        start_time = time.time()


        legal_moves = game.moves(context, self.player)
        root        = Node(None, None, context, legal_moves, 0, self.player)

        episodes = 0
        stop_time = math.inf if max_seconds <= 0.0 else time.time() + max_seconds
        
        while episodes < max_episodes and time.time() < stop_time:
            current_node = self.search(game, root)
            new_node     = self.expand(game, current_node)
            reward       = self.playout(game, new_node)
            self.backpropagate(new_node, reward)


            
            arr_children = {}
            for ch in root.children:
                empirical_avg = round(1.0 * ch.q_value/ch.n_value, 6)
                epsilon = empirical_avg
                if episodes > 1 and ch.context in self.log_actions[episodes-1]:
                    epsilon = round(abs(epsilon -  self.log_actions[episodes-1][ch.context]["emp_avg"]),6)
                
                arr_children[ch.context] =  {"emp_avg":empirical_avg, "err":epsilon}
            self.log_actions[episodes] = arr_children
            
            episodes+=1
        

        for ep in self.log_actions:
            print(("episode {:<4} [").format(str(ep)), end= " ")
            str_actions = ""
            for c in self.log_actions[ep]: 
                str_actions += (" {:<2} ({:<10}, {:<10}) ").format(c, str(self.log_actions[ep][c]["emp_avg"]), str(self.log_actions[ep][c]["err"]))
            print(str_actions + "]")

        # displaying the memory
        tmp = tracemalloc.get_traced_memory()
        ag_str = self.get_name()
        str1 = str(int(tmp[0]/1000))+"MiB"
        str2 = str(int(tmp[1]/1000))+"MiB"
        str3 = str(psutil.virtual_memory()[2]) + "%"
        str4 = str(round((time.time() - start_time), 6)) + "s"

        #print(f'{ag_str:<15}{str1:<12}{str2:<12}{str3:<8}{str4:<8}')
        tracemalloc.stop()

        return self.max_balanced_child(root)
    

    def search(self, game, node):
        
        # can be an unexpanded node or a leaf node
        if len(node.legal_moves) > 0 or (len(node.legal_moves) == 0 and len(node.children) == 0):
            return node
    
        else:
            #next_node = self.UCB1(node)
            next_node = self.search(game, self.UCB1(node))
            
            return next_node
    
    def expand(self, 
               game, 
               current_node):
        
        # leaf node
        if current_node.legal_moves == []:
            return current_node

        next_move    = current_node.legal_moves.pop()
        next_context = game.apply(next_move, current_node.context)
        next_player  = current_node.player * -1
        return Node(current_node, next_move, next_context, game.moves(next_context, next_player), current_node.ply+1, next_player)

    def playout(self, 
                game, 
                node):
        
        current_state = node.context
        ply       = 0#node.ply
        ply_limit = 50
        player    = node.player

        while not game.is_terminal_state(current_state) and ply <= ply_limit:
            
            ply     +=  1
            player  *= -1
            legal_moves = game.moves(current_state, player)
            random.shuffle(legal_moves)
            if len(legal_moves) == 0:
                break
            current_state = game.apply(legal_moves[0], current_state)
            
        
        return self.reward_value(game, current_state)

    def backpropagate(self, node, reward):
        current = node
        while current != None:
            current.q_value += reward
            current.n_value += 1
            current = current.parent

    def UCB1(self, node):
        best_child   = node
        max_value    = -math.inf
        lucky_number = 0
        parent_log   = 2.0 * math.log(max(1, node.n_value))
        
        for ch in node.children:

            exploitation = ch.q_value/ch.n_value
            exploration  = math.sqrt(parent_log/ch.n_value)
            if(node.player != self.player):
                exploitation *=- 1
            sum_ee = (exploration) + exploitation
            
            if sum_ee > max_value:
                max_value  = sum_ee
                best_child = ch
            
            elif sum_ee == max_value:
                if random.randint(0, lucky_number + 1) == 0:
                    best_child = ch
                lucky_number += 1

        return best_child

    
    def reward_value(self, game, state):
        if game.is_victory(state, self.player):
            return 1
        return 0

        #if game.is_victory(state, player) and player == self.player:
        #    return 1
        #elif game.is_victory(state, player*-1):
        #    return 0
        #else:
        #    return 0

    def robust_child(self, root):
        max_n_value = -math.inf
        max_q_value = -math.inf
        max_move = None
        
        random.shuffle(root.children)
        for ch in root.children:
            
            if ch.n_value > max_n_value:
                max_n_value = ch.n_value
                max_q_value = ch.q_value
                max_move    = ch.move

            elif ch.n_value == max_n_value:
                if ch.q_value > max_q_value:
                    max_n_value = ch.n_value
                    max_q_value = ch.q_value
                    max_move    = ch.move
        return max_move
    
    def max_balanced_child(self, root):
        max_balanced = -math.inf
        max_move = None
        
        parent_log   = 2.0 * math.log(max(1, 2000))
        
        random.shuffle(root.children)
        for ch in root.children:
            exploitation = ch.q_value/ch.n_value
            exploration  = math.sqrt(parent_log/ch.n_value)
            sum_ee = exploitation - exploration
            if sum_ee > max_balanced:
                max_balanced = sum_ee
                max_move = ch.move
        return max_move
    

class Node:
    def __init__(self, parent, move, context, legal_moves, ply, player):
        self.n_value  = 0
        self.q_value  = 0 
        self.ply      = ply
        self.player   = player
        self.children = []
        self.legal_moves = []
        self.legal_moves = legal_moves
        random.shuffle(self.legal_moves)

        self.parent  = parent
        self.move    = move
        self.context = context
    
        if parent is not None:
            parent.children.append(self)
    
    def deep_copy(self):
        return deepcopy(self)
    
    def __del__(self):
        self.n_value  = None
        self.q_value  = None
        self.ply      = None
        self.player   = None
        self.children = None
        self.legal_moves = None
        self.parent  = None
        self.move    = None
        self.context = None
    
