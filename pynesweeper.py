"""
Python textline Minesweeper clone
Python 3.5
Tyler Hall 2016
Minesweeper is property of Microsoft
"""

import random


def how_to_play():
    print("Pynesweeper is a game of clearing a field of mines. The three difficulties vary on size of the field and " +
          "number of mines,\nbut the rules stay the same. Once you've selected a difficulty and the game starts, " +
          "you can dig up a location, mark it\nwith a flag, or reveal nearby mines once enough flags have been " +
          "placed. Once a spot is dug up, a number will indicate how\nmany mines are next to the spot, with a " +
          "maximum of 8. But watch out! If you dig up a mine, it will be game over, and you'll\nhave to start from " +
          "scratch. Good luck and have fun!\n")
    return


def arrange_xy(old_coords):  # Arranges a list oc (x, y) coordinates into a new list by the x-value first
    new_coords = []
    for i in range(map_size_x):
        for j in range(map_size_y):
            if old_coords.count([i, j]) > 0:
                old_coords.remove([i, j])
                new_coords.append([i, j])
    return new_coords


def win_screen():  # Announces the player's success, and offer to restart
    print_end_map()
    print("You Win!")
    print()
    print("Would you like to play again?")
    menu()
    map_gen()
    return


def lose_screen():  # Announces the player's failure, and offer to restart
    print_end_map()
    print("You Lose!")
    print()
    print("Would you like to play again?")
    menu()
    map_gen()
    return


def mark(x, y):  # Places a flag 'P' at an x, y coordinate
    global rev_map_array
    if rev_map_array[y][x] == chr(1160):
        rev_map_array[y][x] = "P"
    elif rev_map_array[y][x] == "P":
        rev_map_array[y][x] = chr(1160)
    else:
        print("Invalid option, location revealed")


def dig(x, y):  # Reveals an x, y location. If a mine, triggers the lose screen, if no nearby mines, clears an area
    global hidden_map_array
    global rev_map_array
    global map_size_x
    global map_size_y
    global mine_array
    global map_array
    if y < 0 or y >= map_size_y or x < 0 or x >= map_size_x:  # Does nothing if out of range for the map
        return
    elif rev_map_array[y][x] != chr(1160):  # Does nothing if coordinate has been revealed
        return
    else:
        rev_map_array[y][x] = hidden_map_array[y][x]
        if hidden_map_array[y][x] == 'X':  # Lose condition
            print_map()
            print("Boom!")
            lose_screen()
            return
        map_array.remove([x, y])
        if hidden_map_array[y][x] == 0:  # Reveals an area if no mines as neighbors
            for i in range(-1, 2):
                for j in range(-1, 2):
                    dig(x + i, y + j)


def reveal(x, y):
    global reveal_array
    print("placeholder " + str(x) + ' ' + str(y))
    if rev_map_array[y][x] == 0:  # Does nothing if coordinate has been revealed
        print("No neighboring mines")
        return
    elif rev_map_array[y][x] == chr(1160):  # Does nothing if coordinate has been revealed
        print("Location not dug up")
        return
    else:
        mines = rev_map_array[y][x]
        print(mines)
        if neighbor_mines(mines, x, y):
            for each in range(len(reveal_array)):
                i = reveal_array[each][0]  #x
                j = reveal_array[each][1]  #y
                print(str(i) + " " + str(j))
                dig(i, j)
                #rev_map_array[j][i] = hidden_map_array[j][i]
                #map_array.remove([i, j])
    return


def x_check(check_num):  # Checks if a x-value is within the map
    global x_range
    for i in range(len(x_range)):
        if x_range[i] == check_num:
            return True
    return False


def y_check(check_num):  # Checks if a y-value is within the map
    global y_range
    for i in range(len(y_range)):
        if y_range[i] == check_num:
            return True
    return False


def neighbor_mines(mines, x, y):
    global reveal_array
    reveal_array.clear()
    print("Neighbor to check " + str(mines))
    mine_count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if y < 0 or y >= map_size_y or x < 0 or x >= map_size_x:
                pass
            elif rev_map_array[y + j][x + i] == 'P':
                mine_count += 1
            else:
                if rev_map_array[y + j][x + i] == chr(1160):
                    reveal_array.append([x + i, y + j])
    if mine_count == rev_map_array[y][x]:
        return True
    else:
        return False


def player_turn():  # Main gameplay loop.
    # print("There's gonna be a loop here")
    playing = True
    while playing:
        print_map()
        if map_array == mine_array:  # Checks for win conditions
            # playing = False
            win_screen()
        else:  # Takes user input if not win
            usr_input = input("Actions: 'Dig x y' 'Mark x y' 'Reveal x y' and 'Quit'\n")
            usr_command = [0, 0, 0]
            for i in range(len(usr_input.split())):  # Parses input to up to three objects
                usr_command[i] = usr_input.split()[i]
            if usr_command[0].casefold() == "quit":  # Exits the game
                print("Quitting game")
                break
            elif (usr_command[0].casefold() == "dig") and (x_check(usr_command[1])) and (y_check(usr_command[2])):
                # print("dug", usr_command[1], usr_command[2])
                if rev_map_array[int(usr_command[2]) - 1][int(usr_command[1]) - 1] != chr(1160):
                    print("Invalid option, location revealed")
                else:
                    dig(int(usr_command[1]) - 1, int(usr_command[2]) - 1)
            elif (usr_command[0].casefold() == "mark") and (x_check(usr_command[1])) and (y_check(usr_command[2])):
                # print("mork", usr_command[1], usr_command[2])
                mark(int(usr_command[1]) - 1, int(usr_command[2]) - 1)
            elif (usr_command[0].casefold() == "reveal") and (x_check(usr_command[1])) and (y_check(usr_command[2])):
                reveal(int(usr_command[1]) - 1, int(usr_command[2]) - 1)
            else:
                print("Invalid option")


def print_map2():   # Prints out the hidden mine map hidden_map_array; not used in final version
    for y in range(len(hidden_map_array)):
        for x in range(len(hidden_map_array[y])):
            print(hidden_map_array[y][x], " ", sep='', end='')
        print()
    print(chr(166))


def print_map3():  # prints out the base rev_map_array without the extra borders; not used in final version
    for y in range(len(rev_map_array)):
        for x in range(len(rev_map_array[y])):
            print(rev_map_array[y][x], " ", sep='', end='')
        print()
    print(chr(166))


def print_end_map():    # So this one will display the map with borders as the player will actually be shown
    disp_map_array.clear()
    first_line = [' ', ' ', 'X']
    second_line = [' ', ' ', ' ']
    third_line = ['Y', ' ', '+']
    for x in range(map_size_x):
        if x < 9:
            first_digit = " "
        elif x < 19:
            first_digit = 1
        elif x < 29:
            first_digit = 2
        else:
            first_digit = 3
        first_line.append(' ')
        first_line.append(str(first_digit))
        second_line.append(' ')
        second_line.append(str((x + 1) % 10))
        third_line.append('-')
        third_line.append('-')
    # print(first_line)
    # print(second_line)
    # print(third_line)
    disp_map_array.append(first_line)
    disp_map_array.append(second_line)
    disp_map_array.append(third_line)
    for y in range(map_size_y):  # Starts feeding in map data, readying it for display to the user
        this_line = []
        if y < 9:
            first_digit = " "
        else:
            first_digit = 1
        this_line.append(str(first_digit))
        this_line.append(str((y + 1) % 10))
        this_line.append(chr(166))
        for x in range(map_size_x):
            this_line.append(' ')
            this_line.append(str(hidden_map_array[y][x]))
        # print(this_line)
        disp_map_array.append(this_line)
    # for x in range(len(hidden_map_array[y])):  # wtf was I doing here
    #     print  # mang idfk
    for y in range(len(disp_map_array)):  # Prints out the map
        for x in range(len(disp_map_array[y])):
            print(disp_map_array[y][x], sep='', end='')
        print()


def print_map():    # So this one will display the map with borders as the player will actually be shown
    disp_map_array.clear()
    first_line = [' ', ' ', 'X']
    second_line = [' ', ' ', ' ']
    third_line = ['Y', ' ', '+']
    for x in range(map_size_x):
        if x < 9:
            first_digit = " "
        elif x < 19:
            first_digit = 1
        elif x < 29:
            first_digit = 2
        else:
            first_digit = 3
        first_line.append(' ')
        first_line.append(str(first_digit))
        second_line.append(' ')
        second_line.append(str((x + 1) % 10))
        third_line.append('-')
        third_line.append('-')
    # print(first_line)
    # print(second_line)
    # print(third_line)
    disp_map_array.append(first_line)
    disp_map_array.append(second_line)
    disp_map_array.append(third_line)
    for y in range(map_size_y):  # Starts feeding in map data, readying it for display to the user
        this_line = []
        if y < 9:
            first_digit = " "
        else:
            first_digit = 1
        this_line.append(str(first_digit))
        this_line.append(str((y + 1) % 10))
        this_line.append(chr(166))
        for x in range(map_size_x):
            this_line.append(' ')
            this_line.append(str(rev_map_array[y][x]))
        # print(this_line)
        disp_map_array.append(this_line)
    # for x in range(len(hidden_map_array[y])):  # wtf was I doing here
    #     print  # mang idfk
    for y in range(len(disp_map_array)):  # Prints out the map
        for x in range(len(disp_map_array[y])):
            print(disp_map_array[y][x], sep='', end='')
        print()


def map_gen():  # Generates the hidden and revealed maps, builds up the arrays used for checking win condition
    global hidden_map_array
    global rev_map_array
    global x_range
    global y_range
    global map_size_x
    global map_size_y
    global mine_array
    global map_array
    global reveal_array

    mine_array.clear()
    map_array.clear()
    reveal_array.clear()
    print("Generating map")
    hidden_map_array = [[0 for i in range(map_size_x)] for i in range(map_size_y)]
    rev_map_array = [[0 for i in range(map_size_x)] for i in range(map_size_y)]
    x_range = [str(i + 1) for i in range(map_size_x)]
    y_range = [str(i + 1) for i in range(map_size_y)]
    # print("Empty map")
    # print_map2()
    for i in range(mine_num):  # Propagates mines in the map
        rand_x = random.randrange(map_size_x)
        rand_y = random.randrange(map_size_y)
        # print(rand_x, " ", rand_y)
        placing_mine = True
        while placing_mine:
            if hidden_map_array[rand_y][rand_x] == 0:
                hidden_map_array[rand_y][rand_x] = "X"
                mine_loc = [rand_x, rand_y]
                mine_array.append(mine_loc)
                # print(i)
                placing_mine = False
            else:
                rand_x = random.randrange(map_size_x)
                rand_y = random.randrange(map_size_y)
                # print(rand_x, " ", rand_y)
    # print("Mined map")
    # print_map2()
    for y in range(len(hidden_map_array)):  # Counts nearby mines at each location and fills in that data
        # print("y loop", y)
        for x in range(len(hidden_map_array[y])):
            map_array.append([x, y])
            # print("x loop", x)
            if hidden_map_array[y][x] == 0:
                nearby_count = 0
                # print(y, x)
                ty = y
                tx = x
                for iy in range(ty-1, ty+2):
                    for ix in range(tx-1, tx+2):
                        # print("i", iy, ix, end=' ')
                        if not (iy < 0 or iy >= map_size_y or ix < 0 or ix >= map_size_x):
                            # print("in range", end=' ')
                            if hidden_map_array[iy][ix] == "X":
                                # print("X", end=' ')
                                nearby_count += 1
                        # print()
                hidden_map_array[y][x] = nearby_count
            rev_map_array[y][x] = chr(1160)
    # print("Mined and numbered map")
    # print_map2()
    # print("Mines")
    # print(mine_array)
    # hidden_map_array.sort()
    mine_array = arrange_xy(mine_array)
    # print(mine_array)
    # print(map_array)
    map_array = arrange_xy(map_array)
    # print(map_array)


def menu():  # Menu loop, takes user inupt and either exits program or starts generating the play map
    global map_size_x
    global map_size_y
    global mine_num
    in_menu = True
    while in_menu:
        usr_command = input("'New' game to start, 'Info' for game rules, or 'Quit' to exit\n")
        if usr_command.casefold() == "new":
            print("New game")
            diff_selection = True
            while diff_selection:
                print("'Easy'   9x9     10 mines\n" +
                      "'Medium' 16x16   40 mines\n" +
                      "'Hard'   16x30   99 mines")
                usr_command = input("Select your difficulty\n")
                if usr_command.casefold() == "easy":
                    map_size_x = 9
                    map_size_y = 9
                    mine_num = 10
                    diff_selection = False
                    in_menu = False
                    #map_gen()
                elif usr_command.casefold() == "medium":
                    map_size_x = 16
                    map_size_y = 16
                    mine_num = 40
                    diff_selection = False
                    in_menu = False
                    #map_gen()
                elif usr_command.casefold() == "hard":
                    map_size_x = 30
                    map_size_y = 16
                    mine_num = 99
                    diff_selection = False
                    in_menu = False
                    #map_gen()
                elif usr_command.casefold() == "quit":
                    print("Quit game")
                    exit(0)
                else:
                    print("Invalid option")
        elif usr_command.casefold() == "info":
            how_to_play()
        elif usr_command.casefold() == "quit":
            print("Quit game")
            exit(0)
        else:
            print("Invalid option")


if __name__ == "__main__":  # Main method. Sets up global objects, displays title, and calls the menu and game loops
    map_size_x = 0
    map_size_y = 0
    mine_num = 0
    hidden_map_array = [[]]
    rev_map_array = [[]]
    disp_map_array = [[]]
    x_range = []
    y_range = []
    mine_array = []
    map_array = []
    reveal_array = []

    print("Pynesweeper\n" +
          "Accepted commands are in single quotes, and separate X and Y with spaces\n" +
          "Enter your choices")
    menu()
    map_gen()

    # print("Mined and numbered map")
    # print_map2()
    # print("Revealed map")
    # print_map3()
    # print("In-game map")
    # print_map()

    player_turn()
