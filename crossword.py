###########################################################
#  Crossword Puzzle Loader and Solver
#
#  Algorithm
#    define Crossword and Clue classes
#    load crossword puzzle from a CSV file using Crossword class
#    initialize puzzle board and clues within Crossword class constructor
#    parse clues and answers from CSV, creating Clue objects
#    update puzzle board with placeholders for answers
#    define methods for changing guesses, revealing answers,
#    finding incorrect letters, and checking if the puzzle is solved
#    include string representations for easy debugging and visualization
#    allow for interaction with the puzzle through guess updates and reveals
#    determine when the puzzle is correctly solved
#  designed to provide a structured approach to crossword puzzle solving
###########################################################

import csv

CROSSWORD_DIMENSION = 5

GUESS_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"


class Clue:
    def __init__(self, indices, down_across, answer, clue):
        """
        Puzzle clue constructor
        :param indices: row,column indices of the first letter of the answer
        :param down_across: A for across, D for down
        :param answer: The answer to the clue
        :param clue: The clue description
        """
        self.indices = indices
        self.down_across = down_across
        self.answer = answer
        self.clue = clue

    def __str__(self):
        """
        Return a representation of the clue (does not include the answer)
        :return: String representation of the clue
        """
        return f"{self.indices} {'Across' if self.down_across == 'A' else 'Down'}: {self.clue}"

    def __repr__(self):
        """
        Return a representation of the clue including the answer
        :return: String representation of the clue
        """
        return str(self) + f" --- {self.answer}"

    def __lt__(self, other):
        """
        Returns true if self should come before other in order. Across clues come first,
        and within each group clues are sorted by row index then column index
        :param other: Clue object being compared to self
        :return: True if self comes before other, False otherwise
        """
        return ((self.down_across,) + self.indices) < ((other.down_across,) + other.indices)


class Crossword:
    def __init__(self, filename):
        """
        Crossword constructor
        :param filename: Name of the csv file to load from. If a file with
        this name cannot be found, a FileNotFoundError will be raised
        """
        self.clues = dict()
        self.board = [['■' for _ in range(CROSSWORD_DIMENSION)] for __ in range(CROSSWORD_DIMENSION)]
        self._load(filename)

    def _load(self, filename):
        """
        Load a crossword puzzle from a csv file
        :param filename: Name of the csv file to load from
        """
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                indices = tuple(map(int, (row['Row Index'], row['Column Index'])))
                down_across, answer = row['Down/Across'], row['Answer']
                clue_description = row['Clue']
                clue = Clue(indices, down_across, answer, clue_description)

                key = indices + (down_across,)
                self.clues[key] = clue

                i = 0
                while i < len(answer):
                    if down_across == 'A':
                        self.board[indices[0]][indices[1] + i] = '_'
                    else:
                        self.board[indices[0] + i][indices[1]] = '_'
                    i += 1

    def __str__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        board_str = '     ' + '    '.join([str(i) for i in range(CROSSWORD_DIMENSION)])
        board_str += "\n  |" + "-" * (6 * CROSSWORD_DIMENSION - 3) + '\n'
        for i in range(CROSSWORD_DIMENSION):
            board_str += f"{i} |"
            for j in range(CROSSWORD_DIMENSION):
                board_str += f"  {self.board[i][j]}  "
            board_str += '\n'

        return board_str

    def __repr__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        return str(self)

    def change_guess(self, clue, new_guess):  # fill out the parameters
        """
        Function to change the guess for a clue, updating the board with the new guess
        :param clue:
        :param new_guess:
        :return:
        """
        for char in new_guess:
            if char not in GUESS_CHARS:  # check if the character is valid
                print("Guess contains invalid characters.\n")

        if len(new_guess) != len(clue.answer):  # check if the guess length matches the length of the clue
            raise RuntimeError("Guess length does not match the length of the clue.\n")
        row_index, col_index = clue.indices
        for i,char in enumerate(new_guess):  # loop through the characters in the new guess
            if clue.down_across == 'A':
                self.board[row_index][col_index + i] = char
            elif clue.down_across == 'D':
                self.board[row_index + i][col_index] = char

    def reveal_answer(self, clue):
        """
        Function to reveal the answer for a clue, updating the board with the correct answer
        :param clue:
        :return: None
        """
        row_index, col_index = clue.indices  # get the row and column indices of the clue
        for i, char in enumerate(clue.answer):
            if clue.down_across == 'A':  # check if the clue is across
                self.board[row_index][col_index + i] = char
            elif clue.down_across == 'D':  # check if the clue is down
                self.board[row_index + i][col_index] = char

    def find_wrong_letter(self, clue):
        """
        Function to find the first wrong letter in a clue
        :param clue:
        :return: The index of the first wrong letter in the clue, or -1 if the input is correct
        """
        row_index, col_index = clue.indices  # get the row and column indices of the clue
        if clue.down_across == 'A':
            for i, char in enumerate(clue.answer):  # loop through the characters in the answer to check if they match the board
                if self.board[row_index][col_index + i] != char:  # check if the character in the board matches the character in the answer
                    return i
        elif clue.down_across == 'D':
            for i, char in enumerate(clue.answer):  # loop through the characters in the answer to check if they match the board
                if self.board[row_index + i][col_index] != char:
                    return i
        return -1 # return -1 if the clue is correct

    def is_solved(self):  # fill out the parameters
        """
        Function to check if the crossword puzzle is solved
        :param: None
        :return: True if the puzzle is solved, False otherwise
        """
        for key in self.clues:
            clue = self.clues[key]
            row_index, col_index = clue.indices  # get the row and column indices of the clue
            for i, char in enumerate(clue.answer):  # loop through the characters in the answer to check if they match the board
                if clue.down_across == 'A':  # check if the clue is across
                    if self.board[row_index][col_index + i] != char: # check if the character in the board matches the character in the answer
                        return False
                elif clue.down_across == 'D': # check if the character in the board matches the character in the answer
                    if self.board[row_index + i][col_index] != char:
                        return False
        return True
