import pytest
from src.tic_tac_toe import TicTacToe
from src.state import State
from src.token import Token
from collections import namedtuple

Position = namedtuple("Position", ["row", "column"])

BOARD_SIZES = [3, 5, 10, 25, 100, 500]


def create_line_of_moves(game: TicTacToe, square: Position, direction: Position):
    row_col = []
    while game._is_within_range(square.row) and game._is_within_range(square.column):
        row_col.append(Position(square.row, square.column))
        square = Position(square.row + direction.row, square.column + direction.column)
    return row_col


def create_losing_moves(game: TicTacToe, moves_to_miss):
    moves_to_miss = set(moves_to_miss)
    losing_moves = []
    for row in range(game._BOARD_SIZE):
        for column in range(game._BOARD_SIZE):
            if (curr_move := Position(row, column)) not in moves_to_miss:
                losing_moves.append(curr_move)
            if len(losing_moves) == len(moves_to_miss):
                return losing_moves
    return losing_moves


def do_moves_sequentially(board: TicTacToe, winning_moves, losing_moves, winning_player):
    state = None
    losing_player = 1 - winning_player
    # use internal state to change default starting player (allows for easier testing)
    board._current_player = losing_player
    for idx, w_move in enumerate(winning_moves):
        board.place_marker(board._FIELD_CHARS[losing_player], *losing_moves[idx])
        state = board.place_marker(board._FIELD_CHARS[winning_player], *w_move)
    return state


@pytest.mark.parametrize("board_size", BOARD_SIZES)
def test_winner_diagonal(board_size):
    board = TicTacToe(board_size=board_size)
    winning_moves = create_line_of_moves(board, Position(0, 0), Position(1, 1))
    losing_moves = create_losing_moves(board, winning_moves)
    assert do_moves_sequentially(board, winning_moves, losing_moves, 0) == State.NAUGHT_WON


@pytest.mark.parametrize("board_size", BOARD_SIZES)
def test_winner_inverse_diagonal(board_size):
    board = TicTacToe(board_size=board_size)
    winning_moves = create_line_of_moves(board, Position(board._BOARD_SIZE - 1, 0), Position(-1, 1))
    losing_moves = create_losing_moves(board, winning_moves)
    assert do_moves_sequentially(board, winning_moves, losing_moves, 1) == State.CROSS_WON


@pytest.mark.parametrize("board_size", BOARD_SIZES)
def test_winner_horizontal(board_size):
    board = TicTacToe(board_size=board_size)
    winning_moves = create_line_of_moves(board, Position(0, 0), Position(0, 1))
    losing_moves = create_losing_moves(board, winning_moves)
    assert do_moves_sequentially(board, winning_moves, losing_moves, 1) == State.CROSS_WON


@pytest.mark.parametrize("board_size", BOARD_SIZES)
def test_winner_vertical(board_size):
    board = TicTacToe(board_size=board_size)
    winning_moves = create_line_of_moves(board, Position(0, 0), Position(1, 0))
    losing_moves = create_losing_moves(board, winning_moves)
    assert do_moves_sequentially(board, winning_moves, losing_moves, 0) == State.NAUGHT_WON


@pytest.mark.parametrize("board_size", BOARD_SIZES)
def test_reset(board_size):
    board = TicTacToe(board_size=board_size)
    board.place_marker(Token.CROSS, 1, 1)
    board.place_marker(Token.NAUGHT, 0, 0)
    board.reset()
    assert board._board == board._create_board()
    

def test_draw():
    board = TicTacToe(board_size=3)
    board.place_marker(Token.CROSS, 1, 1)
    board.place_marker(Token.NAUGHT, 0, 0)
    board.place_marker(Token.CROSS, 2, 2)
    board.place_marker(Token.NAUGHT, 0, 1)
    board.place_marker(Token.CROSS, 1, 0)
    board.place_marker(Token.NAUGHT, 1, 2)
    board.place_marker(Token.CROSS, 0, 2)
    board.place_marker(Token.NAUGHT, 2, 0)
    assert board.place_marker(Token.CROSS, 2, 1) == State.DRAW
