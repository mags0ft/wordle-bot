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

    with open(path.join("wordlists", "wordlist.json"), "w") as f:
        dump([el.strip() for el in l], f)


if __name__ == "__main__":
    main()
