from time import sleep
import tictactoe
import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_piece_simbol(piece):
    if piece == 1: 
        return 'X'
    elif piece == 2:
        return 'O'
    else:
        return '-'

def print_board_line(line):
    print(f"{get_piece_simbol(line[0])} {get_piece_simbol(line[1])} {get_piece_simbol(line[2])}")

def print_board(board):
    for line in board:
        print_board_line(line)

def print_result(board):
    if tictactoe.Game.is_terminal_state(board):
        print(tictactoe.Game.state_name(board))

def print_frame(board):
    clear_terminal()
    print_board(board)
    print_result(board)
    sleep(0.5)
