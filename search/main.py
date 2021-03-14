"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json
import search.ai_util as au

# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from search.util import print_board, print_slide, print_swing


# key: cur 当前坐标tuple
# value: [[]upper/lower, r/s/p/b],[...]]
board_dict = {}


def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)


    # TODO
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).

    au.json_to_dict(data, board_dict)

    # while跑到游戏胜利
    while not au.check_win(board_dict):
        print(au.check_win(board_dict))

    # 每一个回合
    print(board_dict)
    for cur, token_list in board_dict.items():
        for token in token_list:
            if token[0] == "upper":
                print(cur)
                # best_move = au.get_next_move()
                # au.move(cur, best_move)

