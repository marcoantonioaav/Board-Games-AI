from agents.minimax import MinimaxAgent
from agents.agent import Agent
from agents.sequential_halving import SequentialHalvingAgent, ShotAgent
from agents.random import RandomAgent
import ui.ui as ui
from games.tictactoe import TicTacToe

def run_game(game, agent_1:Agent, agent_2:Agent):
    agent_1.set_game(game), agent_2.set_game(game)
    agent_1.set_player(Agent.PLAYER_1), agent_2.set_player(Agent.PLAYER_2)

    board = game.get_initial_board()
    while not game.is_terminal_state(board):
        board = game.apply(agent_1.select_action(board), board)
        if not game.is_terminal_state(board):
            board = game.apply(agent_2.select_action(board), board)
    return game.get_winner(board)

def run_game_on_screen(game, agent_1:Agent, agent_2:Agent):
    agent_1.set_game(game), agent_2.set_game(game)
    agent_1.set_player(Agent.PLAYER_1), agent_2.set_player(Agent.PLAYER_2)

    board = game.get_initial_board()
    ui.print_frame(board)
    while not game.is_terminal_state(board):
        board = game.apply(agent_1.select_action(board), board)
        ui.print_frame(board)
        if not game.is_terminal_state(board):
            board = game.apply(agent_2.select_action(board), board)
            ui.print_frame(board)
    ui.print_result(board, game)
    return game.get_winner(board)

def result_to_list_index(result):
    if result == Agent.PLAYER_1:
        return 1
    if result == Agent.PLAYER_2:
        return 2
    return 0

def simulate_games(game, agent_1:Agent, agent_2:Agent, simulations):
    results = {"Draws":0, "Agent 1 victories":0, "Agent 2 victories":0}
    for i in range(simulations):
        result_index = result_to_list_index(run_game(game, agent_1, agent_2))
        results[list(results)[result_index]] += 1
    
    return results

if __name__ == "__main__":
    #run_game_on_screen(TicTacToe(), RandomAgent(), ShotAgent())
    #run_game_on_screen(RandomAgent(), MinimaxAgent())
    #print(simulate_games(TicTacToe(),  MCTS.UCT(), MCTS.Reclycle_UCT(), 100))
    print(simulate_games(TicTacToe(), RandomAgent(), ShotAgent(), 100))