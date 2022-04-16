import random
import math
import time
from copy import deepcopy

from agents.agent import Agent
from agents.agent import UCT
from agents.agent import Node

'''
 Recycle-UCT:  It reuses subtree from previous play and discard unused parts 

 * Im thinking in two options:
    1- search and grow the already used tree (as here)
    2- create a new tree and use the old one as a bias to decision making in some sense
'''
class Recycle_UCT(UCT):
    SUM = 0
    N = 0
    
    def __init__(self):
        self.root = None

    def get_name(self):
        return "Recycle UCT Agent"

    def select_action(self, 
                      game, 
                      context, 
                      max_seconds  =   -1,
                      max_episodes = 2000,
                      max_depth    =    0):
        r_nodes = 0

        if not self.root == None:
            self.root = self.recycle(self.root, context) #breath-first search to find the next root
            
            if not self.root == None:
                self.discard_garbage(self.root) #clear memory (can be done by a thread)
                self.root.parent = None
                self.SUM += self.root.n_value
                r_nodes = self.root.n_value
            # missed
            else:
                legal_moves = game.moves(context, self.player)
                self.root   = Node(None, None, context, legal_moves, 0, self.player)

        else:

            legal_moves = game.moves(context, self.player)
            self.root   = Node(None, None, context, legal_moves, 0, self.player)

        episodes  = 0
        stop_time = math.inf if max_seconds <= 0.0 else time.time() + max_seconds
        
        while episodes < max_episodes and time.time() < stop_time:
            current_node = self.search(game, self.root)
            new_node     = self.expand(game, current_node)
            reward       = self.playout(game, new_node)
            self.backpropagate(new_node, reward)
            
            episodes+=1
        self.N+=1

        #print("ply: " + str(self.N))
        #print("average reused nodes: " + str(round(float(self.SUM/self.N),3)))
        #print("current reused nodes: " + str(r_nodes)+ " ("+ str(int((r_nodes/max_episodes)*100)) + "%)")

        return self.max_balanced_child(self.root)
    
    # should implement breath-first search
    def recycle(self, node, target):
        if node.context == target:
            return node

        target_node = None
        highest_n = 0
        the_chosen_one = None
        for ch in node.children:
            target_node = self.recycle(ch, target)
            if target_node != None:
                if target_node.n_value > highest_n:
                    the_chosen_one = target_node
        
        return the_chosen_one

    def discard_garbage(self, new_root):
        # 1st go to old root
        old_root = new_root
        while old_root.parent != None:
            old_root = old_root.parent

        garbage_nodes = [ch for ch in old_root.children if ch != new_root]
        del old_root

        while not garbage_nodes == []:
            node = garbage_nodes.pop()
            t_gn = [ch for ch in node.children if ch != new_root]
            garbage_nodes = garbage_nodes + t_gn
            del node
