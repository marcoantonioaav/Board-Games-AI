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
    Here im not sure what is the best way to do it... if a parent node has to compare who is the next step and
    one node appears in more than one path, maybe is infair compare its parameters with his sibblin.

                        ** IMPORTANT **
using transposition table bring to changes the structure of the game tree
into a directed graph, BUT depending on the game it appears to have be cyclic
SO it must use some strategy to avoid it, like not allow expanding nodes that
would cause a cicle.
'''
    
class TT_UCT(UCT):  
    def __init__(self):
        self.TTable = {}
        self.count_transpositions = 0
        self.leafs = 0

    def get_name(self):
        return "TT-UCT Agent"

    #@profile
    def select_action(self, 
                      game, 
                      context, 
                      max_seconds  =   -1,
                      max_episodes = 5000,
                      max_depth    =    0):

        # starting the monitoring
        tracemalloc.start()
        start_time = time.time()

        legal_moves = game.moves(context, self.player)
        root        = TTNode(None, None, context, legal_moves, self.player)

        episodes = 0
        self.count_transpositions = 0
        self.leafs = 0
        self.TTable = {}
        stop_time = math.inf if max_seconds <= 0.0 else time.time() + max_seconds
        
        while episodes < max_episodes and time.time() < stop_time:
            current_node = self.search(game, root)
            new_node     = self.expand(game, current_node)
            reward       = self.playout(game, new_node)
            self.backpropagate(new_node, reward)
            
            episodes+=1

        #print(self.count_transpositions)

        # displaying the memory
        ag_str = self.get_name()
        tmp = tracemalloc.get_traced_memory()
        str1 = str(int(tmp[0]/1000))+"MiB"
        str2 = str(int(tmp[1]/1000))+"MiB"
        str3 = str(psutil.virtual_memory()[2]) + "%"
        str4 = str(round(int(time.time() - start_time), 6)) + "s"
        print(f'{ag_str:<15}{str1:<12}{str2:<12}{str3:<8}{str4:<8}')
        tracemalloc.stop()

        return self.robust_child(root)

    def expand(self, 
               game, 
               current_node):
        
        if current_node.legal_moves == []:
            #self.leafs+=1
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
    
    # update every parent node that appeared at expansion
    def pre_backpropagate(self, target_node, new_parent):
        
        # 1: search for every reachable node from target_node
        lst_old_parents = set()
        lst_path = [target_node]
        while len(lst_path) > 0:
            current = lst_path.pop(0)
            lst_old_parents.add(current)
            if current.parent == [None]:
                continue
            lst_path = lst_path + current.parent
        
        # 2: for every reachable node starting at new_parent (that not appears at lst_old_parents)
        #       increment its Nvalue and Qvalue with target_node values
        lst_path = [new_parent]
        while len(lst_path) > 0:
            current = lst_path.pop(0)
            if current.parent == [None]:
                continue
            elif not current in lst_old_parents:
                current.n_value += target_node.n_value
                current.q_value += target_node.q_value
            lst_path = lst_path + current.parent


    def backpropagate(self, node, reward):
        lst_nodes = [node]
        lst_parents = set() # for double updating at backtrack
        while len(lst_nodes) > 0:
            current = lst_nodes.pop(0)
            if current in lst_parents or current.parent == [None]:
                continue
            
            current.q_value += reward
            current.n_value += 1
            lst_parents.add(current)
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

    def __str__(self):
        return "p" + str(self.player) + "|"+str(self.context)
    
