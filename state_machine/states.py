from enum import Enum

class match_state(Enum):
    p1_win = 0
    p2_win = 1
    tie = 2
    betting_open = 3
    regular_match = 4

    invalid = 5

__state__ = match_state.invalid

def set_state(state):
    __match_state__ = state

def get_state(state):
    return __match_state__

def function_P1_win():
    pass

def function_P2_win():
    pass

def function_tie():
    pass

def function_betting_open():
    pass

def function_regular_match():
    pass
