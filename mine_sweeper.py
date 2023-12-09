import time
import random as ran

# Starting Variables -- -- -- --
version= "1.1.6C"
title = """

TEXT - BASED -

M   M  I  N   N  EEEEE      /  SSSSS  W   W  EEEEE  EEEEE  PPPP   EEEEE  RRRR
MM MM  I  NN  N  E         /   S      W   W  E      E      P   P  E      R   R
M M M  I  N N N  EEE      /    SSSSS  W W W  EEE    EEE    PPPP   EEE    RRRR
M   M  I  N  NN  E       /         S  WW WW  E      E      P      E      R   R
M   M  I  N   N  EEEEE  /      SSSSS  W   W  EEEEE  EEEEE  P      EEEEE  R   R

                                      Created By: CanvasSpots / version {vers}""".format(vers=version)

gameboard_text = ""

bad_hints = [
    ""
]

# Classes -- -- -- --
class Game:
    # Game number shows total games, wins, and cells cleared
    game_num = [0, 0, 0]
    # Difficulties are arranged in the following order: Rows, columns, and mines; then total played.
    difficulties = {
    "easy": [9, 9, 10, 0],
    "medium": [16, 16, 40, 0],
    "hard": [16, 30, 99, 0],
    "customs": [0, 0, 0, 0]
    }

    def __init__(self):
        Game.game_num[0] += 1
        self.game_num = Game.game_num[0]

        # Initiate game-dependent variables
        self.game_mines = []
        self.gameboard = []
        self.action_list = []

        # Set-up the game's difficulty
        self.difficulty = []
        self.rows = 0
        self.cols = 0
        self.mines = 0
    
    def __repr__(self):
        loss = Game.game_num[0] - Game.game_num[1] - 1
        if loss > 0:
            win_loss = Game.game_num[1] / loss
        else: 
            win_loss = 1
        return_text = "This account has a total of {win} wins and {loss} losses for an overall win/loss ratio of {winloss}.".format(win=Game.game_num[1], loss=loss, winloss=win_loss)
        
        return_text += "\nThis account has played {easy} easy games, {med} medium games, {hard} hard games, and {cust} custom games.".format(easy=Game.difficulties["easy"][3], med=Game.difficulties["medium"][3], hard=Game.difficulties["hard"][3], cust=Game.difficulties["customs"][3])

        return_text += "\n\nThis account has cleared {tiles} cells from mines.".format(tiles=Game.game_num[2])

        return_text += "\n\nThis is game {num}.".format(num=self.game_num)
        return return_text

    # Start a New Game -- --
    def start_game(self):
        game_options = ["n", "l", "e", "s", "q"]
        game_select = input("""
    ┌ - - - - - - - - - - - - - - - - - - - - -┐
    | New Game, Load Game, Extras, Stats, Quit |
    └ - - - - - - - - - - - - - - - - - - - - -┘
""") + " "
        while game_select[0] not in game_options:
            print("Sorry, but that's not a valid option. Please select again. \n")
            game_select = input("""
    ┌ - - - - - - - - - - - - - - - - - - - - -┐
    | New Game, Load Game, Extras, Stats, Quit |
    └ - - - - - - - - - - - - - - - - - - - - -┘
""") + " "
        game_select = game_select.lower()
        if "n" in game_select[0]:
            print("     -- -- INITIALIZING GAME NUMBER {game} -- --".format(game=self.game_num))
            self.difficulty = select_difficulty()
            self.rows = self.difficulty[0]
            self.cols = self.difficulty[1]
            self.mines = self.difficulty[2]

            self.game_mines.clear()
            self.gameboard.clear()

            first_selection = self.first_action()
            self.game_mines = self.generate_mines(first_selection)
            self.gameboard = self.generate_gameboard()
            self.select_spot(first_selection)
        elif "l" in game_select[0]:
            print('Sorry, but lading is not available at this time.')
            self.start_game()
        elif "e" in game_select[0]:
            print("Sorry, but there are no extras available at this time.")
            self.start_game()
        elif "s" in game_select[0]:
            print(self)
            self.start_game()
        else:
            exit()

    # Gameboard Generators -- --
    # Generate mines returns a list of locations the mines can go. Mines cannot be placed on-top of pre-existing mines.
    def generate_mines(self, first_selection):
        game_gen_mines =[{'num': 0, 'row': first_selection[0], 'col': first_selection[1]}]
        for mine in range(1, self.mines + 1):
            mine_row = ran.randint(0, self.rows - 1)
            mine_col = ran.randint(0, self.cols - 1)
            while mine_check(game_gen_mines, mine_row, mine_col):
                mine_row = ran.randint(0, self.rows - 1)
                mine_col = ran.randint(0, self.cols - 1)
            game_gen_mines.append({'num': mine, 'row': mine_row, 'col': mine_col})
        return game_gen_mines
    
    # Generates the gameboard by first creating a "Field" class for each cell and setting them to mine or number. After the field has been set, the numbers will correctly calculate how many mines are around them. As I think abou this, I could have added a script to add to all surrounding cells using the mines, but I didn't.
    def generate_gameboard(self):
        gameboard = []
        Field.total_free = 0
        Field.total_flags = 1
        for row in range(0, self.rows):
            column_list = []
            for col in range(0, self.cols):
                if mine_check(self.game_mines, row, col, False):
                    column_list.append(Field(row, col, "Mine"))
                else:
                    column_list.append(Field(row, col))
                    Field.total_free += 1
            gameboard.append(column_list)
        
        # Goes through each field item and checks their numbers. This has to be done after generation so that all instances of the class are on the field to check.
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                gameboard[row][col].mine_counter(gameboard, self.rows, self.cols)
        
        return gameboard
    
    # Win / Lose -- -- -- --
    def win(self):
        generate_gameboard_text(self.rows, self.cols)
        print("CONGRATULATIONS!! YOU WON!")
        Game.game_num[1] += 1

        time.sleep(2)
        print("\n- - - Game Over - - -\n")

        time.sleep(2)
        play_again()

    def lose(self):
        generate_gameboard_text(self.rows, self.cols)
        print("YOU IDIOT. YOU HIT A MINE!")
        Game.game_num[2] += 1
        
        time.sleep(2)
        print("\n- - - Game Over - - -\n")  
        time.sleep(2)
        play_again()
    
    # Player Actions -- --
    #Divides the action based on if this is the first one or any one afterwards. First selection is bomb-free.
    def first_action(self):
        selection_options = ["s", "m", "q", "h"]
        selection = input("""
    Your first selection is always free.
    
    WHAT WOULD YOU LIKE TO DO?
    ┌ - - - - - - - - - - - - - - ┐
    | Options: Select, Main, Hint |
    └ - - - - - - - - - - - - - - ┘\n""") + " "
        while selection[0] not in selection_options:
            print("Sorry, but that's not a valid option. Please select again.")
            selection = input("""
    Your first selection is always free.
    
    WHAT WOULD YOU LIKE TO DO?
    ┌ - - - - - - - - - - - - - - ┐
    | Options: Select, Main, Hint |
    └ - - - - - - - - - - - - - - ┘\n""") + " "
        selection = selection.lower()

        if "s" in selection[0]:
            if (":" in selection) and ("," in selection):
                start_spot = selection_split(selection)
                if type(start_spot[0]) == type(int()) and type(start_spot[1]) == type(int()):
                        return start_spot
            start_spot = [self.rows + 1, -1]
            while (0 > start_spot[0]) or (start_spot[0] >= self.rows):
                select = input("\nWhich row would you like to select? ")
                while check_select(select, self.rows) == False:
                    select = input("Which row would you like to select? ")
                start_spot[0] = int(select)
            while (0 > start_spot[1]) or (start_spot[1] >= self.cols):
                select = input("\nWhich column would you like to select? ")
                while check_select(select, self.cols) == False:
                    select = input("Which column would you like to select? ")
                start_spot[1] = int(select)
            return start_spot
        elif "m" in selection[0]:
            self.start_game()
        elif "q" in selection[0]:
            exit()
        elif "h" in selection:
            print("""
    1. To quickly select a cell, try use the syntax s:row,column.
    2. Main will return you to the main menu.
    3. You can always quit the game with "quit".
    4. Don't worry about upper- or lower-case letters, the program will fix them for you.
    5. Have fun!""")
            self.select_action()
    
    # Lets the player select what they'll be doing next. Added in hints to help players go faster.
    def select_action(self):
        selection_options = ["s", "f", "m", "q", "h"]
        selection = input("""
    WHAT WOULD YOU LIKE TO DO?
    ┌ - - - - - - - - - - - - - - - - - ┐
    | Options: Select, Flag, Main, Hint |
    └ - - - - - - - - - - - - - - - - - ┘\n""") + " "
        while selection[0] not in selection_options:
            print("Sorry, but that's not a valid option. Please select again.")
            selection = input("""
    WHAT WOULD YOU LIKE TO DO?
    ┌ - - - - - - - - - - - - - - - - - ┐
    | Options: Select, Flag, Main, Hint |
    └ - - - - - - - - - - - - - - - - - ┘\n""") + " "
        selection = selection.lower()

        # When using the quick input, this divides the selection into 
        if "s" in selection[0]:
            if (":" in selection) and ("," in selection):
                split = selection_split(selection)
                if type(split[0]) == type(int()) and type(split[1]) == type(int()):
                    self.select_spot(split)
                else:
                    self.select_spot()
            else:
                self.select_spot()
        elif "f" in selection[0]:
            if (":" in selection) and ("," in selection):
                split = selection_split(selection)
                self.select_flag(split)
            else:
                self.select_flag()
        elif "main" in selection:
            Game.game_num[2] += 1
            gamelist.append(Game())
            gamelist[-1].start_game()
        elif "quit" in selection:
            exit()
        elif "h" in selection:
            print("""
        1. To quickly select a cell, try use the syntax s:row,column.
        2. To quickly flag a cell, try using the syntax f:row,column.
        3. Main will return you to the main menu.
        4. You can always quit the game with "quit".
        5. Don't worry about upper- or lower-case letters, the program will fix them for you.
        6. Have fun!""")
            self.select_action()
        else: 
            print("Sorry, but that's not a valid option. Please select again. \n")
            self.select_action()
        
    # If selecting a spot, this checks that both a row and a column have been selected. If not, asks for a new row and column selection before initiating the Field.set_spot method.
    def select_spot(self, init_spot = [-1, -1]):
        select_row = init_spot[0]
        select_col = init_spot[1]
        while (0 > select_row) or (select_row >= self.rows):
            select = input("\nWhich row would you like to select? ")
            while check_select(select, self.rows) == False:
                select = input("Which row would you like to select? ")
            select_row = int(select)
        while (0 > select_col) or (select_col >= self.cols):
            select = input("\nWhich column would you like to select? ")
            while check_select(select, self.cols) == False:
                select = input("Which column would you like to select? ")
            select_col = int(select)
        self.gameboard[select_row][select_col].set_spot(self.gameboard, self.action_list, self.rows, self.cols)

    # If flagging a spot, this checks that both a row and a column have been selected. If not, asks for a new row and column selection before initiating the Field.set_flag method.
    def select_flag(self, init_spot = [-1, -1]):
        select_row = init_spot[0]
        select_col = init_spot[1]
        while (0 > select_row >= self.rows):
            select = input("Which row would you like to select? ")
            while check_select(select, self.rows) == False:
                select = input("Which row would you like to select? ")
            select_row = int(select)
        while (0 > select_col >= self.cols):
            select = input("\nWhich column would you like to select? ")
            while check_select(select, self.cols) == False:
                select = input("Which column would you like to select? ")
            select_col = int(select)
        self.gameboard[select_row][select_col].set_flag(self.rows, self.cols)

        
class Field:
    total_free = 0
    total_flags = 0

    def __init__(self, init_row, init_col, init_type = "Num"):
        self.name = "◻"
        self.cord_row = init_row
        self.cord_col = init_col
        self.type = init_type
        self.counter = 0
        self.checkout = True
    
    def __repr__(self):
        return "Field type {type} is located at {row} and {col}.".format(type=self.type, row=self.cord_row, col=self.cord_col)
    
    # Counts the number of mines around the currently selected cell.
    def mine_counter(self, gameboard, rows, cols):
        if self.type == "Num":
            count = 0
            for row_plus in range(-1, 2):
                for col_plus in range(-1, 2):
                    test_row = self.cord_row + row_plus
                    test_col = self.cord_col + col_plus 
                    if row_plus == 0 and col_plus == 0:
                        pass
                    elif test_row >= 0 and test_col >= 0 and test_row < rows and test_col < cols:
                        if gameboard[test_row][test_col].type == "Mine":
                            count += 1
            self.counter = count

    # Counts the number of flags around the currently selected cell.
    def flag_counter(self, gameboard, rows, cols):
        count = 0
        for row_plus in range(-1, 2):
            for col_plus in range(-1, 2):
                test_row = self.cord_row + row_plus
                test_col = self.cord_col + col_plus
                if row_plus == 0 and col_plus == 0:
                    pass
                elif test_row >= 0 and test_col >= 0 and test_row < rows and test_col < cols:
                    if gameboard[test_row][test_col].name == "⚑":
                        count += 1
        return count
    
    # Checks the selected cell. If the cell is a number, reveals the number. If the cell is a bomb, reveals the bomb and ends the game in a loss. And if all cells have been flipped, ends the game in a win.
    def set_spot(self, gameboard, action_list, rows, cols):
        error = False
        gameover = False
        if self.name == "◻":
            if self.type == "Num":
                if self.counter == 0:
                    self.name = " "
                else:
                    self.name = str(self.counter)
                Field.total_free -= 1
                Game.game_num[2] += 1

                # If the number of flags indicated in the cell match the number selected, this will add each cell surrounding the current one to the action list. Action list will then repeat the set_spot function to find more empty cells (or can end the game if the wrong cell is flagged). 
                # Trust me, this small piece of code makes the game so much better.
                if self.counter == self.flag_counter(gameboard, rows, cols):
                    for row_plus in range(-1, 2):
                        for col_plus in range(-1, 2):
                            test_row = self.cord_row + row_plus
                            test_col = self.cord_col + col_plus
                            if row_plus == 0 and col_plus == 0:
                                pass
                            elif (0 <= test_row < rows) and (0 <= test_col < cols) and gameboard[test_row][test_col].name == "◻":
                                if check_actions(test_row, test_col):
                                    action_list.append([test_row, test_col, True])
            else:
                self.name = "M"
                gameover = True                             
        else:
            error = True

        for action in action_list:
            if action[2]:
                action[2] = False
                gameboard[action[0]][action[1]].checkout = False
                gameboard[action[0]][action[1]].set_spot(gameboard, action_list, rows, cols)
        
        if Field.total_free == 0:
            gamelist[-1].win()
        elif gameover == True:
            gamelist[-1].lose()

        # Checkout refers to if the cell has been checked-out by the player or by the game. If the cell is checked-out by the player, there is a change they've selected a flag cell or a number cell and needs to be re-selected. Also lets the player select a new action after correctly selecting a cell.
        elif self.checkout == True:
            if error == True:
                if self.name == "⚑":
                    print("Sorry, but that location is protected by a flag.")
                else: 
                    print("Sorry, but that location cannot be selected.")
                    gamelist[-1].select_spot()
            
            else:
                generate_gameboard_text(gamelist[-1].rows, gamelist[-1].cols)
            gamelist[-1].select_action()
        self.checkout = True

    # Sets the current spot to a flag or changes it to not a flag. Also changes quantity of remaining bombs. If a location is already unlocked, it will request a new action.
    def set_flag(self, rows, cols):
        error = False
        if self.name == "◻":
            self.name = "⚑"
            Field.total_flags += 1
        elif self.name == "⚑":
            self.name = "◻"
            Field.total_flags -= 1
        else:
            error = True
        generate_gameboard_text(rows, cols)

        if error == True:
            print("Sorry, but that location cannot be flagged.")
            gamelist[-1].select_flag()
        else:
            gamelist[-1].select_action()
            
# Functions -- -- -- --
# Lets the player select their level of difficulty. Easy, Medium, and Hard mode rows, columns, and mines taken from real Minesweeper. Custom builds a board as big as the player wants with as many mines as they want, but there must always be at least one cell must not be a mine.
def select_difficulty():
    possible_answers = ["e", "m", "h", "c"]
    selection = input("""
    DIFFICULY SELECTIONS
    ┌ - - - - - - - - - - - - - - - - - - - - ┐
    | Options: Easy, Medium, Hard, and Custom |
    └ - - - - - - - - - - - - - - - - - - - - ┘
""") + " "
    while selection[0] not in possible_answers:
        print("Sorry, but that's not a valid difficulty. Please select again. \n")
        selection = input("""
    DIFFICULY SELECTIONS
    ┌ - - - - - - - - - - - - - - - - - - - - ┐
    | Options: Easy, Medium, Hard, and Custom |
    └ - - - - - - - - - - - - - - - - - - - - ┘
""") + " "
    selection = selection.lower()

    #Translate the selection to a possible outcome. This also includes quick selecting based on first letter.
    if selection[0] == "e":
        select = "easy"
    elif selection[0] == "m":
            select = "medium"
    elif selection[0] == "h":
            select = "hard"
    else:
        Game.difficulties["customs"][3] += 1
        input_rows = int(input("How many rows? "))
        input_cols = int(input("How many columns? "))
        input_mines = int(input("How many mines? "))
        while (input_rows * input_cols) <= input_mines:
            print("It seems you've entered too many mines. Please try again.")
            input_rows = int(input("How many rows? "))
            input_cols = int(input("How many columns? "))
            input_mines = int(input("How many mines? "))
        return [input_rows, input_cols, input_mines]
    
    Game.difficulties[select][3] += 1
    return Game.difficulties[select]

    # The magic of custom games starts here. Input runs until the correct number has been added.
    
#This checks that the selection is an integer.
def check_select(selection, count):
    try:
        int(selection)
    except:
        print("\nPlease use an integer between 0 and " + str(count))
        return False
    else:
        return True
# Mine check looks to see if a mine exists at the locaiton indicated. Returns a boolean.
def mine_check(mine_list, check_row, check_col, check_start = True):
    for mine in mine_list:
        if check_start == False and mine['num'] == 0:
            pass
        elif check_row == mine['row'] and check_col == mine['col']:
            return True
    return False

# The magical gameboard text generator creates a gameboard. Creates a key for each row and column at the top and the left to help players navigate the board. Gathers what the cell is currently supposed to be displaying as well. Also creates square boxes using text around each of the cells. Board should correctly display for all sizes up to 99.
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
                    text += gamelist[-1].gameboard[true_row][true_col].name
    text += "\nThere are {mines} remaining.".format(mines=len(gamelist[-1].game_mines) - Field.total_flags)
    print(text)
    return text

# Magical bit of code that splits apart a player's selection for the faster selection bit.
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

# goes through the action list and sees if the action already exists.
def check_actions(check_row, check_col):
    for item in gamelist[-1].action_list:
        if item[0] == check_row and item[1] == check_col:
            return False
    return True

def play_again():
    again = input("""
    PLAY AGAIN??
    ┌ - - - - - - - - - - - - - - ┐
    | Options: Yes, No (and Quit) |
    └ - - - - - - - - - - - - - - ┘\n""")
    again = again.lower()
    if "y" in again[0]:
        gamelist.append(Game())
        gamelist[-1].start_game()
    else:
        exit()

# Gameplay -- -- -- --
# I'm really sad to say that this is so far all I've generated for the gameplay tab. Looking at adding the "Game" class which should be able to keep track of games, scores, and start new ones. Also hoping to integrate a bit of a text file to add saves for statistics.
print('\n\nWelcome to...' + title)
time.sleep(1)

gamelist = [Game()]
gamelist[0].start_game()