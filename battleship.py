#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""This is a version of the Battleship-boardgame.
Everything is included in this file, so no other files are needed for playing.
This file follows the Python PEP8 style guidelines."""

import os

__author__ = "Timo Särkkä"
__copyright__ = "Copyright 2016"

'''Here are the constants for the battleship.py'''
# The game title is drawn here and used in the game. Picture from chris.com and
# text from patorjk.com
TITLEPICTURE = r"""
                       __/___
                 _____/______|
         _______/_____\_______\_____
         \              < < <       |
       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ____        __  __  __          __    _
   / __ )____ _/ /_/ /_/ /__  _____/ /_  (_)___
  / __  / __ `/ __/ __/ / _ \/ ___/ __ \/ / __ \
 / /_/ / /_/ / /_/ /_/ /  __(__  ) / / / / /_/ /
/_____/\__,_/\__/\__/_/\___/____/_/ /_/_/ .___/
                                       /_/"""

# Game board size is an array the size of BOARD_SIZE x BOARD_SIZE
BOARD_SIZE = 10


# Game markers used to display various states on the gameboard
VERTICAL_SHIP = '|'
HORIZONTAL_SHIP = '-'
EMPTY = 'O'
MISS = '.'
HIT = '*'
SUNK = '#'

# A list of tuples containing info about ship names and sizes
SHIP_INFO = [
    ("Aircraft Carrier", 5),
    ("Battleship", 4),
    ("Submarine", 3),
    ("Cruiser", 3),
    ("Patrol Boat", 2)
]

# Creates an alphabet row for the game board using a list comprehension
BOARD_ALPHABETS = ("   " + " ".join([chr(i) for i in range(ord('A'),
                   ord('A') + BOARD_SIZE)]))


# Here begin the auxiliary functions for battleship.py'''
def empty_scr():
    '''Empties the screen when applicable'''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def title():
    '''Displays the game logo and title when applicable'''
    print(TITLEPICTURE)


def generate_coordinates(row_no, column_no):
    '''Turns numeric array values into gameboard coordinates
    e.g. [4, 0] -> A5'''
    return chr(ord('A') + column_no) + str(row_no + 1)


def generate_numeric(coordinates):
    '''Turns gameboard coordinates intos numeric values
    e.g. A5 -> [4, 0]'''
    column_no = ord(coordinates[0]) - ord('A')
    row_no = int(coordinates[1:]) - 1
    return (row_no, column_no)


def help():
    '''Print help for the player, explaining the symbols'''
    print("\nGAME SYMBOLS:\n"
          "Ships vertical {} or horizontal {}\n"
          "Empty {}\n"
          "Miss {}\n"
          "Hit {}\n"
          "Sunk {}\n"
          "".format(VERTICAL_SHIP, HORIZONTAL_SHIP, EMPTY, MISS, HIT, SUNK))


# Here begin the actual functions used by the game'''
def names():
    """Ask for player's name"""
    player_name = None
    while player_name == None or player_name == '':
        player_name = input("Please, enter the name of a player: ")
        if not player_name:
            print("You have to enter something!")
    return player_name


def print_board(player_name, player_view):
    '''Print the player gameboard'''
    print("   {}".format(player_name + "'s gameboard:\n"))
    for player_line in player_view:
        print("{}".format(player_line))


def print_boards_in_game(other_player_name,
                         player_name,
                         other_player_view,
                         player_view):
    '''Print both player boards'''
    print("         {:22}        {:22} \n".format(
        other_player_name + "'s board:", player_name + "'s board:"))
    for other_player, player in zip(other_player_view, player_view):
        print("   {:22}        {:22}".format(other_player, player))


def check_if_valid(coordinates, boardsize=BOARD_SIZE):
    '''Check if given coordinate is in the right form (length, form) and that
    player tries to input a coordinate that is actually on gameboard'''
    if len(coordinates) < 2:
        return False
    try:
        column = ord(coordinates[0].upper())
        row = int(coordinates[1:])
    except (TypeError, ValueError):
        return False
    return (column >= ord('A') and column <= ord('A') + boardsize - 1 and
            row >= 1 and row <= boardsize)


def calculate_start_location(starting_point, size, direction):
    '''Calculate where the ship is based on given user input. The ship
    starts from the starting point and runs up for vertical and right for
    horizontal choice. This function also checks if ship is actually on the
    game board, otherwise displays an error message.'''
    s_col = ord(starting_point[0].upper())
    s_row = int(starting_point[1:])

    if direction[0].lower() == 'v':
        array_values = [chr(s_col) + str(row)
                        for row in range(s_row, s_row + size)]
    else:
        array_values = [chr(col) + str(s_row)
                        for col in range(s_col, s_col + size)]
    if check_if_valid(array_values[0]) and check_if_valid(array_values[-1]):
        return array_values
    else:
        return []


def calc_starting_point():
    '''Asks the user to give the starting point for the ship.'''
    while True:
        point_input = input("\nGive the starting point for the vessel (e.g. "
                            "'A5' or 'D7').\nThe vessel will run down if "
                            "vertical and right if horizontal: ").strip()
        starting_point = point_input.upper()
        if check_if_valid(starting_point):
            return starting_point
        else:
            print("Sorry, this point {} is not on the board. "
                  "Please enter in form e.g. 'A5'".format(starting_point))


def guess(player):
    '''Ask for a player guess'''
    while True:
        guess_input = input("Enter {}'s guess (e.g. 'A5' or 'D7') or "
                            "'HELP' to display clarification\n"
                            "for symbols:\n".format(player.name).strip())
        guess = guess_input.upper()
        if guess in player.guesses:
            print("That point was {} already tried before! Please,"
                  "try again.\n".format(guess))
            continue
        if check_if_valid(guess):
            return guess
        if guess == 'HELP':
            help()
            continue
        else:
            print("Sorry, that point is not on the board. "
                  "Please enter in form 'A5' for example.\n")


def get_direction():
    '''Ask whether to place the vessel vertically or horizontally'''
    while True:
        direction = input("Indicate the ship's direction, "
                          "[V]ertical or [H]orizontal: ").strip()
        if not direction:
            print("Please type only 'V' or 'H' for selecting the direction.")
            continue
        direction = direction[0].lower()
        if direction == 'v' or direction == 'h':
            return direction
        else:
            print("Please type only 'V' or 'H' for selecting the direction.")


def place_ships(player):
    '''Add each player's ships to their respective gameboards.'''
    # Go through every ship on the ship list
    for ship in SHIP_INFO:
        ship_name = ship[0]
        ship_size = ship[1]
        empty_scr()
        title()
        # Adding ships to this player
        print("Adding ships for {}:\n".format(player.name))
        print_board(player.name, player.board.see_player_board())
        print("Adding the following vessel: {},"
              "(size:{})\n".format(ship_name, ship_size))
        # Loops through the sequence of getting the direction
        # and starting point and calculating the location from these
        while True:
            direction = get_direction()
            starting_point = calc_starting_point()
            array_values = calculate_start_location(starting_point,
                                                    ship_size,
                                                    direction)
            # Possible error messages
            if not array_values:
                print("You tried to place the vessel fully or "
                      "partly outside the gameboard. Try again!\n")
                continue
            if not player.board.check_if_empty(array_values):
                print("You tried to place the vessel on top of "
                      "another one. Try again!\n")
                continue
            break
        # Creates a ship instance based on the info given
        ship = Ship(ship_name, ship_size, array_values, direction)
        # Adds ship to a player list
        player.add_ship(ship)
        # Places the ship on the gameboard
        player.board.put_ship_on_board(ship)
    empty_scr()
    title()
    # Prints the game board for info
    print("Adding ships for {}:\n".format(player.name))
    print_board(player.name, player.board.see_player_board())
    input("{}, you're all set! Press ENTER to continue. "
          "".format(player.name))
    empty_scr()


def play_turn(player, opponent):
    '''Play one turn at a time'''
    # First, empty the screen and display the title
    empty_scr()
    title()
    # Let the player know about their turn
    input("{}, you're up. Press ENTER to continue.".format(player.name))
    # Empty screen once more and display the title
    empty_scr()
    title()
    # Display the boards
    print("{}, you're up.\n".format(player.name))
    opp_view = opponent.board.see_opponent_board()
    player_view = player.board.see_player_board()
    print_boards_in_game(opponent.name, player.name, opp_view, player_view)
    # Get a guess from the player
    coordinates = guess(player)
    player.guesses.append(coordinates)
    # Append the game view with the given guess
    response = opponent.board.guess(coordinates)
    opp_view = opponent.board.see_opponent_board()
    # Empty screen and display the title
    empty_scr()
    title()
    # The other player's turn
    print("{}, you're up.\n".format(player.name))
    print_boards_in_game(opponent.name, player.name, opp_view, player_view)
    print(response)
    # And round it goes again
    input("Press ENTER to clear the screen and "
          "give the turn to the other player.")
    empty_scr()


class Board():

    def __init__(self, size=BOARD_SIZE):
        '''Gameboard initializations'''
        self.boardsize = size
        self.boardgrid = []
        for row in range(self.boardsize):
            new_row = []
            for column in range(self.boardsize):
                new_row.append(Location(generate_coordinates(row, column)))
            self.boardgrid.append(new_row)

    def see_player_board(self):
        '''Display the player's own view of his/her vessels'''
        display = [BOARD_ALPHABETS]
        row_num = 1
        for row in self.boardgrid:
            display.append(str(row_num).rjust(2) + " " + " ".join(
                [location.player_view() for location in row]))
            row_num += 1
        display.append("")
        return display

    def see_opponent_board(self):
        '''See the view of the other board without displaying ships'''
        display = [BOARD_ALPHABETS]
        row_num = 1
        for row in self.boardgrid:
            display.append(str(row_num).rjust(2) + " " + " ".join(
                [location.opponent_view() for location in row]))
            row_num += 1
        display.append("")
        return display

    def check_if_empty(self, coordinates):
        '''Check if the board is truly empty'''
        result = True
        for value in coordinates:
            row, column = generate_numeric(value)
            if self.boardgrid[row][column].ship:
                result = False
        return result

    def put_ship_on_board(self, ship):
        '''Put the vessel on the gameboard'''
        for value in ship.coordinates:
            row, column = generate_numeric(value)
            self.boardgrid[row][column].ship = ship

    def guess(self, coordinates):
        '''Apply guess to board'''
        row, column = generate_numeric(coordinates)
        result = self.boardgrid[row][column].guess()
        if result == MISS:
            status = "The guess was [{}]: That's a miss!\n".format(coordinates)
        elif result == HIT:
            status = "The guess was [{}]: That's a hit!\n".format(coordinates)
        elif result == SUNK:
            status = "The guess was [{}]: You sunk the {}!\n".format(
                coordinates, self.boardgrid[row][column].ship.name)
        return status


class Location():
    '''An auxiliary class to help get the status of the gameboard and ships'''
    def __init__(self, coordinates):
        '''Initializing everything'''
        self.coordinates = coordinates
        self.ship = None
        self.state = EMPTY

    def player_view(self):
        '''Return player view'''
        if self.ship:
            return self.ship.player_status(self.coordinates)
        else:
            return self.state

    def opponent_view(self):
        '''Return opponent view'''
        if self.ship:
            return self.ship.opponent_status(self.coordinates)
        else:
            return self.state

    def guess(self):
        '''Apply a guess here'''
        if not self.ship:
            self.state = MISS
        else:
            self.state = self.ship.hit(self.coordinates)
        return self.state


class Player():
    '''Player-class with name and ship info'''

    def __init__(self, name):
        '''Define player's name, board, ships, guesses'''
        self.name = name
        self.board = Board()
        self.ships = []
        self.guesses = []

    def add_ship(self, ship):
        '''Add a ship to player's list'''
        self.ships.append(ship)

    def ships_left(self):
        '''Search for ships that are still in the game'''
        found = False
        for ship in self.ships:
            if not ship.sunk:
                found = True
        return found


class Ship():
    '''Ship-class with following info: name, size, coordinates, and hits'''

    def __init__(self, name, size, coordinates, direction):
        '''Initializations'''
        self.name = name
        self.size = size
        self.coordinates = coordinates
        self.direction = direction
        self.hits = []
        self.sunk = False

        # Depending on the direction, either show | or - as the ship symbol
        if direction.lower() == 'v':
            self.symbol = VERTICAL_SHIP
        else:
            self.symbol = HORIZONTAL_SHIP

    def player_status(self, coordinates):
        '''Return SUNK, HIT, or the appropriate symbol'''
        # Controls how the symbols are displayed for the player board
        if self.sunk:
            return SUNK
        elif coordinates in self.hits:
            return HIT
        else:
            return self.symbol

    def opponent_status(self, coordinates):
        '''Return SUNK, HIT, or EMPTY (no location revealed)'''
        # Controls how the symbols are displayed for the opponent board
        if self.sunk:
            return SUNK
        elif coordinates in self.hits:
            return HIT
        else:
            return EMPTY

    def hit(self, coordinates):
        '''Hit this location'''
        # Check if coordinate given is a ship coordinate
        if coordinates.upper() in self.coordinates:
            # If yes, append the hit list
            self.hits.append(coordinates)
            # Further, if the length of hits list is the length of the ship,
            # the ship is sunk
            if len(self.hits) == self.size:
                self.sunk = True
                self.symbol = SUNK
                return SUNK
            # Otherwise, just return the hit
            else:
                return HIT


def main():
    '''The actual game function'''

    # First, screen is emptied and title is shown
    empty_scr()
    title()
    # A one-time welcome message
    print("Welcome to play the Battleship-game version 0.1!\n")
    # Names are asked
    name1 = names()
    name2 = names()
    # Player-classes initialized
    player1 = Player(name1)
    player2 = Player(name2)
    # Start of adding ships
    input("\nTime to place the vessels on board. "
          "{} goes first. {}, look away for a moment.\n\n"
          "Press ENTER to continue.".format(name1, name2))
    empty_scr()
    # Place ships for the first player
    place_ships(player1)
    title()
    input("{}, time to add your ships. Press ENTER to continue. ".format(name2))
    # Place ships for the second player
    place_ships(player2)
    title()
    input("Let's play! {}, you go first. Press ENTER to continue. ".format(name1))

    '''The actual game loop, where turns are taken until all of the ships of
    one player are out of the game.'''
    while True:
        play_turn(player1, player2)
        if not player2.ships_left():
            title()
            input("{}, you win the game! Press ENTER to see the "
                  "status of the boards.\n".format(player1.name))
            break
        play_turn(player2, player1)
        if not player1.ships_left():
            title()
            input("{}, you win the game! Press ENTER to see the "
                  "status of the boards.\n".format(player2.name))
            break

    # Print the final status of the boards before ending the game
    print_boards_in_game(player1.name, player2.name,
                         player1.board.see_player_board(),
                         player2.board.see_player_board())


'''This makes sure that the game is run as main and if there's keyboard
termination, the exit is done properly.'''
if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nBattleship is terminating. Thanks for playing!")
