from boards.board import Board


class TicTacToeBoard(Board):
    def __init__(self, size=3, style=Board.STYLE_SQUARES) -> None:
        super().__init__(size, style)