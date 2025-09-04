# Gathering word lists

This directory contains scripts to convert word lists from one format to another.

Some Wordle provider websites use different formats to store their word lists. For example, some may encode the characters used in the words as two-digit decimal numbers as ASCII code points for the respective characters. Other providers may simply store the words in a plain text file, with one word per line.

You can use the scripts `convert_encoded.py` and `convert_txt_to_json.py` to convert these into usable JSON files respectively.

The final wordlist should be in the following format:

```json
[
    "APPLE",
    "BERRY",
    "CHARM",
    ...
]
```

_(all capital letters, all exactly 5 characters long, all ASCII)_
