'''

    *** ARTIFICIAL GAME TREE ***


generates a game tree artificially :0

it should extend the Game class in order to be understandable for the agents.

feel free for you state-key representation.

every state should have a is_terminal flag, win probability and all applicable actions at current state.
 - is up to you how you going to reduce (state, applicable action) ==> new state.

There is two kinds of terminal states, the actual terminal states and the
ones that have further states in practice, but we wont expand it here.
so.. for the actual ones represent it useing pro-win value properly:
    1 for win
    0 for loss
for the fake terminal states, mark it as terminal but give prob-win a value as you wish.
'''
from agents.agent import Agent
from games.game import Game

import random


class AGTree(Game):
    
    IS_TERMINAL = 0
    PROB_WIN    = 1
    APPLICABLE_ACTIONS = 2
    def __init__(self):
        self.states  = {}
        self.instace()
        self.winning_number = 0

    def instace(self):
        # <state> = {is_terminal, prob-win, [applicable actions]}
        self.states['A'] = { 'is_terminal':0, 'prob-win': 0   , 'app_actions':('b', 'c')}
        self.states['B'] = { 'is_terminal':0, 'prob-win':0.354, 'app_actions':('d', 'e')}
        self.states['C'] = { 'is_terminal':0, 'prob-win':0.775, 'app_actions':('f', 'd')}
        self.states['D'] = { 'is_terminal':0, 'prob-win':0.75 , 'app_actions':('h', 'i')}
        self.states['E'] = { 'is_terminal':1, 'prob-win':0    , 'app_actions':()        }
        self.states['F'] = { 'is_terminal':0, 'prob-win':0.8  , 'app_actions':('g')     }
        self.states['G'] = { 'is_terminal':1, 'prob-win':0.8  , 'app_actions':()        }
        self.states['H'] = { 'is_terminal':0, 'prob-win':0.75 , 'app_actions':('i', 'j')}
        self.states['I'] = { 'is_terminal':1, 'prob-win':0.7  , 'app_actions':()        }
        self.states['J'] = { 'is_terminal':1, 'prob-win':0.8  , 'app_actions':()        }

    def get_initial_board(self):
        return 'A'

    def is_terminal(self, state_id):
        return self.states[state_id]['is_terminal']

    def apply(self, action, curr_state):
        self.winning_number = random.uniform(0.0, 1.0)
        curr_state = action.upper()
        return curr_state

    def moves(self, curr_state, player):
        return list(self.states[curr_state]['app_actions'])

    def is_victory(self, state, player):
        if self.states[state]['is_terminal'] == 0:
            return False

        
        if (self.winning_number < self.states[state]['prob-win'] and player == 1) or (self.winning_number >= self.states[state]['prob-win'] and player == -1):
            return True
        else:
            return False


    
        
                
        

        

