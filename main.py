import ui
import tictactoe
import agents

def run_game(agent_1:agents.Agent, agent_2:agents.Agent):
    board = tictactoe.get_initial_board()
    while not tictactoe.is_terminal_state(board):
        board = tictactoe.make_move(agent_1.get_move(board), board)
        if not tictactoe.is_terminal_state(board):
            board = tictactoe.make_move(agent_2.get_move(board), board)
    return tictactoe.get_winner(board)

def run_game_on_screen(agent_1:agents.Agent, agent_2:agents.Agent):
    board = tictactoe.get_initial_board()
    ui.print_frame(board)
    while not tictactoe.is_terminal_state(board):
        board = tictactoe.make_move(agent_1.get_move(board), board)
        ui.print_frame(board)
        if not tictactoe.is_terminal_state(board):
            board = tictactoe.make_move(agent_2.get_move(board), board)
            ui.print_frame(board)
    return tictactoe.get_winner(board)


def simulate_games(agent_1:agents.Agent, agent_2:agents.Agent, simulations):
    results = {"Draws":0, "Agent 1 victories":0, "Agent 2 victories":0}
    for i in range(simulations):
        results[list(results)[run_game(agent_1, agent_2)]] += 1
    return results

if __name__ == "__main__":
    #run_game_on_screen(agents.MinimaxAgent(1), agents.SequentialHalvingAgent(2))
    #run_game_on_screen(agents.RandomAgent(1), agents.MinimaxAgent(2))
    print(simulate_games(agents.SequentialHalvingAgent(1), agents.RandomAgent(2), 100))
    #print(simulate_games(agents.RandomAgent(1), agents.RandomAgent(2), 100))