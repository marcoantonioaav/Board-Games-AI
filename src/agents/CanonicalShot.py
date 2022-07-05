import math
import copy
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
    
    # overload '>' operator
    def __gt__(a, b):
        return a if a.wins/a.playouts > b.wins/b.playouts else b
        

class CanonicalShot(SequentialHalvingAgent):
    def select_action(self, game, context, max_iterations=0, max_episodes=0, max_depth=0):
        root = SHOTNode(context, None, game.moves(context, self.player), self.get_opponent_of(self.player))
        self.game = game
        budget = 1000
        budget_used = self.expand(game, root, 1000)
        if root.playouts >= budget:
            return root.children[0]

        virtual_ch_len = len(root.children)
        layer_budget = 0
        
        while(virtual_ch_len > 1):
            layer_budget += self.layer_budget(root.playouts, budget, len(root.children))
            root.children = self.sort(root.children, virtual_ch_len, root.turn)
            
            for i in range(virtual_ch_len):    
                ch = root.children[i]
                child_budget = (layer_budget/virtual_ch_len) - ch.playouts

                # Aqui faz aquele negócio estranho para quando tem só |S| == 2
                # aqui é para alocal o resto do budget para cada
                if virtual_ch_len <= 2:
                    child_budget = budget - root.playouts - child_budget

                self.search(game, ch, child_budget)
                root.playouts += ch.playouts
                root.wins += ch.wins
            virtual_ch_len = math.floor(virtual_ch_len/2)
        
        root.children = self.sort(root.children, 2, root.turn)
        return root.children[0]

    def search(self, game, node, budget):
        if self.game.is_terminal_state(node.state) or budget == 1:
            node.wins += self.make_playout(node.state, self.player)
            node.playouts += 1
            return
        
        if len(node.unvisited_actions) > 0:
            self.expand(game, node, budget)
            if node.playouts >= budget:
                return

        
        virtual_ch_len = len(node.children)
        layer_budget = 0
        while virtual_ch_len > 1:
            layer_budget += self.layer_budget(node.playouts, budget, len(node.children))
            node.children = self.sort(node.children, virtual_ch_len, node.turn)            
            
            for i in range(virtual_ch_len):
                ch = node.children[i]
                child_budget = (layer_budget/virtual_ch_len) - ch.playouts
                self.search(game, ch, child_budget)
                node.playouts += ch.playouts
                node.wins     += ch.wins
            
            virtual_ch_len=math.floor(virtual_ch_len/2)
            
    def expand(self, game, node, budget):
        budget_used = 0
        for it_actions in range(len(node.unvisited_actions)):
            budget_used+= 1
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
                return budget_used
        return budget_used

    def layer_budget(self, trials, budget, len_children):
        
        total_budget = trials + budget           
        total_layers = math.ceil(math.log(len_children, 2))
        return math.floor(max(1, total_budget/total_layers))


    def sort(self, array, interval, player):
        ch_sort_cpy = array[:interval]
        if self.player == player:
            ch_sort_cpy.sort()
        else:
            ch_sort_cpy.sort(reverse = True)
        
        array = ch_sort_cpy + array[interval:]
        return array

    def get_name(self):
        return "SHOT Agent"





