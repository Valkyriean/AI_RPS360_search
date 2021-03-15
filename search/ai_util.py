import random

# 移动向量
move_vector_list = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]


# 记录每个棋子的每一步的走法
# ("r", [(0,0),(1,0)])
def data_to_path(data):
    path_list = []
    enemy_list = []
    block_list = []
    for token in data["upper"]:
        token_coordinate = (token[1], token[2])
        path_list.append((token[0],[token_coordinate]))
    for token in data["lower"]:
        token_coordinate = (token[1], token[2])
        enemy_list.append((token[0],token_coordinate))
    for token in data["block"]:
        token_coordinate = (token[1], token[2])
        block_list.append(token_coordinate)
    return path_list, enemy_list, block_list


# 判断our能不能干死tar
def can_defeat(our, tar):
    if (our == "p" and tar == "r") or (our == 'r' and tar == 's') or (our == 's' and tar == 'p'):
        return 1
    elif our == tar:
        return 0
    else:
        return -1

# 返回可能有的敌人
def potential_target(token, enemy_list):
    potential_target_list = []
    for enemy in enemy_list:
        if can_defeat(token[0], enemy[0]) == 1:
            enemy_coordinate = (enemy[1][0], enemy[1][1])
            potential_target_list.append(enemy_coordinate)
    return potential_target_list

# 监测输入格子是否可用
# TODO 把乱七八糟的检测都放在这里
def movable(tar, block_list):
    # 走出棋盘
    if abs(tar[0]) > 4 or abs(tar[1]) > 4:
        return False
    # 撞block
    if tar in block_list:
        return False
    return True


# 返回当前点周围没有出界且不是block的格子
def potential_slide(cur, block_list):
    surrounding_list = []
    for move_vector in move_vector_list:
        tar = (cur[0] + move_vector[0], cur[1] + move_vector[1])
        if movable(tar, block_list):
            surrounding_list.append(tar)
    return surrounding_list


def potential_move(cur, token, round, path_list, enemy_list, block_list):
    surrounding_list = potential_slide(cur, block_list)
    # 把周围的格子放进来
    move_list = surrounding_list.copy()
    # 检测那个时候可以芜湖的队友
    for friendly_token in path_list:
        if len(friendly_token[1]) < round:
            continue
        friendly_pos = friendly_token[1][round]
        if friendly_pos in surrounding_list:
            move_list += potential_slide(friendly_pos, block_list)
    # 去掉可能被敌人干死的位置
    for enemy in enemy_list:
        if enemy[1] in swing_list and can_defeat(token[0], enemy[0]) == -1:
            move_list.remove(enemy[1])

    # 去掉那个时候可能干死或者被干死的队友
    for friendly_token in path_list:
        if len(friendly_token[1]) < round:
            continue
        friendly_pos = friendly_token[1][round+1]
        friendly_fire = can_defeat(token[0], friendly_token[0])
        if friendly_fire != 0 and friendly_pos in move_list:
            move_list.remove(friendly_pos)

    move_list = list(dict.fromkeys(swing_list))
    move_list.remove(cur)        
    return move_list


def search(token, target, path_list, enemy_list, block_list):
    path = []
    origin = token[1][-1]

    # TODO 搜索算法放这里
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
        potential_move_list = potential_move(node, token, len(token[1])+len(path)-2, path_list, enemy_list, block_list)
        for move in potential_move_list:
            new_path = path.copy()
            new_path.append(move)
            queue.append(new_path)
    # 不要返回起点 但是要返回终点


# token: ("r", [(0,0),(1,0)])
def build_path(token, path_list, enemy_list, block_list):
    potential_target_list = potential_target(token, enemy_list)
    potential_path_list = []
    for target in potential_target_list:
        potential_path_list.append(search(token, target, path_list, enemy_list, block_list))
    chosen = min(potential_path_list, key = len)
    index = 0
    for enemy in enemy_list.copy():
        if enemy[1] == chosen[-1]:
            enemy_list.pop(index)
            break
        index+=1
    # remove吃掉的敌人
    return chosen




# 循环每一个友方棋子 并建立路径
def build_path_list(data):
    path_list, enemy_list, block_list = data_to_path(data)
    # 吃到没有敌人可以吃为止
    while len(enemy_list) > 0:
        #每个棋子去试图吃一个人, 如果暂时吃不到或者没人可以吃的话就不动
        for token in path_list:
            token[1] += build_path(token, path_list, enemy_list, block_list)
    
    return path_list




# def print_path(path_list):
#     friendly_count = len(path_list)
#     turn = 1
#     while friendly_count > 0:
#         for token in path_list:
#             if len(token[1])





