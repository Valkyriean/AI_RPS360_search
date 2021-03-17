import random
import search.util as u
import token as T
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
        friendly_list.append(T.Friendly(token[0], token_coordinate))
    for token in data["lower"]:
        token_coordinate = (token[1], token[2])
        enemy_list.append(T.Enemy(token[0], token_coordinate))
    for token in data["block"]:
        token_coordinate = (token[1], token[2])
        block_list.append(token.Block(T.Block(token_coordinate)))
    return friendly_list, enemy_list, block_list



# return a list of potential target that can be eaten
def potential_target(token, enemy_list):
    potential_target_list = []
    for enemy in enemy_list:
        if token.can_defeat(enemy):
            potential_target_list.append(enemy)
    return potential_target_list


# return the valid grids around cur
def potential_slide(cur):
    surrounding_list = []
    for move_vector in move_vector_list:
        tar = (cur[0] + move_vector[0], cur[1] + move_vector[1])
        surrounding_list.append(tar)
    return surrounding_list


def potential_swing(cur, friendly_list):
    surrounding_list = potential_slide(cur)
    swing_list = []
    for friendly in friendly_list:
        friendly_pos = friendly.path[-1]
        if friendly_pos in surrounding_list:
            swing_list += potential_slide(friendly_pos)
    return swing_list

def remove_out_bound(potential_move_list):
    for cord in potential_move_list.copy():
        if abs(cord[0]) > 4 or abs(cord[1]) > 4 or abs(cord[0]+cord[1]) > 4:
            potential_move_list.remove(cord)

def remove_on_block(block_list, potential_move_list):
    for block in block_list:
        if block.cord in potential_move_list:
            potential_move_list.remove(block)


def remove_enemy_kill(token, enemy_list, potential_move_list):
    for enemy in enemy_list:
        hit_enemy = enemy.cord in potential_move_list
        killed_by_enemy = token.can_defeat(enemy['type']) == -1
        if enemy.active and hit_enemy and killed_by_enemy:
            potential_move_list.remove(enemy.cord)


def remove_friendly_kill(token, friendly_list, potential_move_list):
    for friendly in friendly_list:
        friendly_pos = friendly.path[-1]
        friendly_fire = token.can_defeat(friendly)
        if friendly_fire != 0 and friendly_pos in potential_move_list:
            potential_move_list.remove(friendly_pos)


def potential_move(cur, token, friendly_list, enemy_list, block_list):
    potential_move_list = []
    # add slide
    potential_move_list += potential_slide(cur)
    # add swing
    potential_move_list += potential_swing(cur, friendly_list)
    # remove replic
    potential_move_list = list(set(potential_move_list))
    if cur in potential_move_list:
        potential_move_list.remove(cur)
    # remove out of bound
    remove_out_bound(potential_move_list)
    # remove step on block
    remove_on_block(block_list, potential_move_list)
    # remove killed by enemy
    remove_enemy_kill(token, enemy_list, potential_move_list)
    # remove killed by friendly
    remove_friendly_kill(token, friendly_list, potential_move_list)
    return potential_move_list


def search(token, target, friendly_list, enemy_list, block_list):
    path = []
    origin = token.path[-1]
    token_type = token.symbol

    # TODO subtitute with a*
    budget = 100
    queue = []
    queue.append(origin)
    while queue:
        path = queue.pop(0)
        if len(path) > budget:
            return path, False
        if type(path) == tuple:
            path = [path]        
        node = path[-1]
        if node == target:
            path.pop(0)
            return path,True
        cur_round = len(token.path) + len(path) - 2
        potential_move_list = potential_move(node, token_type, friendly_list, enemy_list, block_list)
        for move in potential_move_list:
            new_path = path.copy()
            new_path.append(move)
            queue.append(new_path)
    # do not include start point but the finishing point
    return None,False

# TODO change this to only return one step
def build_path(token, friendly_list, enemy_list, block_list):
    potential_target_list = potential_target(token, enemy_list)
    potential_path_list = []
    min_cost = 99999999
    chosen = []
    killed_enemy = {}
    for target in potential_target_list:
        path,killed = search(token, target.cord, friendly_list, enemy_list, block_list)
        if len(path) < min_cost:
            chosen = path
            min_cost = len(path)
            if killed:
                killed_enemy = target
    if killed_enemy:
        killed_enemy.active = False
    return chosen



# TODO move token in good order for one step
# loop through upper tokens and build path for each
def eat_enemy(data):
    friendly_list, enemy_list, block_list = data_to_path(data)
    # loop til no more lower token
    win = False
    while win == False:
        # try find a target to eat, if no target or not accessable at the moment, stay still
        for token in friendly_list:
            token.path += build_path(token, friendly_list, enemy_list, block_list)
        win = True
        for enemy in enemy_list:
            if enemy.active:
                win = False
    return friendly_list, enemy_list, block_list


def makeup_rest(friendly_list, enemy_list, block_list):
    max_round = -1
    for enemy in enemy_list:
        cur_round = enemy['death_round']
        if cur_round > max_round:
            max_round = cur_round

    for friendly in friendly_list:
        cur_round = len(friendly['path']) - 1
        while cur_round < max_round:
            move_list = potential_move(friendly['path'][-1], friendly['type'], cur_round, friendly_list, enemy_list, block_list)
            move = random.choice(move_list)
            friendly['path'].append(move) 
            cur_round += 1
    return max_round


def print_path(max_round, friendly_list, enemy_list, block_list):
    list_to_dict(0, friendly_list, enemy_list, block_list)
    for i in range(1,max_round + 1):
        list_to_dict(i, friendly_list, enemy_list, block_list)
        for friendly in friendly_list:
            last_cord = friendly.path[i - 1]
            cur_cord = friendly.path[i]
            if cur_cord in potential_slide(last_cord):
                u.print_slide(i, last_cord[0], last_cord[1], cur_cord[0], cur_cord[1])
            else:
                u.print_swing(i, last_cord[0], last_cord[1], cur_cord[0], cur_cord[1])



def list_to_dict(i, friendly_list, enemy_list, block_list):
    board_dict = {}
    for friendly in friendly_list:
        cord = friendly.path[i]
        if(cord in board_dict):
            board_dict[cord] += friendly['type'].upper()
        else:
            board_dict[cord] = friendly['type'].upper()
    for enemy in enemy_list:
        if i < enemy['death_round']:
            cord = enemy['cord']
            if(cord in board_dict):
                board_dict[cord] += ('(' + enemy['type'] + ')')
            else:
                board_dict[cord] = ('(' + enemy['type'] + ')')
    for block in block_list:
        if(block in board_dict):
            board_dict[block] += ('X')
        else:
            board_dict[block] = ('X')
    u.print_board(board_dict,str(i))

