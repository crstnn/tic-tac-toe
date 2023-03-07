#!/usr/bin/python3.10
from state import State


class TicTacToe:
    _NAUGHT = 'O'
    _CROSS = 'X'
    _BLANK = '-'
    _FIELD_CHARS = (_NAUGHT, _CROSS)
    _BOARD_SIZE = 3

    def __init__(self, board_size: int | None = None):
        self._maybe_change_board_size(board_size)
        self._current_player = self._CROSS
        self._board = self._create_board()

    def _maybe_change_board_size(self, board_size):
        if board_size is not None:
            self._BOARD_SIZE = board_size

    def _create_board(self):
        # init with blank char
        return [[self._BLANK] * self._BOARD_SIZE for _ in range(self._BOARD_SIZE)]

    def _get_winner(self, char):
        match char:
            case self._NAUGHT:
                return State.NAUGHT_WON
            case self._CROSS:
                return State.CROSS_WON
            case _:
                return False

    def _get_turn(self):
        match self._current_player:
            case self._NAUGHT:
                return State.NAUGHT_TURN
            case self._CROSS:
                return State.CROSS_TURN
            case _:
                raise Exception(f"character '{self._current_player}' is not a valid player")

    def place_marker(self, symbol, row, column):
        if symbol not in self._FIELD_CHARS:
            raise Exception(f"{symbol} is not an accepted char. Use ({', '.join(self._FIELD_CHARS)}).")
        if self._is_within_range(row) and self._is_within_range(column):
            raise Exception(f"Position ({row}, {column}) exceeds board range.")
        if marker := self._board[row][column] in self._FIELD_CHARS:
            raise Exception(f"Cannot place marker in ({row}, {column}) "
                            f"as a player has already placed a {marker} there.")
        if self._current_player != symbol:
            raise Exception(f"Other player's turn.")
        self._board[row][column] = symbol

    def check_state(self) -> State:
        is_char = lambda char: (c == char for c in row)
        diagonal_left_to_right = []
        diagonal_right_to_left = []
        diag_idx = 0
        have_seen_blank_char = False
        for row in self._board:
            if any(is_char(self._BLANK)):
                have_seen_blank_char = True
            elif all(is_char(self._NAUGHT)) or all(is_char(self._CROSS)):
                return self._get_winner(row[0])
            inverse_diag_idx = self._BOARD_SIZE - diag_idx - 1
            diagonal_left_to_right.append(row[diag_idx][diag_idx])
            diagonal_right_to_left.append(row[inverse_diag_idx][inverse_diag_idx])
            diag_idx += 1

        if diagonal_left_to_right[0] != self._BLANK != diagonal_right_to_left[0] \
                and (all(diagonal_left_to_right) or all(diagonal_right_to_left)):
            return self._get_winner(diagonal_left_to_right[0]) or self._get_winner(diagonal_right_to_left[0])

        if have_seen_blank_char:
            return self._get_turn()
        return State.DRAW

    def _is_within_range(self, v):
        return 0 <= v < self._BOARD_SIZE

    def reset(self):
        new_tic_tac_toe = TicTacToe(self._BOARD_SIZE)
        self.__dict__ = new_tic_tac_toe.__dict__

    def __str__(self):
        underline_on = "\033[4m"
        underline_off = "\033[0m"

        heading_numbers = (str(col_idx + 1) for col_idx in range(self._BOARD_SIZE))
        return_str = [f"{underline_on} | {' '.join(heading_numbers)}{underline_off}"]
        for row_idx, row in enumerate(self._board):
            return_str.append(f"{row_idx + 1}| {' '.join(row)}")

        return '\n'.join(return_str)
