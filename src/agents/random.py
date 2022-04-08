import random
from agents.agent import Agent


class RandomAgent(Agent):
    def select_action(self, game, context, max_seconds=0, max_iterations=0, max_depth=0):
        return random.choice(self.game.moves(context, self.player))