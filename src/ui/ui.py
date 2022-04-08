from time import sleep
import os

from agents.agent import Agent

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_piece_simbol(piece):
    if piece == Agent.PLAYER_1: 
        return 'X'
    elif piece == Agent.PLAYER_2:
        return 'O'
    else:
        return '-'

def board_line_to_string(line):
    line_string = ""
    for piece in line:
        line_string += get_piece_simbol(piece)+" "
    return line_string

def print_board_line(line):
    print(board_line_to_string(line))

def print_board(board):
    for line in board:
        print_board_line(line)

def print_result(board, game):
    print(game.state_name(board))

def print_frame(board):
    clear_terminal()
    print_board(board)
    sleep(0.5)