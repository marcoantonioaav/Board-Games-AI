  
import random
import math
import time
from copy import deepcopy

from agents.agent import Agent
from agents.UCT import UCT

from memory_profiler import profile
import tracemalloc
import psutil
'''
TT-UCT: UCT with transposition table
Uses transposition tables at Upper Confidence Trees:
Node are considered the same if it shares the state and same player's turn.
In order to do it, we have to change expansion phase, backpropagation and maybe UCB policy.
*expansion phase:
    if (player, state) in TTable it should first append the new parent discovered and its new child.
    then it must make a *pre-backpropagation*, updating every new parent of the transposed node with
    its previous nvalue and qvalue.
        - pay attention to avoid update a parent node that was already at the transposed node.
*backpropagation:
    it must update not only the nodes visisted at the searching-phase, but every parent node
    the expanded node can reach. (it must do a bottom-up update)
        - avoid double update nodes that appears in more than one path
*UCB:
    Check if creates to much bias and if UCB is sufficient to solve it with exploration vs exploitation

TODO: I think it should double update parents, if it dont, maybe it will interfier in policy
TODO 2: Maybe transposition affects UCB and for the parent choose, maybe the parent should use some episodes to balance the bias.
'''
    
class TT_UCT(UCT):  
    log_actions = {}
    
    def __init__(self):
        self.TTable = {}
        self.count_transpositions = 0

    def get_name(self):
        return "TT-UCT Agent"

    #@profile
    def select_action(self, 
                      game, 
                      context, 
                      max_seconds  =   -1,
                      max_episodes = 2000,
                      max_depth    =    0):

        # starting the monitoring
        tracemalloc.start()
        start_time = time.time()

        legal_moves = game.moves(context, self.player)
        root        = TTNode(None, None, context, legal_moves, self.player)

        episodes = 0
        self.count_transpositions = 0
        self.TTable = {}
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

        #print(self.count_transpositions)
        for ep in self.log_actions:
            print(("episode {:<4} [").format(str(ep)), end= " ")
            str_actions = ""
            for c in self.log_actions[ep]: 
                str_actions += (" {:<2} ({:<10}, {:<10}) ").format(c, str(self.log_actions[ep][c]["emp_avg"]), str(self.log_actions[ep][c]["err"]))
            print(str_actions + "]")

            
        # displaying the memory
        ag_str = self.get_name()
        tmp = tracemalloc.get_traced_memory()
        str1 = str(int(tmp[0]/1000))+"MiB"
        str2 = str(int(tmp[1]/1000))+"MiB"
        str3 = str(psutil.virtual_memory()[2]) + "%"
        str4 = str(round(int(time.time() - start_time), 6)) + "s"
        #print(f'{ag_str:<15}{str1:<12}{str2:<12}{str3:<8}{str4:<8}')
        tracemalloc.stop()

        return self.max_balanced_child(root)

    def expand(self, 
               game, 
               current_node):
        
        if current_node.legal_moves == []:
            return current_node

        next_move    = current_node.legal_moves.pop()
        next_context = game.apply(next_move, current_node.context)
        next_player  = current_node.player * -1
        str_next_context = str(next_context)

        #HIT Transposition Table:
        if (next_player, str_next_context) in self.TTable:
            target_node = self.TTable[(next_player, str_next_context)]
            self.pre_backpropagate(target_node, current_node)
            target_node.parent.append(current_node)
            current_node.children.append(target_node)
            self.count_transpositions+=1
            return target_node

        new_node = TTNode(current_node, next_move, next_context, game.moves(next_context, next_player), next_player)
        self.TTable[(next_player, str_next_context)] = new_node
        return new_node
    
    def pre_backpropagate(self, target_node, new_parent):
        
        # 1: search for every reachable node from target_node
        lst_old_parents = set()
        lst_path = [target_node]
        while len(lst_path) > 0:
            current = lst_path.pop(0)
            if current.parent == [None]:
                continue
            lst_old_parents.add(current)
            lst_path = lst_path + current.parent
        
        # 2: for every reachable node starting at new_parent (that not appears at lst_old_parents)
        #       increment its Nvalue and Qvalue with target_node values
        lst_path = [new_parent]
        while len(lst_path) > 0:
            current = lst_path.pop(0)
            #TODO: fix it
            if current == [None] or current == [] or current is None:
                continue
            
            #elif not current in lst_old_parents: # Not sure if it should invalid parents already updated in previous propagations
            else:
                current.n_value += target_node.n_value
                current.q_value += target_node.q_value
            lst_path = lst_path + current.parent


    def backpropagate(self, node, reward):
        lst_nodes = [node]
        lst_parents = set() # for double updating at backtrack
        while len(lst_nodes) > 0:
            current = lst_nodes.pop(0)
            
            #TODO: fix it
            if current in lst_parents or current == [None] or current == [] or current is None: 
                continue
            
            current.q_value += reward
            current.n_value += 1
            
            #lst_parents.add(current) # Not sure if it should check parents already marked
            
            lst_nodes = current.parent + lst_nodes
class TTNode:
    def __init__(self, parent, move, context, legal_moves, player):
        self.n_value  = 0
        self.q_value  = 0 
        self.player   = player
        self.children = []
        self.legal_moves = legal_moves
        random.shuffle(self.legal_moves)

        
        self.parent = [parent]
        self.move    = move
        self.context = context

        if parent != None:
            parent.children.append(self)
    
    
    def deep_copy(self):
        return deepcopy(self)
    
    def __del__(self):
        self.n_value  = None
        self.q_value  = None
        self.player   = None
        self.children = None
        self.legal_moves = None
        self.parent  = None
        self.move    = None
        self.context = None

