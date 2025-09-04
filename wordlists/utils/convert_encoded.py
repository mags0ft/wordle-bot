"""
Converts ASCII-Encoded character strings back into actual letters.
"""

from json import load, dump
from os import path


def main():
    """
    Main method to convert the wordlist.
    """

    def _convert_letters(num_string: str):
        converted = ""

        for letter in range(0, len(num_string), 2):
            num: int = int(num_string[letter : letter + 2])
            converted += chr(num)

        return converted
    
    with open(path.join("wordlists", "encoded-wordlist.json"), "r") as f:
        l = load(f)

    with open(path.join("wordlists", "encoded-wordlist.json"), "w") as f:
        dump([_convert_letters(el) for el in l], f)


if __name__ == "__main__":
    main()
