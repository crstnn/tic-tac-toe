import pytest
from src.tic_tac_toe import TicTacToe
from src.state import State
from src.token import Token
from collections import namedtuple

Position = namedtuple("Position", ["row", "column"])

BOARD_SIZES = [3, 4, 5, 20, 100]


def create_diagonal(t: TicTacToe, char: Token, square: Position, direction: Position):
    while t._is_within_range(square.row) and t._is_within_range(square.column):
        t._board[square.row][square.column] = char
        square = Position(square.row + direction.row, square.column + direction.column)


@pytest.mark.parametrize("board_size", BOARD_SIZES)
def test_winner_diagonal1(board_size):
    t = TicTacToe(board_size=board_size)
    create_diagonal(t, Token.NAUGHT, Position(0, 0), Position(1, 1))
    assert t.check_state() == State.NAUGHT_WON


@pytest.mark.parametrize("board_size", BOARD_SIZES)
def test_winner_diagonal2(board_size):
    t = TicTacToe(board_size=board_size)
    create_diagonal(t, Token.CROSS, Position(t._BOARD_SIZE - 1, t._BOARD_SIZE - 1), Position(-1, -1))
    assert t.check_state() == State.CROSS_WON


@pytest.mark.parametrize("board_size", BOARD_SIZES)
def test_winner_horizontal(board_size):
    t = TicTacToe(board_size=board_size)
    t._board[0] = [Token.CROSS for _ in range(t._BOARD_SIZE)]
    assert t.check_state() == State.CROSS_WON


@pytest.mark.parametrize("board_size", BOARD_SIZES)
def test_winner_vertical(board_size):
    t = TicTacToe(board_size=board_size)
    for idx in range(t._BOARD_SIZE):
        t._board[idx][0] = Token.NAUGHT
    assert t.check_state() == State.NAUGHT_WON


@pytest.mark.parametrize("board_size", BOARD_SIZES)
def test_change_of_turn(board_size):
    t = TicTacToe(board_size=board_size)
    t.place_marker(Token.CROSS, 0, 0)
    t.place_marker(Token.NAUGHT, 2, 1)
    t.place_marker(Token.CROSS, 1, 1)
    t.place_marker(Token.NAUGHT, 1, 2)
    t.place_marker(Token.CROSS, 2, 2)
    if board_size == 3:
        assert t.check_state() == State.CROSS_WON

@pytest.mark.parametrize("board_size", BOARD_SIZES)
def test_reset(board_size):
    t = TicTacToe(board_size=board_size)
    t.place_marker(Token.CROSS, 1, 1)
    t.place_marker(Token.NAUGHT, 0, 0)
    t.reset()
    assert t._board == t._create_board()


