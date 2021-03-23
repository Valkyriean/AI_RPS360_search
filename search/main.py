"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json
import time

# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:


from search.game import Game


def main():
    start_time = time.time()
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # game loop
    game = Game(data)
    # loop til no more lower token
    while not game.game_over():
        # try find a target to eat, if no target or not accessable at the moment, stay still
        state = game.turn_update()
        if state == -1:
            return -1
    return 0
