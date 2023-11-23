from time import sleep

from agents.agent import Agent
from boards.board import Board
from boards.tapatan_board import TapatanBoard
from boards.tictactoe_board import TicTacToeBoard
from ui.util import *

def print_board(board):
    #print(TapatanBoard().to_string(board))
    #print()
    print(TicTacToeBoard().to_string(board))

def print_result(board, game):
    print(game.state_name(board))

def print_frame(board):
    clear_terminal()
    print_board(board)
    sleep(0.5)