# writen by Lingyuan Jin ID:1020657 and Jiachen Li 1068299
from itertools import permutations
from search.util import print_slide, print_swing, print_board
from search.token import Friendly, Enemy, Block

class Game:
    def __init__(self, data):
        self.next_move_dict = {}
        self.friendly_list = []
        self.enemy_list = []
        self.block_list = []
        self.turn = 0
        self.init_data(data)
        # self.print_game()

    # read json file
    def init_data(self, data):
        for token in data["upper"]:
            cord = (token[1], token[2])
            self.friendly_list.append(Friendly(token[0], cord))
        for token in data["lower"]:
            cord = (token[1], token[2])
            self.enemy_list.append(Enemy(token[0], cord))
        for token in data["block"]:
            cord = (token[1], token[2])
            self.block_list.append(Block(cord))

    # make game stop
    def game_over(self):
        for enemy in self.enemy_list:
            if enemy.active:
                return False
        return True

    def num_friendly(self):
        return len(self.friendly_list)

    def get_next_target_loop(self):
        for friendly in self.friendly_list:
            friendly.get_next_target(self)

    def get_order_list(self):
        return list(permutations(range(0, self.num_friendly()), self.num_friendly()))

    # Act all upper tokens in order, return -1 if one token have no valid move
    def act_all(self, order):
        for i in order:
            state = self.friendly_list[i].act(self)
            if state == -1:
                return -1
        return 0

    # def print_game(self):
    #     board_dict = {}
    #     for friendly in self.friendly_list:
    #         if friendly.active:
    #             cord = friendly.cord
    #             if (cord in board_dict):
    #                 board_dict[cord] += friendly.symbol.upper()
    #             else:
    #                 board_dict[cord] = friendly.symbol.upper()
    #     for enemy in self.enemy_list:
    #         if enemy.active:
    #             cord = enemy.cord
    #             if (cord in board_dict):
    #                 board_dict[cord] += ('(' + enemy.symbol + ')')
    #             else:
    #                 board_dict[cord] = ('(' + enemy.symbol + ')')
    #     for block in self.block_list:
    #         if (block.cord in board_dict):
    #             board_dict[block.cord] += ('X')
    #         else:
    #             board_dict[block.cord] = ('X')
    #     print_board(board_dict, str(self.turn))

    # print the move
    def apply_move(self):
        for token, move in self.next_move_dict.items():
            (r_a, q_a) = token.cord
            (r_b, q_b) = move
            if move in token.potential_slide(token.cord):
                print_slide(self.turn, r_a, q_a, r_b, q_b)
            else:
                print_swing(self.turn, r_a, q_a, r_b, q_b)
            token.cord = move
            # update the state of eliminated token
            for enemy in self.enemy_list:
                if enemy.active and token.cord == enemy.cord:
                    if token.can_defeat(enemy) == 1:
                        enemy.active = False
                    elif token.can_defeat(enemy) == -1:
                        token.active = False
            for friendly, friendly_move in self.next_move_dict.items():
                if token != friendly and move == friendly_move:
                    if token.can_defeat(friendly) == -1:
                        token.active = False
        # self.print_game()
        self.next_move_dict = {}

    # update the attribute of game
    def turn_update(self):
        self.turn += 1
        self.get_next_target_loop()

        # try move in different order
        order_list = self.get_order_list()
        for order in order_list:
            state = self.act_all(order)
            # if success
            if state == 0:
                self.apply_move()
                return 0
            self.next_move_dict = {}
        return -1
