"""
Actual implementation of the Wordle bot.
"""

import json
import random

WORDLIST_FILENAME = "wordlists/wordlist-en.json"


def read_wordlist(filename: str) -> "list[str]":
    """
    Reads the wordlist.
    """

    with open(filename, "r") as f:
        return [el.upper() for el in json.load(f)]


def make_guess(list_: "list[str]", filters):
    """
    Applies the filters and finds the best word among the results.
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

    return random.choice(highest) if len(highest) > 1 else best_word


def rate_by_diversity(word: str) -> int:
    """
    Diverse letters get more points.
    """

    letters = set(word)

    return len(letters)


def generate_filters_from_feedback(feedback: str):
    """
    Generates Filters from feedback.
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


def main() -> None:
    """
    The main function for using the app.
    """

    wordlist = read_wordlist(WORDLIST_FILENAME)

    r: int = 0
    filters: list = []

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
                print("Another guess:", another_guess)
                continue

            new_filters = generate_filters_from_feedback(feedback)
            filters.extend(new_filters)

        guess = make_guess(wordlist, filters)
        print("Guess:", guess)

        r += 1


if __name__ == "__main__":
    main()
