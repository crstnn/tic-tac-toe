#!/usr/bin/python3.10
from .state import State
from .token import Token


class TicTacToe:
    _FIELD_CHARS = (Token.NAUGHT, Token.CROSS)
    _BOARD_SIZE = 3  # can be variable

    def __init__(self, board_size: int = 3):
        self._BOARD_SIZE = board_size
        self._current_player_turn: int = 1  # CROSS always starts
        self._state: State = self._get_turn()  # CROSS always starts
        self.col_stat = [self._create_statistic() for _ in range(self._BOARD_SIZE)]
        self.row_stat = [self._create_statistic() for _ in range(self._BOARD_SIZE)]
        self._diag_negative_gradient_stat = self._create_statistic()
        self._diag_positive_gradient_stat = self._create_statistic()
        self._total_placements = 0
        self._board = self._create_board()

    def _create_board(self):
        # init with blank char
        return [[Token.BLANK] * self._BOARD_SIZE for _ in range(self._BOARD_SIZE)]

    def _create_statistic(self):
        return dict(zip(self._FIELD_CHARS, (0, 0)))

    def _get_winner(self):
        match self._current_player_turn:
            case 0:
                return State.NAUGHT_WON
            case 1:
                return State.CROSS_WON
            case _:
                return False

    def _get_turn(self):
        match self._current_player_turn:
            case 0:
                return State.NAUGHT_TURN
            case 1:
                return State.CROSS_TURN
            case _:
                raise Exception(f"Character '{self._current_player_turn}' is not a valid player")

    def _change_turn(self):
        self._current_player_turn = 1 - self._current_player_turn  # flip bit

    @property
    def state(self):
        return self._state

    def place_marker(self, symbol, row, column) -> State:
        if symbol not in self._FIELD_CHARS:
            raise Exception(f"{symbol} is not an accepted char. Use ({', '.join(c.value for c in self._FIELD_CHARS)}).")
        if not self.is_within_range(row) or not self.is_within_range(column):
            raise Exception(f"Position ({row}, {column}) exceeds board range.")
        if (marker := self._board[row][column]) in self._FIELD_CHARS:
            raise Exception(f"Cannot place marker in ({row}, {column}) "
                            f"as a player has already placed a {marker} there.")
        if self._FIELD_CHARS[self._current_player_turn] != symbol:
            raise Exception(f"Other player's turn.")
        self._update_state(symbol, row, column)
        self._state = self._check_state(symbol, row, column)
        self._change_turn()
        return self._state

    def _update_state(self, symbol, curr_placement_row, curr_placement_column):
        self._board[curr_placement_row][curr_placement_column] = symbol

        if curr_placement_row == curr_placement_column:
            self._diag_negative_gradient_stat[symbol] += 1
        if curr_placement_row + curr_placement_column == self._BOARD_SIZE - 1:
            self._diag_positive_gradient_stat[symbol] += 1
        self.row_stat[curr_placement_row][symbol] += 1
        self.col_stat[curr_placement_column][symbol] += 1
        self._total_placements += 1

    def _check_state(self, symbol, curr_placement_row, curr_placement_column) -> State:

        if self.row_stat[curr_placement_row][symbol] == self._BOARD_SIZE \
                or self.col_stat[curr_placement_column][symbol] == self._BOARD_SIZE \
                or self._diag_negative_gradient_stat[symbol] == self._BOARD_SIZE \
                or self._diag_positive_gradient_stat[symbol] == self._BOARD_SIZE:
            return self._get_winner()

        if self._total_placements == self._BOARD_SIZE ** 2:
            return State.DRAW

        return self._get_turn()

    def is_within_range(self, v):
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
