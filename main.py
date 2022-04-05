import ui
from tictactoe import Game
import agents
import MCTS
def run_game(game, agent_1:agents.Agent, agent_2:agents.Agent):
    board = game.get_initial_board()
    while not game.is_terminal_state(board):
        board = game.apply(agent_1.select_action(game,board), board)
        if not game.is_terminal_state(board):
            board = game.apply(agent_2.select_action(game,board), board)
    return game.get_winner(board)

def run_game_on_screen(game, agent_1:agents.Agent, agent_2:agents.Agent):
    board = game.get_initial_board()
    ui.print_frame(board)
    while not game.is_terminal_state(board):
        board = game.apply(agent_1.select_action(game,board), board)
        ui.print_frame(board)
        if not game.is_terminal_state(board):
            board = game.apply(agent_2.select_action(game,board), board)
            ui.print_frame(board)
    return game.get_winner(board)


def simulate_games(game, agent_1:agents.Agent, agent_2:agents.Agent, simulations):
    results = {"Draws":0, "Agent 1 victories":0, "Agent 2 victories":0}
    for i in range(simulations):
        results[list(results)[run_game(game, agent_1, agent_2)]] += 1
    
    return results

if __name__ == "__main__":
    #run_game_on_screen(agents.MinimaxAgent(1), agents.SequentialHalvingAgent(2))
    #run_game_on_screen(agents.RandomAgent(1), agents.MinimaxAgent(2))
    print(simulate_games(Game(),  MCTS.UCT(1), MCTS.Reclycle_UCT(-1), 100))
    #print(simulate_games(agents.RandomAgent(1), agents.RandomAgent(2), 100))
