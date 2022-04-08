from numpy import Inf
from agents.agent import Agent


class MinimaxAgent(Agent):
    def get_heuristc_value(self, context):
        if self.game.is_victory(context, self.player):
            return 1
        elif self.game.is_victory(context, self.get_opponent()):
            return -1
        else:
            return 0
    
    def minimax(self, context, depth, maximizingMoveer):
        if depth == 0 or self.game.is_terminal_state(context):
            return self.get_heuristc_value(context), None
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
        value, move = self.minimax(context, max_depth, True)
        return move

    def get_name(self):
        return "Minimax Agent"