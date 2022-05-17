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
    def __init__(self, game_type):
        self.states  = {}
        self.instace(game_type)
        self.winning_number = 0

    def instace(self, game_type = "T1"):
        # <state> = {is_terminal, prob-win, [applicable actions]}
        
        if game_type ==  "T1P":
        ######  PROB TREE 1 ###########
            self.states['A'] = { 'is_terminal':0, 'prob-win': 0   , 'app_actions':('b', 'c')}
            self.states['B'] = { 'is_terminal':0, 'prob-win':0.30, 'app_actions':('d', 'e')}
            self.states['C'] = { 'is_terminal':0, 'prob-win':0.70, 'app_actions':('f', 'd')}
            self.states['D'] = { 'is_terminal':0, 'prob-win':0.60 , 'app_actions':('h', 'i')}
            self.states['E'] = { 'is_terminal':1, 'prob-win':0    , 'app_actions':()        }
            self.states['F'] = { 'is_terminal':0, 'prob-win':0.8  , 'app_actions':('g')     }
            self.states['G'] = { 'is_terminal':1, 'prob-win':0.8  , 'app_actions':()        }
            self.states['H'] = { 'is_terminal':0, 'prob-win':0.60 , 'app_actions':('i', 'j', 'k')}
            self.states['I'] = { 'is_terminal':1, 'prob-win':0.7  , 'app_actions':()        }
            self.states['J'] = { 'is_terminal':1, 'prob-win':0.8  , 'app_actions':()        }
            self.states['K'] = { 'is_terminal':1, 'prob-win':0.3  , 'app_actions':()        }
        elif game_type == "T1":    
            ##### TREE 1 ##########
            self.states['A'] = { 'is_terminal':0, 'prob-win':1  , 'app_actions':('b', 'c')}
            self.states['B'] = { 'is_terminal':0, 'prob-win':0, 'app_actions':('d', 'e')}
            self.states['C'] = { 'is_terminal':0, 'prob-win':1, 'app_actions':('f', 'd')}
            self.states['D'] = { 'is_terminal':0, 'prob-win':1 , 'app_actions':('h')}
            self.states['E'] = { 'is_terminal':1, 'prob-win':0  , 'app_actions':()        }
            self.states['F'] = { 'is_terminal':0, 'prob-win':1  , 'app_actions':('g')     }
            self.states['G'] = { 'is_terminal':1, 'prob-win':1  , 'app_actions':()        }
            self.states['H'] = { 'is_terminal':0, 'prob-win':1 , 'app_actions':('i', 'j', 'k')}
            self.states['I'] = { 'is_terminal':1, 'prob-win':1  , 'app_actions':()        }
            self.states['J'] = { 'is_terminal':1, 'prob-win':1  , 'app_actions':()        }
            self.states['K'] = { 'is_terminal':1, 'prob-win':1  , 'app_actions' :()        }

        elif game_type ==  "T2P":
        ###### PROB TREE 2 ###########
            self.states['A'] = { 'is_terminal':0, 'prob-win': 0   , 'app_actions':('b', 'c', 'l')}
            self.states['B'] = { 'is_terminal':0, 'prob-win':0.30, 'app_actions':('d', 'e')}
            self.states['C'] = { 'is_terminal':0, 'prob-win':0.70, 'app_actions':('f', 'd')}
            self.states['D'] = { 'is_terminal':0, 'prob-win':0.60 , 'app_actions':('h', 'i')}
            self.states['E'] = { 'is_terminal':1, 'prob-win':0    , 'app_actions':()        }
            self.states['F'] = { 'is_terminal':0, 'prob-win':0.8  , 'app_actions':('g')     }
            self.states['G'] = { 'is_terminal':1, 'prob-win':0.8  , 'app_actions':()        }
            self.states['H'] = { 'is_terminal':0, 'prob-win':0.60 , 'app_actions':('i', 'j', 'k')}
            self.states['I'] = { 'is_terminal':1, 'prob-win':0.7  , 'app_actions':()        }
            self.states['J'] = { 'is_terminal':1, 'prob-win':0.8  , 'app_actions':()        }
            self.states['K'] = { 'is_terminal':1, 'prob-win':0.3  , 'app_actions':()        }
            self.states['L'] = { 'is_terminal':0, 'prob-win':0.75  , 'app_actions':('m', 'n')   }
            self.states['M'] = { 'is_terminal':1, 'prob-win':0.85  , 'app_actions':()        }
            self.states['N'] = { 'is_terminal':0, 'prob-win':0.65  , 'app_actions':('o','p','q')}
            self.states['O'] = { 'is_terminal':1, 'prob-win':0.70  , 'app_actions':()           }
            self.states['P'] = { 'is_terminal':1, 'prob-win':0.90  , 'app_actions':()           }
            self.states['Q'] = { 'is_terminal':0, 'prob-win':0.35  , 'app_actions':('r','s')    }
            self.states['R'] = { 'is_terminal':1, 'prob-win':0.50  , 'app_actions':()           }
            self.states['S'] = { 'is_terminal':1, 'prob-win':0.20  , 'app_actions':()           }
            
        elif game_type == "T2":
        ###### TREE 2 ##########
            self.states['A'] = { 'is_terminal':0, 'prob-win':1  , 'app_actions':('b', 'c', 'l')}
            self.states['B'] = { 'is_terminal':0, 'prob-win':0, 'app_actions':('d', 'e')}
            self.states['C'] = { 'is_terminal':0, 'prob-win':1, 'app_actions':('f', 'd')}
            self.states['D'] = { 'is_terminal':0, 'prob-win':1 , 'app_actions':('h')}
            self.states['E'] = { 'is_terminal':1, 'prob-win':0  , 'app_actions':()        }
            self.states['F'] = { 'is_terminal':0, 'prob-win':1  , 'app_actions':('g')     }
            self.states['G'] = { 'is_terminal':1, 'prob-win':1  , 'app_actions':()        }
            self.states['H'] = { 'is_terminal':0, 'prob-win':1 , 'app_actions':('i', 'j', 'k')}
            self.states['I'] = { 'is_terminal':1, 'prob-win':1  , 'app_actions':()        }
            self.states['J'] = { 'is_terminal':1, 'prob-win':1  , 'app_actions':()        }
            self.states['K'] = { 'is_terminal':1, 'prob-win':0  , 'app_actions'  :()        }
            self.states['L'] = { 'is_terminal':0, 'prob-win':1  , 'app_actions':('m', 'n')   }
            self.states['M'] = { 'is_terminal':1, 'prob-win':1  , 'app_actions':()        }
            self.states['N'] = { 'is_terminal':0, 'prob-win':1  , 'app_actions':('o','p','q')}
            self.states['O'] = { 'is_terminal':1, 'prob-win':1  , 'app_actions':()           }
            self.states['P'] = { 'is_terminal':0, 'prob-win':1  , 'app_actions':('c')           }
            self.states['Q'] = { 'is_terminal':0, 'prob-win':1  , 'app_actions':('r','s')    }
            self.states['R'] = { 'is_terminal':1, 'prob-win':1  , 'app_actions':()           }
            self.states['S'] = { 'is_terminal':1, 'prob-win':0 , 'app_actions':()         }
            
        

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
        # TODO: fix it
        if self.states[state]['is_terminal'] == 0:
            return False

        
        if (self.winning_number < self.states[state]['prob-win'] and player == 1) or (self.winning_number >= self.states[state]['prob-win'] and player == -1):
            return True
        else:
            return False


    
        
                
        

        

