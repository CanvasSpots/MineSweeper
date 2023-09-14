import time
import random

# Starting Variables -- -- -- --
title = """
M   M  I  N   N  EEEEE      /  SSSSS  W   W  EEEEE  EEEEE  PPPP   EEEEE  RRRR
MM MM  I  NN  N  E         /   S      W   W  E      E      P   P  E      R   R
M M M  I  N N N  EEE      /    SSSSS  W W W  EEE    EEE    PPPP   EEE    RRRR
M   M  I  N  NN  E       /         S  WW WW  E      E      P      E      R   R
M   M  I  N   N  EEEEE  /      SSSSS  W   W  EEEEE  EEEEE  P      EEEEE  R   R
"""
reselect_difficulty = False

# Functions -- -- -- --
def select_difficulty():
    difficulty = input("""\
What level of difficulty would you like to play on?
    ┌ - - - - - - - ┐
    | Options: Easy |
    └ - - - - - - - ┘
""")
    if reselect_difficulty == True:
        generate_board

def generate_board(difficulty):
    reselect_difficulty = True
    difficulty = difficulty.lower()
    if difficulty == "easy":
        pass
    else:
        print("Sorry, but that's not a valid difficulty")
        select_difficulty

def generate_mine():
    pass

# Gameplay -- -- -- --
print('\n\nWelcome to...' + title)
time.sleep(3)

select_difficulty
generate_board