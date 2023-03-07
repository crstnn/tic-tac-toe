import unittest

from ..src.tic_tac_toe import TicTacToe
from ..src.state import State
from ..src.token import Token
from collections import namedtuple

Position = namedtuple("Position", ["row", "column"])


def create_diagonal(t: TicTacToe, char: Token, square: Position, direction: Position):
    while t._is_within_range(square.row) and t._is_within_range(square.column):
        t._board[square.row][square.column] = char
        square = Position(square.row + direction.row, square.column + direction.column)


class TestTicTacToe(unittest.TestCase):
    def test_winner_diagonal1(self):
        t = TicTacToe()
        create_diagonal(t, Token.NAUGHT, Position(0, 0), Position(1, 1))
        self.assertEqual(State.NAUGHT_WON, t.check_state())

    def test_winner_diagonal2(self):
        t = TicTacToe()
        create_diagonal(t, Token.CROSS, Position(t._BOARD_SIZE - 1, t._BOARD_SIZE - 1), Position(-1, -1))
        self.assertEqual(State.CROSS_WON, t.check_state())

    def test_winner_horizontal(self):
        t = TicTacToe()
        t._board[0] = [Token.CROSS for _ in range(t._BOARD_SIZE)]
        self.assertEqual(State.CROSS_WON, t.check_state())

    def test_winner_vertical(self):
        t = TicTacToe()
        for idx in range(t._BOARD_SIZE):
            t._board[idx][0] = Token.NAUGHT
        self.assertEqual(State.NAUGHT_WON, t.check_state())

    def test_change_of_turn(self):
        t = TicTacToe()
        t.place_marker(Token.CROSS, 0, 0)
        t.place_marker(Token.NAUGHT, 2, 1)
        t.place_marker(Token.CROSS, 1, 1)
        t.place_marker(Token.NAUGHT, 1, 2)
        t.place_marker(Token.CROSS, 2, 2)


if __name__ == '__main__':
    unittest.main()
