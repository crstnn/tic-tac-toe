from src.tic_tac_toe import TicTacToe
from src.state import State
from src.token import Token
from collections import namedtuple

import pytest

Position = namedtuple("Position", ["row", "column"])


def create_diagonal(t: TicTacToe, char: Token, square: Position, direction: Position):
    while t._is_within_range(square.row) and t._is_within_range(square.column):
        t._board[square.row][square.column] = char
        square = Position(square.row + direction.row, square.column + direction.column)


def test_winner_diagonal1():
    t = TicTacToe()
    create_diagonal(t, Token.NAUGHT, Position(0, 0), Position(1, 1))
    assert t.check_state() == State.NAUGHT_WON


def test_winner_diagonal2():
    t = TicTacToe()
    create_diagonal(t, Token.CROSS, Position(t._BOARD_SIZE - 1, t._BOARD_SIZE - 1), Position(-1, -1))
    assert t.check_state() == State.CROSS_WON


def test_winner_horizontal():
    t = TicTacToe()
    t._board[0] = [Token.CROSS for _ in range(t._BOARD_SIZE)]
    assert t.check_state() == State.CROSS_WON


def test_winner_vertical():
    t = TicTacToe()
    for idx in range(t._BOARD_SIZE):
        t._board[idx][0] = Token.NAUGHT
    assert t.check_state() == State.NAUGHT_WON


def test_change_of_turn():
    t = TicTacToe()
    t.place_marker(Token.CROSS, 0, 0)
    t.place_marker(Token.NAUGHT, 2, 1)
    t.place_marker(Token.CROSS, 1, 1)
    t.place_marker(Token.NAUGHT, 1, 2)
    t.place_marker(Token.CROSS, 2, 2)
