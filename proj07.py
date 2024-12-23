###########################################################
#  Crossword Puzzle Game
#
#  Algorithm
#    display initial help menu with game options
#    prompt for crossword puzzle filename
#    load crossword puzzle from file
#    loop to accept and process game commands
#       - display clues (C)
#       - make a guess for a clue (G)
#       - reveal the answer for a clue (R)
#       - give a hint for a clue (T)
#       - display help menu (H)
#       - restart the game with a new puzzle (S)
#       - quit the game (Q)
#    process user inputs and update game state accordingly
#    display clues, crossword state, or hints based on user actions
#    validate user inputs and provide feedback
#    check for puzzle completion and congratulate if solved
#    loop until the user decides to quit
#  display closing message upon quitting
###########################################################

from crossword import Crossword
from crossword import Clue
import sys

HELP_MENU = "\nCrossword Puzzler -- Press H at any time to bring up this menu" \
            "\nC n - Display n of the current puzzle's down and across clues" \
            "\nG i j A/D - Make a guess for the clue starting at row i, column j" \
            "\nR i j A/D - Reveal the answer for the clue starting at row i, column j" \
            "\nT i j A/D - Gives a hint (first wrong letter) for the clue starting at row i, column j" \
            "\nH - Display the menu" \
            "\nS - Restart the game" \
            "\nQ - Quit the program"

OPTION_PROMPT = "\nEnter option: "
PUZZLE_PROMPT = "Enter the filename of the puzzle you want to play: "
PUZZLE_FILE_ERROR = "No puzzle found with that filename. Try Again.\n"
"\nAcross"
"\nDown"
"\nPuzzle solved! Congratulations!"
"Letter {} is wrong, it should be {}"
"Invalid option/arguments. Type 'H' for help."
"Enter your guess (use _ for blanks): "
"This clue is already correct!"

RuntimeError("Guess length does not match the length of the clue.\n")
RuntimeError("Guess contains invalid characters.\n")


def input(prompt=None):
    """
        DO NOT MODIFY: Uncomment this function when submitting to Codio
        or when using the run_file.py to test your code.
        This function is needed for testing in Codio to echo the input to the output
        Function to get user input from the standard input (stdin) with an optional prompt.
        Args:
            prompt (str, optional): A prompt to display before waiting for input. Defaults to None.
        Returns:
            str: The user input received from stdin.
    """

    if prompt:
        print(prompt, end="")
    aaa_str = sys.stdin.readline()
    aaa_str = aaa_str.rstrip("\n")
    print(aaa_str)
    return aaa_str


def open_crossword_file():
    """
    Open a crossword puzzle file and return the Crossword object.
    :return: crossword puzzle object
    """
    try:
        filename = input(PUZZLE_PROMPT) # prompt for crossword puzzle filename
        crossword = Crossword(filename)  # load crossword puzzle from file
        crossword._load(filename)
        display_clues(crossword, 5)
        print(crossword)  # display the crossword puzzle
        return crossword
    except FileNotFoundError:  # catch file not found error
        print(PUZZLE_FILE_ERROR)
        return open_crossword_file()   # prompt for a new crossword puzzle filename


def display_clues(crossword, number_of_clues=0):
    """
    Display a set number of across and down clues for the user.
    :param crossword: A Crossword object representing the current state of the crossword puzzle.
    :param number_of_clues: An integer representing the number of clues to display for each clue type.
                            The default is 0, which means display all clues.
    """
    across_clues = []  # create empty lists for across and down clues
    down_clues = []  # create empty lists for across and down clues

    for clue in crossword.clues.values():  # loop through the clues in the crossword object
        if clue.down_across == 'A':
            across_clues.append(clue)
        elif clue.down_across == 'D':
            down_clues.append(clue)

    across_clues.sort()
    down_clues.sort()
    for direction, clues in (("Across", across_clues), ("Down", down_clues)):  # loop through across and down clues
        print(f"\n{direction}")
        for clue in clues[:number_of_clues or None]:  # if number_of_clues is 0, it defaults to None
            print(clue)


def get_validation(crossword, user_input):
    """
    Validate user input and return the command or action to be taken.
    :param crossword:
    :param user_input:
    :return: Depending on the user input, return the command to be executed, or None if the input is invalid.
    """
    user_input = user_input.split()
    if user_input[0] == "C":  # Display clues
        if len(user_input) != 2 or not user_input[1].isdigit():  # Check if the input is valid
            print("Invalid option/arguments. Type 'H' for help.")
            return None  # Return None if the input is invalid
        else:
            return display_clues(crossword, int(user_input[1]))
    elif user_input[0] in ["R", "T", "G"]:
        if len(user_input) != 4 or user_input[3] not in ["A", "D"] or not (
                user_input[1].isdigit() and user_input[2].isdigit()):  # Check if the input is valid
            print("Invalid option/arguments. Type 'H' for help.")   # Print an error message if the input is invalid
            return None
        else:
            clue_key = (int(user_input[1]), int(user_input[2]), user_input[3])  # Create a clue key from the user input
            clue = crossword.clues.get(clue_key)  # Get the clue from the crossword object
            if not clue:
                print("Invalid option/arguments. Type 'H' for help.")   # Print an error message if the input is invalid
                return None
            if user_input[0] == "R":
                crossword.reveal_answer(clue)  # Reveal the answer for the clue
                return Clue.__repr__(clue)  # Return the clue representation
            elif user_input[0] == "T":
                index = crossword.find_wrong_letter(clue)  # Find the first wrong letter in the clue
                if index == -1:
                    print("This clue is already correct!")
                else:
                    print("Letter {} is wrong, it should be {}".format(int(index + 1), clue.answer[index]))
            elif user_input[0] == "G":
                while True:
                    new_guess_input = input("Enter your guess (use _ for blanks): ").upper()
                    if not all(char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ_" for char in new_guess_input):
                        print("Guess contains invalid characters.")
                    elif len(new_guess_input) != len(clue.answer):  #Check if the guess length matches the length of the clue
                        print("Guess length does not match the length of the clue.")
                    else:
                        break
                crossword.change_guess(clue, new_guess_input)  # Change the guess for the clue
                return Clue.__repr__(clue)
    elif user_input[0] in ["S", "Q", "H"]:  # Restart, Quit, or Help
        if len(user_input) > 1:
            print("Invalid option/arguments. Type 'H' for help.")  #
            return None
        else:
            return user_input[0]  # Return the command itself for 'S', 'Q', 'H'


def main():
    crossword = open_crossword_file()
    print(HELP_MENU)
    while True:
        user_input = input(OPTION_PROMPT)
        validation = get_validation(crossword, user_input)

        if validation == "S":
            crossword = open_crossword_file()  # Restart the game with a new puzzle
            print(HELP_MENU)
        elif validation == "Q":
            break
        elif validation == "H":
            print(HELP_MENU)
        elif validation is None and user_input[0] == "T":
            continue
        elif validation is not None or user_input[0] in ["G"]:  # Make a guess
            user_input = user_input.split()  # Split the user input
            # Check if the input is valid
            if int(user_input[1]) in range(0, 5) and int(user_input[2]) in range(0, 5) and user_input[3] in ["A", "D"]:
                print(crossword)
            else:
                continue # Print the crossword after any potentially puzzle-altering action
        elif validation is not None or user_input[0] in ["R"]:
            user_input = user_input.split()
            if int(user_input[1]) in range(0, 5) and int(user_input[2]) in range(0, 5) and user_input[3] in ["A", "D"]:
                print(crossword)
            else:
                continue
        elif user_input[0] not in ["C","R", "T", "G", "S", "Q", "H"]: # Check if the input is valid
            print("Invalid option/arguments. Type 'H' for help.")
            continue
        # Check if the puzzle is solved after any action that could potentially complete it
        if crossword.is_solved():
            print("Puzzle solved! Congratulations!")
            break


if __name__ == "__main__":
    main()