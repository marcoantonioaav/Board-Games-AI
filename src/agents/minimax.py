from inspect import trace
from numpy import Inf
from agents.agent import Agent
import tracemalloc

class MinimaxAgent(Agent):
    def evaluate(self, context):
        if self.game.is_victory(context, self.player):
            return 1
        elif self.game.is_victory(context, self.get_opponent()):
            return -1
        else:
            return 0
    
    def minimax(self, context, depth, maximizingMoveer):
        if depth == 0 or self.game.is_terminal_state(context):
            return self.evaluate(context), None
        if maximizingMoveer:
            max_value = -Inf
            max_move = None
            for legal_move in self.game.moves(context, self.player):
                new_context = self.game.apply(legal_move, context)
                new_value, move = self.minimax(new_context, depth - 1, False)
                if new_value > max_value:
                    max_value = new_value
                    max_move = legal_move
            return max_value, max_move
        else:
            min_value = Inf
            min_move = None
            for legal_move in self.game.moves(context, self.get_opponent()):
                new_context = self.game.apply(legal_move, context)
                new_value, move = self.minimax(new_context, depth - 1, True)
                if new_value < min_value:
                    min_value = new_value
                    min_move = legal_move
            return min_value, min_move

    def select_action(self, game, context, max_second=0, max_iterations=0, max_depth=4):
        # starting the monitoring
        tracemalloc.start()
        
        value, move = self.minimax(context, max_depth, True)

        # displaying the memory
        tmp = tracemalloc.get_traced_memory()
        str1 = str(int(tmp[0]/1000))+"MiB"
        str2 = str(int(tmp[1]/1000))+"MiB"
        print(f'{str1:<12}{str2}')
        tracemalloc.stop()
        return move

    def get_name(self):
        return "Minimax Agent"