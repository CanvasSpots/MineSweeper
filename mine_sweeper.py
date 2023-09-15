import time
import random as ran

# Starting Variables -- -- -- --
version= "1.0.2"
title = """

TEXT - BASED -

M   M  I  N   N  EEEEE      /  SSSSS  W   W  EEEEE  EEEEE  PPPP   EEEEE  RRRR
MM MM  I  NN  N  E         /   S      W   W  E      E      P   P  E      R   R
M M M  I  N N N  EEE      /    SSSSS  W W W  EEE    EEE    PPPP   EEE    RRRR
M   M  I  N  NN  E       /         S  WW WW  E      E      P      E      R   R
M   M  I  N   N  EEEEE  /      SSSSS  W   W  EEEEE  EEEEE  P      EEEEE  R   R

                                       Created By: Derek Bauer / version {vers}""".format(vers=version)

gameboard = []
gameboard_text = ""
gamemines = []
actionlist = []

# Difficulties are shown with their row, column, and number of mines.
difficulties = {
    "easy": [9, 9, 10],
    "medium": [16, 16, 40],
    "hard": [16, 30, 99]
}

# Classes -- -- -- --
class Game:
    game_num = 0

    def __init__(self):
        self.game_num = Game.game_num
        Game.game_num += 1

        # Set-up the game's difficulty
        self.difficulty = select_difficulty()
        self.rows = self.difficulty[0]
        self.cols = self.difficulty[1]
        self.mines = self.difficulty[2]

        # Set-up the game's initial information
        self.game_mine = generate_mines(self.rows, self.cols)
        self.gameboard = generate_gameboard(self.rows, self.cols)
    
    def __repr__(self):
        return "This is game {num}.".format(num=self.game_num)
        
class Field:
    total_free = 0
    total_flags = 0

    def __init__(self, init_row, init_col, init_type = "Num"):
        self.name = " "
        self.cord_row = init_row
        self.cord_col = init_col
        self.type = init_type
        self.counter = 0
        self.checkout = True
    
    def __repr__(self):
        return "Field type {type} is located at {row} and {col}.".format(type=self.type, row=self.cord_row, col=self.cord_col)
    
    def mine_counter(self, gameboard, total_rows, total_cols):
        if self.type == "Num":
            count = 0
            for row_plus in range(-1, 2):
                for col_plus in range(-1, 2):
                    test_row = self.cord_row + row_plus
                    test_col = self.cord_col + col_plus 
                    if test_row >= 0 and test_col >= 0 and test_row < total_rows and test_col < total_cols:
                        if gameboard[test_row][test_col].type == "Mine":
                            count += 1
            self.counter = count

    def flag_counter(self, gameboard, total_rows, total_cols):
        count = 0
        for row_plus in range(-1, 2):
            for col_plus in range(-1, 2):
                test_row = self.cord_row + row_plus
                test_col = self.cord_col + col_plus 
                if test_row >= 0 and test_col >= 0 and test_row < total_rows and test_col < total_cols:
                    if gameboard[test_row][test_col].name == "F":
                        count += 1
        return count
    
    def set_spot(self, total_rows, total_cols):
        error = False
        gameover = False
        if self.name == " ":
            if self.type == "Num":
                self.name = str(self.counter)
                Field.total_free -= 1

                # If the flags match the number selected, will check the surrounding cells
                if self.counter == self.flag_counter(gameboard, total_rows, total_cols):
                    for row_plus in range(-1, 2):
                        for col_plus in range(-1, 2):
                            test_row = self.cord_row + row_plus
                            test_col = self.cord_col + col_plus
                            if test_row >= 0 and test_col >= 0 and test_row < total_rows and test_col < total_cols and gameboard[test_row][test_col].name == " ":
                                if check_actions(test_row, test_col):
                                    actionlist.append([test_row, test_col, True])
            else:
                self.name = "M"
                gameover = True                             
        else:
            error = True

        for actions in actionlist:
            if actions[2]:
                actions[2] = False
                gameboard[actions[0]][actions[1]].checkout = False
                gameboard[actions[0]][actions[1]].set_spot(total_rows, total_cols)
        
        if Field.total_free == 0:
            win()
        elif gameover == True:    
            print("You hit a mine!")
            time.sleep(2)
            print("\n- - - Game Over - - -\n")  
            exit()
        elif self.checkout == True:
            if error == True:
                if self.name == "F":
                    print("Sorry, but that location is protected by a flag.")
                else: 
                    print("Sorry, but that locaiton cannot be selected.")
                select_spot(total_rows, total_cols)
            generate_gameboard_text(total_rows, total_cols)
            select_action()
        self.checkout = True

    def set_flag(self, total_rows, total_cols):
        # Sets the current spot to a flag
        error = False
        if self.name == " ":
            self.name = "F"
            Field.total_flags += 1
        elif self.name == "F":
            self.name = " "
            Field.total_flags -= 1
        else:
            error = True
        generate_gameboard_text(total_rows, total_cols)

        if error == True:
            print("Sorry, but that location cannot be flagged.")
            select_flag(total_rows, total_cols)
        select_action()
            
# Functions -- -- -- --
def select_difficulty():
    selection = input("""
What level of difficulty would you like to play on?
    ┌ - - - - - - - - - - - - - - - - - - - - ┐
    | Options: Easy, Medium, Hard, and Custom |
    └ - - - - - - - - - - - - - - - - - - - - ┘
""")
    selection = selection.lower()
    if selection in difficulties:
        return difficulties[selection]
    elif selection == "custom":
        input_rows = int(input("How many rows? "))
        input_cols = int(input("How many columns? "))
        input_mines = int(input("How many mines? "))
        while (input_rows * input_cols) <= input_mines:
            print("It seems you've entered too many mines. Please try again.")
            input_rows = int(input("How many rows? "))
            input_cols = int(input("How many columns? "))
            input_mines = int(input("How many mines? "))
        return [input_rows, input_cols, input_mines]
    else:
        print("Sorry, but that's not a valid difficulty. Please select again. \n")
        select_difficulty()

# Generate mines returns a list of locations the mines can go. Mines cannot be placed on-top of pre-existing mines.
def generate_mines(num_mines, rows, columns):
    for mine in range(0, num_mines):
        mine_row = ran.randint(0, rows - 1)
        mine_col = ran.randint(0, columns - 1)
        while mine_check(mine_row, mine_col):
            mine_row = ran.randint(0, rows - 1)
            mine_col = ran.randint(0, columns - 1)
        gamemines.append({'num': mine, 'row': mine_row, 'col': mine_col})

# Mine check looks to see if a mine exists at the locaiton indicated. Returns a boolean.
def mine_check(check_row, check_col):
    for mine in gamemines:
        if check_row == mine['row'] and check_col == mine['col']:
            return True
    return False

def generate_gameboard(total_rows, total_columns):
    # Generates all the classes in each row of the field.
    for row in range(0, total_rows):
        column_list = []
        for col in range(0, total_columns):
            if mine_check(row, col):
                column_list.append(Field(row, col, "Mine"))
            else:
                column_list.append(Field(row, col))
                Field.total_free += 1
        gameboard.append(column_list)
    
    # Goes through each field item and checks their numbers. 
    # This has to be done after generation so that all instances of the class are on the field to check.
    for row in range(0, total_rows):
        for col in range(0, total_columns):
            gameboard[row][col].mine_counter(gameboard, total_rows, total_columns)

def generate_gameboard_text(rows, cols):
    rows2 = rows * 2 + 1
    cols2 = cols * 2 + 1
    text = ""
    for row in range(0, rows2 + 1):
        for col in range(0, cols2 + 1):
            true_row = int((row - 1) / 2)
            true_col = int((col - 1) / 2)
            if (row == 0) or (col == 0):
                if (row == 0) and (col == 0):
                    text += "  "
                    if rows > 10:
                        text += " "
                elif (row % 2 == 1) or (col % 2 == 1):
                    text += " "
                    if rows > 10 and col == 0:
                        text += " "
                    if col == cols2:
                        text += "\n"
                elif row == 0:
                    text += " " + str(true_col)
                    if true_col < 10:
                        text += " "
                else: 
                    text += str(true_row)
                    if true_row < 10 and rows > 10:
                        text += " "
            elif row == 1:
                if col == 1:
                    text += " ┌ "
                elif col == cols2:
                    text += " ┐ \n"
                elif col % 2 == 1:
                    text += " ┬ "
                else:
                    text += "-"
            elif row == rows2:
                if col == 1:
                    text += " └ "
                elif col == cols2:
                    text += " ┘ "
                elif col % 2 == 1:
                    text += " ┴ "
                else:
                    text += "-"
            elif row % 2 == 1:
                if col == 1:
                    text += " ├ "
                elif col == cols2:
                    text += " ┤ \n"
                elif col % 2 == 1:
                    text += " ┼ "
                else:
                    text += '-'
            else:
                if (col % 2 == 1):
                    text += " | "
                    if col == cols2:
                        text += "\n"
                else:
                    text += gameboard[true_row][true_col].name
    text += "\nThere are {mines} remaining.".format(mines=len(gamemines)-Field.total_flags)
    print(text)
    return text

def select_action():
    selection = "retry"
    selection = input("""
What would you like to do?
    ┌ - - - - - - - - - - - - - - - - - ┐
    | Options: Select, Flag, Quit, Hint |
    └ - - - - - - - - - - - - - - - - - ┘                      
""")
    selection = selection.lower()
    selection += " "
    if "s" in selection[0]:
        if (":" in selection) and ("," in selection):
            split = selection_split(selection)
            select_spot(total_rows, total_cols, int(split[0]), int(split[1]))
        else:
            select_spot(total_rows, total_cols)
    elif "f" in selection[0]:
        if (":" in selection) and ("," in selection):
            split = selection_split(selection)
            select_flag(total_rows, total_cols, int(split[0]), int(split[1]))
        else:
            select_flag(total_rows, total_cols)
    elif "quit" in selection:
        exit()
    elif "h" in selection:
        print("""
    1. To quickly select a cell, try use the syntax s:row,column.
    2. To quickly flag a cell, try using the syntax f:row,column.
    3. Don't worry about upper- or lower-case letters, the program will fix them for you.
    4. Have fun!""")
        select_action()
    else: 
        print("Sorry, but that's not a valid option. Please select again. \n")
        select_action()

def selection_split(selection):
    split_choice = selection.split(":")
    split_select = split_choice[1].split(",")
    if len(split_select) == 2:
        for selection in range(0,len(split_select)):
            split_select[selection] = int(split_select[selection].strip())
    else:
        print("Row and Column selection is invalid, please retry.")
        split_select = [-1, -1]
    return split_select

def select_spot(total_rows, total_cols, init_row = -1, init_col = -1):
    select_row = init_row
    select_col = init_col
    while (select_row < 0) or (select_row >= total_rows):
        select_row = int(input("Which row would you like to select? "))
    while (select_col < 0) or (select_col >= total_cols):
        select_col = int(input("Which column would you like to select? "))
    gameboard[select_row][select_col].set_spot(total_rows, total_cols)

def select_flag(total_rows, total_cols, init_row = -1, init_col = -1):
    select_row = init_row
    select_col = init_col
    while (select_row < 0) or (select_row >= total_rows):
        select_row = int(input("Which row would you like to select? "))
    while (select_col < 0) or (select_col >= total_cols):
        select_col = int(input("Which column would you like to select? "))
    gameboard[select_row][select_col].set_flag(total_rows, total_cols)

def check_actions(check_row, check_col):
    for item in actionlist:
        if item[0] == check_row and item[1] == check_col:
            return False
    return True

# Win / Lose -- -- -- --
def win():
    generate_gameboard_text(total_rows, total_cols)
    print("Congratulations! You won!")
    exit()

# Gameplay -- -- -- --
print('\n\nWelcome to...' + title)
time.sleep(1)

difficulty = select_difficulty()

total_rows = difficulty[0]
total_cols = difficulty[1]
total_mines = difficulty[2]

generate_mines(total_mines, total_rows, total_cols)
generate_gameboard(total_rows, total_cols)
generate_gameboard_text(total_rows, total_cols)
select_action()