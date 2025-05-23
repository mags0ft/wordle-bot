# Wordle-Bot

A simple Wordle bot that gives you tips for the game using basic strategic thinking. The bot uses a list of 5-letter words and tries to guess the correct word by making educated guesses based on the feedback it receives.

The list is narrowed down until you (hopefully) find the correct word!

## How to use

1. find a wordlist for your specific instance/distribution of Wordle (language- and implementation-specific)
2. put the wordlist in the `wordlists` folder, make sure it's a `.json` list (you can find basic conversion scripts in the `wordlists/utils` folder)
3. run the script with `python3 ./bot.py`
4. have fun!
