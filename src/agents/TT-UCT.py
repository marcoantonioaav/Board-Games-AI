import random
import math
import time
from copy import deepcopy

from agents.agent import Agent
from agents.agent import UCT
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

'''
    
class TT_UCT(UCT):  
    def __init__(self):
        self.TTable = {}

    def select_action(self, 
                      game, 
                      context, 
                      max_seconds  =   -1,
                      max_episodes = 2000,
                      max_depth    =    0):

        legal_moves = game.moves(context, self.player)
        root        = TTNode(None, None, context, legal_moves, self.player)

        episodes = 0
        stop_time = math.inf if max_seconds <= 0.0 else time.time() + max_seconds
        
        while episodes < max_episodes and time.time() < stop_time:
            current_node = self.search(game, root)
            new_node     = self.expand(game, current_node)
            reward       = self.playout(game, new_node)
            self.backpropagate(new_node, reward)
            
            episodes+=1

        return self.robust_child(root)

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
            lst_path = lst_path + current.parents
        
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
            lst_path = lst_path + current.parents

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
    
