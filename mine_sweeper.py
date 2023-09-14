import time
import random

# Starting Variables -- -- -- --
title = """
M   M  I  N   N  EEEEE      /  SSSSS  W   W  EEEEE  EEEEE  PPPP   EEEEE  RRRR
MM MM  I  NN  N  E         /   S      W   W  E      E      P   P  E      R   R
M M M  I  N N N  EEE      /    SSSSS  W W W  EEE    EEE    PPPP   EEE    RRRR
M   M  I  N  NN  E       /         S  WW WW  E      E      P      E      R   R
M   M  I  N   N  EEEEE  /      SSSSS  W   W  EEEEE  EEEEE  P      EEEEE  R   R"""

game_num = 0
gameboard = []
gameboard_text = ""
gamemines = []
playerboard = []

# Difficulties are shown with their row, column, and number of mines.
difficulties = {
    "easy": [9, 9, 10],
    "medium": [16, 16, 40],
    "hard": [16, 30, 99]
}

# Classes -- -- -- --
class Mine:
    name = "M"
    rows = []
    cols = []

    def __init__(self, mine_num, total_rows, total_cols):
        self.id = mine_num
        self.cord_row = random.randint(0, total_rows)
        self.cord_col = random.randint(0, total_cols)
        self.check_mine(total_rows, total_cols)
    
    def __repr__(self):
        return "Mine {num} is located at {row} and {col}.".format(num=self.id, row=self.cord_row, col=self.cord_col)

    # Checks if the mine already exists at that coordinate. If it does, it generates a new coordinate.
    def check_mine(self, total_rows, total_cols):
        while mine_check(self.cord_row, self.cord_col):
            self.cord_row = random.randint(0, total_rows)
            self.cord_col = random.randint(0, total_cols)
        Mine.rows.append(self.cord_row)
        Mine.cols.append(self.cord_col)


# Functions -- -- -- --
def select_difficulty(game_num):
    difficulty = input("""
What level of difficulty would you like to play on?
    ┌ - - - - - - - - - - - - - - - - - - - - ┐
    | Options: Easy, Medium, Hard, and Custom |
    └ - - - - - - - - - - - - - - - - - - - - ┘
""")
    difficulty = difficulty.lower()
    if difficulty in difficulties:
        # This clears the previous game boards to reset.
        game_num += 1
        gameboard.clear()
        gamemines.clear()
        playerboard.clear()

        num_rows = difficulties[difficulty][0]
        num_columns = difficulties[difficulty][1]
        num_mines = difficulties[difficulty][2]

        generate_mines(num_mines, num_rows, num_columns)
        generate_gameboard(num_rows, num_columns)
        generate_gameboard_text(num_rows, num_columns)
        
    else:
        print("Sorry, but that's not a valid difficulty. Please select again. \n")
        select_difficulty()

def generate_gameboard_text(rows, columns):
    rows2 = rows * 2
    cols2 = columns * 2
    text = ""
    for row in range(0, rows2 + 1):
        for col in range(0, cols2 + 1):
            if row == 0:
                if col == 0:
                    text += " ┌ "
                elif col == cols2:
                    text += " ┐ \n"
                elif col % 2 == 0:
                    text += " ┬ "
                else:
                    text += "-"
            elif row == rows2:
                if col == 0:
                    text += " └ "
                elif col == cols2:
                    text += " ┘ "
                elif col % 2 == 0:
                    text += " ┴ "
                else:
                    text += "-"
            elif row % 2 == 0:
                if col == 0:
                    text += " ├ "
                elif col == cols2:
                    text += " ┤ \n"
                elif col % 2 == 0:
                    text += " ┼ "
                else:
                    text += '-'
            else:
                if (col % 2 == 0):
                    text += " | "
                    if col == cols2:
                        text += "\n"
                else:
                    true_row = int((row - 1) / 2)
                    true_col = int((col - 1) / 2)
                    if gameboard[true_row][true_col] == 0:
                        text += " "
                    else:
                        text += str(gameboard[true_row][true_col])
    print(text)
    return text

def generate_mines(num_mines, rows, columns):
    for mine in range(0, num_mines):
        row = rows - 1
        col = columns - 1
        gamemines.append(Mine(mine, row, col))

def mine_check(check_row, check_col):
    for mine_id in range(0, len(gamemines)):
        if check_row == Mine.rows[mine_id] and check_col == Mine.cols[mine_id]:
            return True
    return False

def generate_gameboard(total_rows, total_columns):
    for row in range(0, total_rows):
        column_list = []
        for col in range(0, total_columns):
            if mine_check(row, col):
                column_list.append(Mine.name)
            else:
                space_num = 0
                for row_add in range(-1, 2):
                    for col_add in range(-1, 2):
                        new_row = row + row_add
                        new_col = col + col_add
                        if mine_check(new_row, new_col):
                            space_num += 1
                column_list.append(space_num)
        gameboard.append(column_list)

# Gameplay -- -- -- --
print('\n\nWelcome to...' + title)
time.sleep(1)

select_difficulty(game_num)