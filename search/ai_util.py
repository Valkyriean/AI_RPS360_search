import random

# moving vector
move_vector_list = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]


# turn raw data into three list of upper, lower, and blocks
# ("r", [(0,0),(1,0)])

# friendly_list = [[type, [(start coordinate), ... moving sequence], ...]
# note that index of moving sequence is the round number or the location token sit on at that round
# enemy_list = [[type, coordinate, round of death], ...]
def data_to_path(data):
    friendly_list = []
    enemy_list = []
    block_list = []
    for token in data["upper"]:
        token_coordinate = (token[1], token[2])
        friendly_list.append([token[0],[token_coordinate]])
    for token in data["lower"]:
        token_coordinate = (token[1], token[2])
        enemy_list.append([token[0],token_coordinate, -1])
    for token in data["block"]:
        token_coordinate = (token[1], token[2])
        block_list.append(token_coordinate)
    return friendly_list, enemy_list, block_list


# check if out can eat tar
def can_defeat(our, tar):
    if (our == "p" and tar == "r") or (our == 'r' and tar == 's') or (our == 's' and tar == 'p'):
        return 1
    elif our == tar:
        return 0
    else:
        return -1

# return a list of potential target that can be eaten
def potential_target(token, enemy_list):
    potential_target_list = []
    for enemy in enemy_list:
        if can_defeat(token[0], enemy[0]) == 1:
            enemy_coordinate = (enemy[1][0], enemy[1][1])
            potential_target_list.append(enemy_coordinate)
    return potential_target_list

# Check if the grid is a valid move
def movable(tar, block_list):
    # out of bound
    if abs(tar[0]) > 4 or abs(tar[1]) > 4:
        return False
    # hit a block
    if tar in block_list:
        return False
    return True


# return the valid grids around cur
def potential_slide(cur, block_list):
    surrounding_list = []
    for move_vector in move_vector_list:
        tar = (cur[0] + move_vector[0], cur[1] + move_vector[1])
        if movable(tar, block_list):
            surrounding_list.append(tar)
    return surrounding_list


def potential_move(cur, token, round, friendly_list, enemy_list, block_list):
    surrounding_list = potential_slide(cur, block_list)
    # put in potential slide grids
    move_list = surrounding_list.copy()
    # check friendly that we can swing on
    for friendly_token in friendly_list:
        if len(friendly_token[1]) < round:
            continue
        friendly_pos = friendly_token[1][round]
        if friendly_pos in surrounding_list:
            move_list += potential_slide(friendly_pos, block_list)
    # remove the grid that may killed by enemy
    for enemy in enemy_list:
        if enemy[1] in move_list and can_defeat(token[0], enemy[0]) == -1:
            move_list.remove(enemy[1])

    # remove the grid that my kill or killed by friendly
    for friendly_token in friendly_list:
        if len(friendly_token[1]) < round:
            continue
        friendly_pos = friendly_token[1][round+1]
        friendly_fire = can_defeat(token[0], friendly_token[0])
        if friendly_fire != 0 and friendly_pos in move_list:
            move_list.remove(friendly_pos)

    move_list = list(dict.fromkeys(move_list))
    move_list.remove(cur)        
    return move_list


def search(token, target, friendly_list, enemy_list, block_list):
    path = []
    origin = token[1][-1]

    # TODO subtitute with a*
    queue = []
    queue.append(origin)
    while queue:
        path = queue.pop(0)
        if type(path) == tuple:
            path = [path]        
        node = path[-1]
        if node == target:
            path.pop[0]
            return path
        potential_move_list = potential_move(node, token, len(token[1])+len(path)-2, friendly_list, enemy_list, block_list)
        for move in potential_move_list:
            new_path = path.copy()
            new_path.append(move)
            queue.append(new_path)
    # do not include start point but the finishing point


# token: ("r", [(0,0),(1,0)])
def build_path(token, friendly_list, enemy_list, block_list):
    potential_target_list = potential_target(token, enemy_list)
    potential_friendly_list = []
    for target in potential_target_list:
        potential_friendly_list.append(search(token, target, friendly_list, enemy_list, block_list))
    chosen = min(potential_friendly_list, key = len)
    index = 0
    # remove eaten enemy
    for enemy in enemy_list.copy():
        if enemy[1] == chosen[-1]:
            enemy_list.pop(index)
            break
        index+=1
    return chosen




# loop through upper tokens and build path for each
def build_friendly_list(data):
    friendly_list, enemy_list, block_list = data_to_path(data)
    # loop til no more lower token
    while len(enemy_list) > 0:
        # try find a target to eat, if no target or not accessable at the moment, stay still
        for token in friendly_list:
            token[1] += build_path(token, friendly_list, enemy_list, block_list)
    
    return friendly_list




# def print_path(friendly_list):
#     friendly_count = len(friendly_list)
#     turn = 1
#     while friendly_count > 0:
#         for token in friendly_list:
#             if len(token[1])





