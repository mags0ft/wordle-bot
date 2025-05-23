"""
Converts ASCII-Encoded character strings back into actual letters.
"""

from json import load, dump
from os import path


def main():
    """
    Main method to convert the wordlist.
    """

    with open(path.join("wordlists", "encoded-wordlist.json"), "r") as f:
        l = load(f)

    def convert_letters(num_string: str):
        converted = ""

        for letter in range(0, len(num_string), 2):
            num: int = int(num_string[letter : letter + 2])
            converted += chr(num)

        return converted

    converted_list: str = []

    for el in l:
        converted_list.append(convert_letters(el))

    with open(path.join("wordlists", "encoded-wordlist.json"), "w") as f:
        dump(converted_list, f)


if __name__ == "__main__":
    main()
