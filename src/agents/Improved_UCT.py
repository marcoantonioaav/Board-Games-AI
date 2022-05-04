import random
import math
import time
from copy import deepcopy
from tkinter.tix import Tree

from sqlalchemy import true

from agents.agent import Agent
from agents.UCT import UCT
from agents.TT_UCT import TT_UCT, TTNode
from agents.Recycle_UCT import Recycle_UCT

from memory_profiler import profile
import tracemalloc
import psutil

class Improved_UCT(TT_UCT):
    def __init__(self):
        self.TTable = {}
        self.root = None
        self.count_transpositions = 0
        self.old_root = None
    def get_name(self):
        return "Improved UCT"

    def select_action(self, 
                      game, 
                      context, 
                      max_seconds  =   -1,
                      max_episodes = 2000,
                      max_depth    =    0):
        # starting the monitoring
        #tracemalloc.start()
        start_time = time.time()
        self.count_transpositions = 0
        
        root = None
        # check if new root is in TTable
        if not self.old_root == None and (self.player, str(context)) in self.TTable: 
            root = self.TTable[(self.player, str(context))] #self.recycle(self.root, context) *WITH TTABLE IT DOESENT NEED TO TREE-SEARCH
            self.discard_garbage(root, self.old_root) 
            
            
        else:
            legal_moves = game.moves(context, self.player)
            root   = TTNode(None, None, context, legal_moves, self.player)
            self.TTable = {}
            #self.TTable[(self.player, str(context))] = self.root
        tracemalloc.start()
        
        episodes  = 0
        stop_time = math.inf if max_seconds <= 0.0 else time.time() + max_seconds
        
        while episodes < max_episodes and time.time() < stop_time:
            current_node = self.search(game, root)
            new_node     = self.expand(game, current_node)
            reward       = self.playout(game, new_node)
            self.backpropagate(new_node, reward)
            
            episodes+=1
        


        # displaying the memory
        tmp = tracemalloc.get_traced_memory()
        ag_str = self.get_name()
        str1 = str(int(tmp[0]/1000))+"MiB"
        str2 = str(int(tmp[1]/1000))+"MiB"
        str3 = str(psutil.virtual_memory()[2]) + "%"
        str4 = str(round((time.time() - start_time), 6)) + "s"
        str5 = str(root.n_value) + " | " + str(self.count_transpositions)
        print(f'{ag_str:<15}{str1:<12}{str2:<12}{str3:<8}{str4:<8}{str5:>12}')

        tracemalloc.stop()

        self.old_root = root#root.deep_copy()
        
        return self.max_balanced_child(root)

    def discard_garbage(self, new_root, old_root):
        
        # 1st map every reachable node starting at new_root
        reachable_nodes = set()
        reachable_nodes.add(new_root)
        search_lst = [new_root]
        while len(search_lst) > 0:
            current = search_lst.pop(0)
            reachable_nodes.add(current)
            search_lst += current.children
        
        self.TTable = {}
        new_root.move = None
        lst_nodes =  [new_root]
        while len(lst_nodes) > 0:
            node = lst_nodes.pop(0)
            self.TTable[(node.player, str(node.context))] = node
            lst_nodes += node.children

            for p in node.parent:
                if not p in reachable_nodes:
                    node.parent.remove(p)
            
        new_root.parent = [None]

        
        '''
        # 2nd delete nodes, detach invalid relations and remove keys from TTable
        garbage_nodes = [old_root]
        
        while len(garbage_nodes) > 0:
            #get next parent
            parent = garbage_nodes.pop()
            
            #len_ch = len(parent.children)
            #it = 0
            #iterate over parent's children
            #for it in range(len_ch):
            for ch in parent.children:
                #ch = parent.children[it]
                if parent in ch.parent:
                    ch.parent.remove(parent)
                
                #if not ch.move == None:
                    #ch.legal_moves += [next_parent.move]
                #next_parent.legal_moves += [ch.move]
                #next_parent.children.remove(ch)

                # if child is the new_root, do not append it at garbage nodes
                if ch in reachable_nodes:
                    #it+=1
                    continue
                else:
                    #add to be deleted the pair (parent, children[]) for further iterations
                    garbage_nodes = garbage_nodes + [ch] #[i for i in ch.children if i != new_root]
                
            #if (next_parent.player, str(next_parent.context)) in self.TTable:
            #    del self.TTable[(next_parent.player, str(next_parent.context))] #delete from TTable
            #del next_parent
            #print("DISCARDED: p"+ str(parent.player)+ ", " +str(parent.context) + "--->" +str(parent in reachable_nodes))
        '''

    def __str__(self):
        return "p" + str(self.player) + "|"+str(self.context)
        



