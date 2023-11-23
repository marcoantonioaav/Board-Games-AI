from agents.agent import Agent
from ui.util import ANSIcolors, get_color_string


class Board:
    STYLE_DOTS_AND_LINES = 0
    STYLE_SQUARES = 1

    def __init__(self, size=3, style=STYLE_SQUARES) -> None:
        self.set_size(size)
        self.style = style

    def set_size(self, size:int) -> None:
        self.size = size
        self.lines = [ [ [] for i in range(size) ] for j in range(size) ]

    def get_piece_simbol(self, piece):
        if piece == Agent.PLAYER_1: 
            if self.style == self.STYLE_DOTS_AND_LINES:
                return get_color_string('●', ANSIcolors.GREEN)
            else:
                return get_color_string('⨯', ANSIcolors.GREEN)
        elif piece == Agent.PLAYER_2:
            if self.style == self.STYLE_DOTS_AND_LINES:
                return get_color_string('●', ANSIcolors.RED)
            else:
                return get_color_string('○', ANSIcolors.RED)
        else:
            if self.style == self.STYLE_DOTS_AND_LINES:
                return '∘'
            else:
                return ' '

    def board_line_to_string(self, line, y):
        line_string = ""
        for x, piece in enumerate(line):
            line_string += ' ' + self.get_piece_simbol(piece)
            if x != self.size-1:
                if self.style == self.STYLE_DOTS_AND_LINES:
                    if self.lines[y][x].count((x+1, y)) == 1:
                        line_string += ' ─'
                    else:
                        line_string += '  '
                else:
                    line_string += ' │'
        return line_string
    
    def board_line_between_to_string(self, upper_y):
        line_string = ""
        if self.style == self.STYLE_DOTS_AND_LINES:
            for x in range(self.size):
                if self.lines[upper_y][x].count((x, upper_y+1)) == 1:
                    line_string += ' │'
                if x != self.size-1:
                    has_decrescent_diagonal = self.lines[upper_y][x].count((x+1, upper_y+1)) == 1
                    has_crescent_diagonal = self.lines[upper_y+1][x].count((x+1, upper_y)) == 1
                    if has_decrescent_diagonal and has_crescent_diagonal:
                        line_string += ' ╳'
                    elif has_decrescent_diagonal:
                        line_string += ' ╲'
                    elif has_crescent_diagonal:
                        line_string += ' ╱'
                    else:
                        line_string += '  '
        else:
            line_string += '───┼───┼───'
        return line_string

    def to_string(self, state) -> str:
        string = ""
        for index, line in enumerate(state):
            string += self.board_line_to_string(line, index) 
            if index != self.size-1:
                string += '\n' + self.board_line_between_to_string(index) + '\n'
        return string
