from audioop import reverse
import math
import copy
from agents.UCT import Node
from agents.agent import Agent
from agents.sequential_halving import SequentialHalvingAgent


class SHOTNode():
    def __init__(self, state, action, unvisited_actions, turn):
        self.unvisited_actions = unvisited_actions
        self.state  = state
        self.action = action
        self.turn   = turn
        self.wins   = 0
        self.playouts = 0
        self.children = [] # childre apply(available_action, state)
'''
    Why improve 'Canonical' version of SHOT ? 
        1) The original version of the algorithm is too complex and the pseudo-code is not clear. 
        2) It uses transposition table as data structure (not intuitive) and pass parameters by reference. 
        3) The searching method has three terminal cases. Two of them does basically the same thing. 
        Conceptually has a little difference: It considers not making rollouts when the node is terminal. We believe
        that it can be considered as a rollout and the work that is done there only returns the Utility value.
        4) It is difficult to understand the different steps of the algorithm: everything is done in one function.
        5) Inside the recursion calls for each halvening loop, it has an 'if' condition that holds only at the
        root node when there is two moves left.
        6) It returns the best move for each time it closes a recursion call on the stack but only use it at the root
        in the last halve.
        7) The work done in SHOT algorithm have comparisions with UCT only for one game and we dont know how it works for
        general game playing.
                            
    * Our objective is to make a version that we believe is simpler and better to understand. We believe that SHOT
      could be used as a General Game Play algorithm but the way it was presented first time is too complex to be
      the canonical form of the algorithm.

'''

class NestedSH(SequentialHalvingAgent):
    def select_action(self, game, context, max_iterations=0, max_episodes=5000, max_depth=0):
        root = SHOTNode(context, None, game.moves(context, self.player), self.player)
        self.game = game
        budget = max_episodes
        
        budget_used = self.expand(game, root, budget)
        self.sort(root.children, len(root.children), root.turn)

        if root.playouts >= budget:
            return self.secure_child(root)

        virtual_ch_len = len(root.children)
        layer_budget = 0
        
        while(virtual_ch_len > 1):
            layer_budget += self.layer_budget(root.playouts, budget, len(root.children))
            
            for i in range(virtual_ch_len):    
                ch = root.children[i]
                child_budget = max(1, math.floor(layer_budget/virtual_ch_len)) - ch.playouts

                if virtual_ch_len <= 2:
                    child_budget = budget - root.playouts - child_budget
                
                prev_playouts = ch.playouts
                prev_wins     = ch.wins
                self.search(game, ch, child_budget)
                root.playouts += ch.playouts - prev_playouts
                root.wins += ch.wins - prev_wins
            virtual_ch_len = math.floor(virtual_ch_len/2)
            root.children = self.sort(root.children, virtual_ch_len, root.turn)
            
        root.children = self.sort(root.children, 2, root.turn)
        return self.secure_child(root)

    def search(self, game, node, budget): 
        if self.game.is_terminal_state(node.state) or budget == 1:
            node.wins += self.make_playout(node.state, self.player)
            node.playouts += 1
            return
        
        if len(node.children) == 1:
            prev_playouts = node.children[0].playouts
            prev_wins     = node.children[0].wins
            self.search(game, node.children[0], budget-1)
            node.playouts += node.children[0].playouts - prev_playouts
            node.wins += node.children[0].wins - prev_wins
            return

        if len(node.unvisited_actions) > 0:
            self.expand(game, node, budget)
            node.children = self.sort(node.children, len(node.children), node.turn)            
            
            if node.playouts >= budget:
                return

        virtual_ch_len = len(node.children)
        layer_budget = 0
        while virtual_ch_len > 1:
            layer_budget += self.layer_budget(node.playouts, budget, len(node.children))
            
            for i in range(virtual_ch_len):
                ch = node.children[i]
                child_budget = max(1, math.floor(layer_budget/virtual_ch_len)) - ch.playouts
                prev_playouts = ch.playouts
                prev_wins     = ch.wins
                self.search(game, ch, child_budget)
                node.playouts += (ch.playouts - prev_playouts)
                node.wins     += (ch.wins - prev_wins)
            
            virtual_ch_len=math.floor(virtual_ch_len/2)
            node.children = self.sort(node.children, virtual_ch_len, node.turn)            
            
    def expand(self, game, node, budget):
        for it_actions in range(len(node.unvisited_actions)):
            next_action = node.unvisited_actions.pop(0)
            next_state  = game.apply(next_action, copy.deepcopy(node.state))
            next_turn = self.get_opponent_of(node.turn)
            
            next_node   = SHOTNode(next_state, next_action, game.moves(next_state, next_turn), next_turn)
            next_node.wins = self.make_playout(next_node.state, next_turn)
            next_node.playouts += 1

            node.children.append(next_node)
            node.playouts += next_node.playouts 
            node.wins     += next_node.wins
            
            if node.playouts >= budget:
                return
            
    def layer_budget(self, trials, budget, len_children):
        total_budget = trials + budget           
        total_layers = math.ceil(math.log(len_children, 2))
        return total_budget/total_layers

    def sort(self, array, interval, player):
        ch_sort_cpy = array[:interval]
        ch_sort_cpy.sort(key=lambda ch: ch.wins/ch.playouts, reverse = self.player == player)        
        array = ch_sort_cpy + array[interval:]
        return array

    def secure_child(self, node):
        return node.children[0].action

    def get_name(self):
        return "SHOT Agent"
