"""
Actual implementation of the Wordle bot. Handles reading the wordlist, making
guesses, and generating filters from feedback.
"""

import json
import os
import random

WORDLIST_FILENAME = os.path.join("wordlists", "wordlist-en.json")

WELCOME_MESSAGE = """Welcome to the Wordle solving assistant!
It will help you to solve fun little Wordle puzzles by making guesses.
After entering them, you need to provide feedback on the guesses.

Feedback format, always write it in front of each letter:
    . = gray
    _ = yellow
    ! = green
    - = do not give feedback on this letter

Type "r" to make another guess without giving feedback, which is useful if \
the current guess is not in the wordlist of the game.

Have fun!
"""


def read_wordlist(filename: str) -> "list[str]":
    """
    Reads the wordlist from a JSON list file.

    Arguments:
        filename: The path to the JSON file.

    Returns:
        A list of words in uppercase.
    """

    with open(filename, "r") as f:
        return [el.upper() for el in json.load(f)]


def make_guess(list_: "list[str]", filters) -> tuple[str, bool]:
    """
    Applies the filters and finds the best word among the results.

    Arguments:
        list_: The list of possible words.
        filters: The list of filter functions to apply.

    Returns:
        A tuple of the best guess and a boolean indicating if it's the only
        possible word left.
    """

    results = list(filter(lambda el: all(f(el) for f in filters), list_))

    print(
        "Possibilities:",
        ", ".join(results[:10]),
        f"[... {len(results)-10} more words ...]" if len(results) > 10 else "",
    )

    highest_points = -1
    best_word = "no guess"
    highest = []

    for word in results:
        points = rate_by_diversity(word)
        if points > highest_points:
            best_word = word
            highest_points = points
            highest = [word]
        elif points == highest_points:
            highest.append(word)

    return random.choice(highest) if len(highest) > 1 else best_word, len(
        results
    ) == 1


def rate_by_diversity(word: str) -> int:
    """
    Diverse letters get more points.

    Arguments:
        word: The word to rate.

    Returns:
        The number of unique letters in the word.
    """

    letters = set(word)

    return len(letters)


def generate_filters_from_feedback(feedback: str):
    """
    Generates Filters from feedback.

    Arguments:
        feedback: The feedback string.

    Returns:
        A list of filter functions.
    """

    generated_filters: list = []

    for idx in range(0, len(feedback), 2):
        set_: str = feedback.upper()[idx : idx + 2]
        type_: str = {".": "gray", "_": "yellow", "!": "green", "-": "none"}[
            set_[0]
        ]
        char: str = set_[1]

        if type_ == "gray":
            generated_filters.append(lambda word, char=char: char not in word)
        elif type_ == "yellow":
            generated_filters.append(
                lambda word, char_=char, pos=idx // 2: char_ in word
                and word[pos] != char_
            )
        elif type_ == "green":
            generated_filters.append(
                lambda word, char_=char, pos=idx // 2: word[pos] == char_
            )

    return generated_filters


def adjust_states(states: list, feedback: str) -> tuple[list, bool]:
    """
    Adjusts the states based on feedback.

    Arguments:
        states: The current states.
        feedback: The feedback string.

    Returns:
        The adjusted states.
    """

    is_valid: bool = True

    for idx in range(0, len(feedback), 2):
        set_: str = feedback.upper()[idx : idx + 2]
        type_: str = {".": 0, "_": 0, "!": 2, "-": states[idx // 2]}[set_[0]]

        if type_ > states[idx // 2]:
            # tighten character restriction (grey / yellow -> green)
            states[idx // 2] = type_

        elif type_ < states[idx // 2]:
            # user loosened a restriction - this isn't possible!
            is_valid = False

    return states, is_valid


def main() -> None:
    """
    The main function for using the app. Handles user interaction. Also prints
    instructions and welcomes the user.
    """

    wordlist = read_wordlist(WORDLIST_FILENAME)

    r: int = 0
    filters: list = []

    # keep track of states (. = 0, _ = 1, ! = 2)
    states: list = [0, 0, 0, 0, 0]

    print(WELCOME_MESSAGE)

    while True:
        if r > 0:
            feedback = ""
            while (
                len(feedback) != 10
                or not all(map(lambda el: el in "._-!", feedback[::2]))
            ) and feedback.lower() != "r":
                feedback = input(" >> ").replace(" ", "")

            if feedback.lower() == "r":
                another_guess = make_guess(wordlist, filters)
                print("Another guess:", another_guess[0])
                continue

            states, valid_states = adjust_states(states, feedback)

            if not valid_states:
                print("You loosened a character restriction. Revise input.")
                continue

            new_filters = generate_filters_from_feedback(feedback)
            filters.extend(new_filters)

        guess, finished = make_guess(wordlist, filters)
        print("Guess:", guess)

        r += 1

        if finished:
            print("The word has been found!")
            break


if __name__ == "__main__":
    main()
