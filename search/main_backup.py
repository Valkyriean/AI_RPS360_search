"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json
import ai_util

# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from search.util import print_board, print_slide, print_swing


board_dict = {}

def add_to_out(type, data, out):
    if type in data:
        for i in data[type]:
            out[(i[1], i[2])] = i[0]


def add_target(lower_data, pa, ro, sc):
    for i in lower_data:
        if i[0] == 's':
            ro['target'] = (i[1], i[2])
        elif i[0] == 'r':
            pa['target'] = (i[1], i[2])
        else:
            sc['target'] = (i[1], i[2])


def record_block(data, block):
    for i in data:
        block.append((i[1], i[2]))


def record_origin(upper_data, pa, ro, sc):
    for i in upper_data:
        if i[0] == 's':
            sc['origin'] = (i[1], i[2])
            sc['path'] = []
        elif i[0] == 'r':
            ro['origin'] = (i[1], i[2])
            ro['path'] = []
        else:
            pa['origin'] = (i[1], i[2])
            pa['path'] = []


def init(data, types, pa, ro, sc, block):
    add_target(data[types[0]], pa, ro, sc)
    record_origin(data[types[1]], pa, ro, sc)
    record_block(data[types[2]], block)


# simple slide
def find_path(token):
    if len(token) == 0:
        return 0
    find = False
    now = [token['origin'][0], token['origin'][1]]
    target = token['target']
    while not find:
        if now[0] == target[0] and now[1] == target[1]:
            find = True
        else:
            if now[0] - target[0] > 0 and now[1] - target[1] < 0:
                # move right up
                now[0] -= 1
                now[1] += 1
                token['path'].append([now[0], now[1]])
            elif now[0] - target[0] < 0 and now[1] - target[1] > 0:
                # move right down
                now[0] += 1
                now[1] -= 1
                token['path'].append([now[0], now[1]])

            elif now[0] - target[0] < 0:
                # move to right hex
                now[0] += 1
                token['path'].append([now[0], now[1]])

            elif now[0] - target[0] > 0:
                # move to left hex
                now[0] -= 1
                token['path'].append([now[0], now[1]])
            elif now[1] - target[1] > 0:
                # move up
                now[1] -= 1
                token['path'].append([now[0], now[1]])
            else:
                # move down
                now[1] += 1
                token['path'].append([now[0], now[1]])


def print_path(token):
    if len(token) == 0:
        return 0
    now = token['origin']
    turn = 1
    steps = token['path']
    for i in steps:
        print_slide(turn, now[0], now[1], i[0], i[1])
        now = i
        turn += 1


def check_swing():
    return 0


def main():
    types = ["lower", "upper", "block"]
    out = {}
    pa = {}
    ro = {}
    sc = {}
    block = []
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).

    # put coordinates in dict to print board
    for i in types:
        add_to_out(i, data, out)

    # 初始化，每个棋子记录起始点和目标点，记录block的位置
    init(data, types, pa, ro, sc, block)

    # 寻找路径
    find_path(pa)
    find_path(ro)
    find_path(sc)

    # 打印结果
    print_path(pa)
    print_path(ro)
    print_path(sc)
