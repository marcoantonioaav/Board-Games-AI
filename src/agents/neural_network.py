from agents.agent import Agent
from agents.minimax import MinimaxAgent
import tensorflow as tf
import numpy as np
import random
from copy import deepcopy

class NeuralNetworkAgent(Agent):
    def __init__(self) -> None:
        super().__init__()
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(9, activation='relu', input_dim=9),
            tf.keras.layers.Dense(9, activation='relu'),
            tf.keras.layers.Dense(9, activation='relu'),
            tf.keras.layers.Dense(3, activation='sigmoid')
        ])
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    def train(self, training_size=300, epochs=500):
        train_agent = MinimaxAgent()
        train_agent.set_game(self.game)
        train_agent.set_player(self.player)
        train_x = []
        train_y = []
        for i in range(training_size):
            value = None
            context = None
            while True:
                context = self.get_random_context()
                value, move = train_agent.minimax(context, 9, False)
                value = self.value_to_y(value)
                #value = self.normalize(value)
                if train_y.count(value) < training_size/3:
                    break
            print(f"x:{self.board_to_tensor(context)} y:{value}")
            train_x.append(self.board_to_tensor(context))
            train_y.append(value)
        self.model.fit(train_x, train_y, epochs=epochs)

    def value_to_y(self, value):
        if value == 1:
            return (1, 0, 0)
        elif value == 0:
            return (0, 1, 0)
        else:
            return (0, 0, 1)

    def get_random_context(self):
        max_depth = random.randint(1, 9)
        context = self.game.get_initial_board()
        depth = 0
        while ((not self.game.is_terminal_state(context)) and depth < max_depth):
            move = random.choice(self.game.moves(context, Agent.PLAYER_1))
            context = self.game.apply(move, context)
            depth += 2
            if depth >= max_depth:
                return context
            if not self.game.is_terminal_state(context):
                move = random.choice(self.game.moves(context, Agent.PLAYER_2))
                new_context = self.game.apply(move, context)
                if self.game.is_terminal_state(new_context):
                    return context
                else:
                    context = new_context
        return context
    
    def normalize(self, value):
        return (value - (-1))/(1 - (-1))

    def evaluate(self, context):
        if self.game.is_victory(context, self.player):
            #return self.normalize(1)
            return 1
        elif self.game.is_victory(context, self.get_opponent()):
            #return self.normalize(-1)
            return -1
        else:
            #prediction = self.model.predict([self.board_to_tensor(context)], verbose=0)[0][0]
            #print(f"{self.board_to_tensor(context)} -> {prediction}")
            #return prediction
            prediction = self.model.predict([self.board_to_tensor(context)], verbose=0)[0]
            if prediction[0] > prediction[1] and prediction[0] > prediction[2]:
                #print(f"{self.board_to_tensor(context)} -> {prediction[0]}")
                return prediction[0]
            elif prediction[1] > prediction[0] and prediction[1] > prediction[2]:
                error = (1-prediction[1])/2
                value = prediction[0]*error + prediction[2]*-1*error
                #print(f"{self.board_to_tensor(context)} -> {value}")
                return value
            else:
                #print(f"{self.board_to_tensor(context)} -> {prediction[2]*-1}")
                return prediction[2]*-1
            

    def board_to_tensor(self, board):
        tensor = []
        for line in board:
            tensor += line
        return tuple(tensor)

    def select_action(self, game, context, max_second=0, max_iterations=0, max_depth=4):
        max_value = -np.Inf
        max_move = None
        for move in self.game.moves(context, self.player):
            new_context = self.game.apply(move, context)
            new_value = self.evaluate(new_context)
            if new_value > max_value:
                max_value = new_value
                max_move = move
        return max_move

    def get_name(self):
        return "Neural Network Agent"