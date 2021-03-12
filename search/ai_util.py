# 移动向量
move_vector_list = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]


# 我们的key (x,y) value: [upper/lower, r/s/p/b]
# 她的key upper/lower/block value: [[r/s/p, x, y],[...]]
def json_to_dict(data, board_dict):
    for faction, token_list in data.items():
        for token in token_list:
            token_type = token[0]
            token_coordinate = (token[1], token[2])
            assert token_coordinate not in board_dict.keys()
            board_dict[token_coordinate] = [faction, token_type]


# 监测输入格子是否可用
def movable(tar, board_dict, potential_move_list):
    # 走出棋盘
    if abs(tar[0]) > 4 or abs(tar[1]) > 4:
        return False
    # 装block
    if board_dict[tar][1] is 'block':
        return False
    if tar in potential_move_list:
        return False
    return True


# 返回所有可以走的格子的list
def potential_move(cur, board_dict):
    potential_move_list = [cur]
    # 周围和可以swing的位置
    surrounding_list = []
    for move_vector in move_vector_list:
        surrounding_list.append(cur + move_vector)
    for loc in surrounding_list:
        if board_dict[loc][0] is "upper":
            # 有友军 可以摆
            for move_vector in move_vector_list:
                swing_tar = loc + move_vector
                if movable(swing_tar, board_dict, potential_move_list):
                    potential_move_list.append(swing_tar)
        if movable(loc, board_dict, potential_move_list):
            potential_move_list.append(loc)
    return potential_move_list[1:]


# 不会重叠所以用当前坐标作为唯一识别
def move(cur, tar, board_dict):
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
def get_next_move(cur, board_dict):
    future_board_dict = board_dict.copy()
    potential_move_list = potential_move(cur, board_dict)
    for potential_tar in potential_move_list:
        get_reward(potential_move_list, future_board_dict)
        # 算分， 加入pq

    return
