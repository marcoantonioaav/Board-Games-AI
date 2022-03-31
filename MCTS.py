import random
import math
import time
from copy import deepcopy

'''
 Simple MCTS-UCT implementation.

 Trying to use Ludii's nomenclature for future integration.
'''

class UCT:
    
    def __init__(self, player_id):
        self.player_id = player_id


    def select_action(self, 
                    game, 
                    context, 
                    max_seconds,
                    max_episodes,
                    max_depth):

        legal_moves = game.moves(context)
        root = Node(None, None, context, legal_moves, 0)

        episodes = 0
        stop_time = math.inf if max_seconds <= 0.0 else time.time() + max_seconds
        while episodes < max_episodes and time.time() < stop_time:
            current_node = self.search(game, root)
            new_node = self.expand(game, current_node)
            reward = self.playout(game, new_node)
            self.backpropagate(game, new_node, reward)
            episodes+=1

        return self.robust_child(root)
    

    def search(self, game, node):

        if len(node.legal_moves) > 0:
            return node
    
        else:
            next_node = self.UCB1(game, node)
            self.search(game, next_node)
    
    def expand(self, game, current_node):
        next_move = current_node.legal_moves.pop()
        next_context = game.apply(next_move, current_node.context)
        return Node(current_node, next_move, next_context, game.moves(context), current_node.ply+1)

    def playout(self,game, node):
        
        current_state = node.context
        ply = node.ply
        ply_limit = 50
        player = node.player

        while not game.is_terminal(current_state) and ply <= ply_limit:
            ply+=1
            player *= -1
            legal_moves = random.shuffle(game.moves(current_state, player))
            if len(legal_moves) == 0:
                break
            game.apply(legal_moves[0], current_state)
            
        
        return self.reward_value(game, current_state, player)

    def backpropagate(self,node, reward):
        current = node
        while current.parent != None:
            current.q_value += reward
            current.n_value += 1
            current = current.parent

    def UCB1(self, game, node):
        best_child = None
        max_value = -math.inf
        lucky_number = 0
        parent_log = 2.0 * math.log(max(1, node.n_value))
        
        for ch in node.children:
            exploitation = ch.q_value/ch.n_value
            exploration = math.sqrt(parent_log/ch.n_value)
            
            sum_ee = exploration + exploitation
            
            if sum_ee > max_value:
                max_value = sum_ee
                best_child = ch
            
            elif sum_ee == max_value:
                if random.randint(0, lucky_number + 1) == 0:
                    best_child = ch
                lucky_number+=1
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
        
        for ch in random.shuffle(root.children):
            
            if ch.n_value > max_n_value:
                max_n_value = ch.n_value
                max_q_value = ch.q_value
                max_move = ch.move

            elif ch.n_value == max_n_value:
                if ch.q_value > max_q_value:
                    max_n_value = ch.n_value
                    max_q_value = ch.q_value
                    max_move = ch.move
        return max_move

class Node:
    def __init__(self, parent, move, context, legal_moves, ply):
        self.n_value = 0
        self.q_value = 0 
        self.ply = ply
        self.children = []
        self.legal_moves = legal_moves
        random.shuffle(self.legal_moves)

        self.parent = parent
        self.move = move
        self.context = context
    
        if parent is not None:
            parent.children.append(self)
    
    def deep_copy(self):
        return deepcopy(self)

