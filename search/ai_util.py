import random

# 移动向量
move_vector_list = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]


# 我们的key (x,y) value: [upper/lower, r/s/p/b]
# 她的key upper/lower/block value: [[r/s/p, x, y],[...]]
def json_to_dict(data, board_dict):
    for faction, token_list in data.items():
        for token in token_list:
            token_type = token[0]
            token_coordinate = (token[1], token[2])
            board_dict[token_coordinate] = [[faction, token_type]]


# 监测输入格子是否可用
def movable(tar, board_dict):
    # 走出棋盘
    if abs(tar[0]) > 4 or abs(tar[1]) > 4:
        return False
    # 撞block
    if tar in board_dict and board_dict[tar][0][0] == "block":
        return False
    return True


# 返回当前点周围没有出界且不是block的格子
def potential_slide(cur, board_dict):
    surrounding_list = []
    for move_vector in move_vector_list:
        tar = (cur[0] + move_vector[0], cur[1] + move_vector[1])
        if movable(tar, board_dict):
            surrounding_list.append(tar)
    return surrounding_list


def potential_swing(cur, board_dict):
    swing_list = []
    surrounding_list = potential_slide(cur, board_dict)
    for loc in surrounding_list:
        if loc in board_dict:
            for token in board_dict[loc]:
                if token[0] == "upper":
                    swing_list += (list(set(potential_slide(loc, board_dict))-set(surrounding_list)))
                    break
    swing_list = list(dict.fromkeys(swing_list))
    swing_list.remove(cur)
    return swing_list


# 不会重叠所以用当前坐标作为唯一识别
def move(cur, index, tar, board_dict):



    if board_dict.contain(tar):
        return
        # 吃人
    # 输出当前步骤，可以引用util.print_slide
    return


# 返回分数 e r(n) = (h(n) + score(n) − score(nParent)) × γ**d
def get_reward(cur, board_dict, next_board_dict):
    # 用推演未来惩罚吃掉队友
    return


# 返回tar 下一步坐标
def get_next_move(cur, index, board_dict):
    # future_board_dict = board_dict.copy()

    potential_slide_list = potential_slide(cur, board_dict)
    potential_swing_list = potential_swing(cur, board_dict)
    all_moves = potential_slide_list + potential_swing_list
    # for potential_tar in potential_move_list:
    #     get_reward(potential_move_list, future_board_dict)
    #     # 算分， 加入pq
    return all_moves[random.randint(0, all_moves.len-1)]

