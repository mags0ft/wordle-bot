"""
Converts a wordlist from a text file into a JSON file.
"""

from json import dump
from os import path


def main():
    """
    Main method to convert the wordlist.
    """

    with open(path.join("wordlists", "wordlist.txt"), "r") as f:
        l = f.readlines()

    converted_list: list = []

    for el in l:
        converted_list.append(el.strip())

    with open(path.join("wordlists", "wordlist.json"), "w") as f:
        dump(converted_list, f)


if __name__ == "__main__":
    main()
