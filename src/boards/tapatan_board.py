from boards.board import Board


class TapatanBoard(Board):
    def __init__(self, size=3, style=Board.STYLE_DOTS_AND_LINES) -> None:
        super().__init__(size, style)
        self.lines = [
            [[(0, 1), (1, 0), (1, 1)], [(0, 0), (1, 1), (2, 0)], [(1, 0), (1, 1), (2, 1)]],
            [[(0, 0), (0, 2), (1, 1)], [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)], [(2, 0), (2, 2), (1, 1)]],
            [[(0, 1), (1, 2), (1, 1)], [(0, 2), (1, 1), (2, 2)], [(1, 2), (1, 1), (2, 1)]]
        ]
