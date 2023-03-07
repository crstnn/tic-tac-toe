#!/usr/bin/python3.10
from enum import IntEnum


class State(IntEnum):
    DRAW = 1
    CROSS_TURN = 2
    NAUGHT_TURN = 3
    CROSS_WON = 4
    NAUGHT_WON = 5
