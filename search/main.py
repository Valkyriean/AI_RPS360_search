"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json

# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from search.util import print_board, print_slide, print_swing


def add_to_out(type, data, out):
    if type in data:
        for i in data[type]:
            out[(i[1], i[2])] = i[0]


def add_target(role,data):
    role


def main():
    types = ["lower", "upper", "block"]
    out = {}
    pa = {}
    ro = {}
    sc = {}
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
        # put coordinates in dict to print board
        for i in types:
            add_to_out(i, data, out)
        print_board(out, "test")

    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).
