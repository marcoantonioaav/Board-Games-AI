import os

class ANSIcolors:
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    WHITE = "\033[0;37m"
    NOCOLOR = "\033[0m"

def get_color_string(text:str, color:str = ANSIcolors.NOCOLOR):
    return f"{color}{text}{ANSIcolors.NOCOLOR}"

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')