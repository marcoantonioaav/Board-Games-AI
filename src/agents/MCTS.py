import random
import math
import time
from copy import deepcopy
from agents import Agent
'''
 Simple MCTS-UCT implementation.

 Trying to use Ludii's nomenclature for future integration.
'''

class UCT(Agent):
    
    def __init__(self, player_id):
        self.player_id = player_id

    def get_name(self):
        return "UCT Agent"

    def select_action(self, 
                      game, 
                      context, 
                      max_seconds  =   -1,
                      max_episodes = 1000,
                      max_depth    =    0):

        legal_moves = game.moves(context, self.player_id)
        root        = Node(None, None, context, legal_moves, 0, self.player_id)

        episodes = 0
        stop_time = math.inf if max_seconds <= 0.0 else time.time() + max_seconds
        
        while episodes < max_episodes and time.time() < stop_time:
            current_node = self.search(game, root)
            new_node     = self.expand(game, current_node)
            reward       = self.playout(game, new_node)
            self.backpropagate(new_node, reward)
            
            episodes+=1

        return self.robust_child(root)
    

    def search(self, game, node):
        
        # can be an unexpanded node or a leaf node
        if len(node.legal_moves) > 0 or (len(node.legal_moves) == 0 and len(node.children) == 0):
            return node
    
        else:
            next_node = self.UCB1(node)
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
        ply       = node.ply
        ply_limit = 50
        player    = node.player

        while not game.is_terminal_state(current_state) and ply <= ply_limit:
            
            ply     +=  1
            player  *= -1
            legal_moves = game.moves(current_state, player)
            random.shuffle(legal_moves)
            if len(legal_moves) == 0:
                break
            game.apply(legal_moves[0], current_state)
            
        
        return self.reward_value(game, current_state, player)

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
            if(node.player != self.player_id):
                exploitation *=- 1
            sum_ee = (0.5 * exploration) + exploitation
            
            if sum_ee > max_value:
                max_value  = sum_ee
                best_child = ch
            
            elif sum_ee == max_value:
                if random.randint(0, lucky_number + 1) == 0:
                    best_child = ch
                lucky_number += 1

        return best_child

    
    def reward_value(self, game, state, player):
        if game.is_victory(state, player) and player == self.player_id:
            return 1
        elif game.is_victory(state, player) and player != self.player_id:
            return -1
        else:
            return 0

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



'''
 Recycle-UCT:  It reuses subtree from previous play and discard unused parts 

 * Im thinking in two options:
    1- search and grow the already used tree (as here)
    2- create a new tree and use the old one as a bias to decision making in some sense
'''
class Recycle_UCT(UCT):
    SUM = 0
    N = 0
    
    def __init__(self, player_id):
        self.player_id = player_id
        self.root = None

    def get_name(self):
        return "Recycle UCT Agent"

    def select_action(self, 
                      game, 
                      context, 
                      max_seconds  =   -1,
                      max_episodes = 3000,
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
                legal_moves = game.moves(context, self.player_id)
                self.root   = Node(None, None, context, legal_moves, 0, self.player_id)

        else:

            legal_moves = game.moves(context, self.player_id)
            self.root   = Node(None, None, context, legal_moves, 0, self.player_id)

        episodes  = 0
        stop_time = math.inf if max_seconds <= 0.0 else time.time() + max_seconds
        
        while episodes < max_episodes and time.time() < stop_time:
            current_node = self.search(game, self.root)
            new_node     = self.expand(game, current_node)
            reward       = self.playout(game, new_node)
            self.backpropagate(new_node, reward)
            
            episodes+=1
        self.N+=1

        print("ply: " + str(self.N))
        print("average reused nodes: " + str(round(float(self.SUM/self.N),3)))
        print("current reused nodes: " + str(r_nodes)+ " ("+ str(int((r_nodes/max_episodes)*100)) + "%)")

        return self.robust_child(self.root)
    
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
