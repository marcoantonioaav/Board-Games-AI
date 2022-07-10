import timeit

from agents.agent import Agent
from agents.minimax import MinimaxAgent
from agents.sequential_halving import SequentialHalvingAgent, ShotAgent, ShotTreeAgent
from agents.random import RandomAgent
from agents.UCT import UCT
from agents.Recycle_UCT import Recycle_UCT
from agents.TT_UCT import TT_UCT
from agents.NestedSH import NestedSH

from ui.game_screen import print_frame, print_result
from games.tictactoe import TicTacToe
from games.AGT import AGTree
from ui.simulation_screen import print_simulation_frame

def run_game(game, agent_1:Agent, agent_2:Agent):
    agent_1.set_game(game), agent_2.set_game(game)
    agent_1.set_player(Agent.PLAYER_1), agent_2.set_player(Agent.PLAYER_2)

    board = game.get_initial_board()
    while not game.is_terminal_state(board):
        board = game.apply(agent_1.select_action(game, board), board)
        if not game.is_terminal_state(board):
            board = game.apply(agent_2.select_action(game, board), board)
    return game.get_winner(board)

def run_game_on_screen(game, agent_1:Agent, agent_2:Agent):
    agent_1.set_game(game), agent_2.set_game(game)
    agent_1.set_player(Agent.PLAYER_1), agent_2.set_player(Agent.PLAYER_2)

    board = game.get_initial_board()
    print_frame(board)
    while not game.is_terminal_state(board):
        board = game.apply(agent_1.select_action(game, board), board)
        print_frame(board)
        if not game.is_terminal_state(board):
            board = game.apply(agent_2.select_action(game, board), board)
            print_frame(board)
    print_result(board, game)
    return game.get_winner(board)

def result_to_list_index(result, agent_1:Agent, agent_2:Agent):
    if result == agent_1.player:
        return 1
    if result == agent_2.player:
        return 2
    return 0

def simulate_games(game, agent_1:Agent, agent_2:Agent, simulations, use_ui=True):
    results = {"Draws":0, f"{agent_1.get_name()} victories":0, f"{agent_2.get_name()} victories":0}
    time_spent = 0
    for simulation in range(simulations):
        start_time = timeit.default_timer()
        if simulation%2 == 0:
            result = run_game(game, agent_1, agent_2)
        else:
            result = run_game(game, agent_2, agent_1)
        stop_time = timeit.default_timer()
        result_index = result_to_list_index(result, agent_1, agent_2)
        results[list(results)[result_index]] += 1
        time_spent += stop_time-start_time
        if use_ui:
            print_simulation_frame(simulation, simulations, time_spent/(simulation+1))
    return results

def something(ag, BEST_ACTION):
    game = AGTree("SHOTTree")
    board = game.get_initial_board()
    
    #simul = [1,2,3,4,5,6,7,8,9,10,15,30, 50, 100, 1000]
    simul = [100]
    dic = {}
    while simul != []:    
        episodes = simul.pop(0)
        c_count = 0
        for i in range(1):
            result = ag.select_action(game, board, max_episodes=episodes)
        #print(result)
            if result == BEST_ACTION:
                c_count+=1
        dic[episodes] = c_count
        #print(c_count)
    print(dic)

if __name__ == "__main__":
    #run_game_on_screen(TicTacToe(), RandomAgent(), ShotTreeAgent())
    #run_game_on_screen(RandomAgent(), MinimaxAgent())
    #print(simulate_games(TicTacToe(),  MCTS.UCT(), MCTS.Recycle_UCT(), 100))
    print(simulate_games(TicTacToe(), NestedSH(), RandomAgent(), 100))

    # ag = TT_UCT()
    # ag.set_player(Agent.PLAYER_1)
    # something(ag,'l')


    #ag = CanonicalShot()
    #ag.set_player(Agent.PLAYER_1)
    #something(ag, 'c')

    
