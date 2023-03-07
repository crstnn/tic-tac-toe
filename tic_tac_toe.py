#!/usr/bin/python3.10
from state import State


class TicTacToe:
    FIELD_CHARS = ('O', 'X')
    BLANK_CHAR = '-'
    BOARD_SIZE = 3

    def __init__(self, board_size: int | None = None):
        if board_size is not None:
            self.BOARD_SIZE = board_size
        self._board = self._create_board()

    def _create_board(self):
        # init with blank char
        return [[self.BLANK_CHAR] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]

    def _get_winner(self, char):
        return {self.FIELD_CHARS[0]: State.NAUGHT_WON, self.FIELD_CHARS[1]: State.CROSS_WON}[char]

    def _get_turn(self, char):
        return {self.FIELD_CHARS[0]: State.NAUGHT_TURN, self.FIELD_CHARS[1]: State.CROSS_TURN}[char]

    def place_marker(self, symbol, row, column):
        if symbol not in self.FIELD_CHARS:
            raise Exception(f"{symbol} is not an accepted char. Use ({', '.join(self.FIELD_CHARS)})")
        if self._is_within_range(row) and self._is_within_range(column):
            raise Exception(f"Position ({row}, {column}) exceeds board range")
        if marker := self._board[row][column] in self.FIELD_CHARS:
            raise Exception(f"Cannot place marker in ({row}, {column}) "
                            f"as a player has already placed a {marker} there.")
        self._board[row][column] = symbol

    def check_state(self) -> State:
        diagonal_left_to_right = []
        diagonal_right_to_left = []
        diag_idx = 0
        state = False
        for row in self._board:
            if row[0] != self.BLANK_CHAR and all(row):
                state = row[0]
                break
            inverse_diag_idx = self.BOARD_SIZE - diag_idx - 1
            diagonal_left_to_right.append(row[diag_idx][diag_idx])
            diagonal_right_to_left.append(row[inverse_diag_idx][inverse_diag_idx])
            diag_idx += 1

        if not state and diagonal_left_to_right[0] != self.BLANK_CHAR and all(diagonal_left_to_right):
            state = diagonal_left_to_right[0]
        elif not state and diagonal_right_to_left[0] != self.BLANK_CHAR and all(diagonal_right_to_left):
            state = diagonal_right_to_left[0]

        # TODO: deal with other states

        if state:
            return self._get_winner(state)

    def _is_within_range(self, v):
        return 0 <= v < self.BOARD_SIZE

    def reset(self):
        self._board = self._create_board()

    def print_board(self):
        underline_on = "\033[4m"
        underline_off = "\033[0m"

        heading_numbers = (str(col_idx + 1) for col_idx in range(self.BOARD_SIZE))
        print(f"{underline_on} | {' '.join(heading_numbers)}{underline_off}")
        for row_idx, row in enumerate(self._board):
            print("%d| %s" % (row_idx + 1, " ".join(row)))
