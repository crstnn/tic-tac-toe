#!/usr/bin/python3.10
from .state import State
from .token import Token


class TicTacToe:
    _FIELD_CHARS = (Token.NAUGHT, Token.CROSS)
    _BOARD_SIZE = 3

    def __init__(self, board_size: int | None = None):
        self._maybe_change_board_size(board_size)
        self._current_player: int = 1  # CROSS always starts
        self._board = self._create_board()

    def _maybe_change_board_size(self, board_size):
        if board_size is not None:
            self._BOARD_SIZE = board_size

    def _create_board(self):
        # init with blank char
        return [[Token.BLANK] * self._BOARD_SIZE for _ in range(self._BOARD_SIZE)]

    def _get_winner(self, char):
        match char:
            case Token.NAUGHT:
                return State.NAUGHT_WON
            case Token.CROSS:
                return State.CROSS_WON
            case _:
                return False

    def _get_turn(self):
        match self._current_player:
            case Token.NAUGHT:
                return State.NAUGHT_TURN
            case Token.CROSS:
                return State.CROSS_TURN
            case _:
                raise Exception(f"character '{self._current_player}' is not a valid player")

    def place_marker(self, symbol, row, column):
        if symbol not in self._FIELD_CHARS:
            raise Exception(f"{symbol} is not an accepted char. Use ({', '.join(c.value for c in self._FIELD_CHARS)}).")
        if not self._is_within_range(row) or not self._is_within_range(column):
            raise Exception(f"Position ({row}, {column}) exceeds board range.")
        if (marker := self._board[row][column]) in self._FIELD_CHARS:
            raise Exception(f"Cannot place marker in ({row}, {column}) "
                            f"as a player has already placed a {marker} there.")
        if self._FIELD_CHARS[self._current_player] != symbol:
            raise Exception(f"Other player's turn.")
        self._board[row][column] = symbol
        self._current_player = 1 - self._current_player  # flip bit

    def check_state(self) -> State:
        is_char_generator = lambda char: lambda span: (c == char for c in span)
        is_naught_generator = is_char_generator(Token.NAUGHT)
        is_cross_generator = is_char_generator(Token.CROSS)
        diag_left_to_right = []
        diag_right_to_left = []
        have_seen_blank_char = False
        for idx in range(self._BOARD_SIZE):
            row = self._board[idx]
            column = tuple(self._board[i][idx] for i in range(self._BOARD_SIZE))
            if any(is_char_generator(Token.BLANK)(row)):
                have_seen_blank_char = True
            if all(is_naught_generator(row)) or all(is_cross_generator(row)) \
                    or all(is_naught_generator(column)) or all(is_cross_generator(column)):
                return self._get_winner(self._board[idx][idx])
            inverse_diag_idx = self._BOARD_SIZE - idx - 1
            diag_left_to_right.append(self._board[idx][idx])
            diag_right_to_left.append(self._board[inverse_diag_idx][idx])

        if diag_left_to_right[0] != Token.BLANK and all(is_char_generator(diag_left_to_right[0])(diag_left_to_right)):
            return self._get_winner(diag_left_to_right[0])
        if diag_right_to_left[0] != Token.BLANK and all(is_char_generator(diag_right_to_left[0])(diag_right_to_left)):
            return self._get_winner(diag_right_to_left[0])

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
