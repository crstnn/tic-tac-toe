#!/usr/bin/python3.10
from enum import IntEnum


class State(IntEnum):
    CROSS_TURN = 0
    NAUGHT_TURN = 1
    DRAW = 2
    CROSS_WON = 3
    NAUGHT_WON = 4
