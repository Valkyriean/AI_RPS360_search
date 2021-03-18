from itertools import permutations
from search.util import print_slide, print_swing, print_board
from search.token import Friendly, Enemy, Block

class Game():
    def __init__(self, data):
        self.next_move_dict = {}
        self.friendly_list = []
        self.enemy_list = []
        self.block_list = []
        self.turn = 0
        self.init_data(data)
        self.print_game()


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


    def game_over(self):
        for enemy in self.enemy_list:
            if enemy.active == True:
                return False
        return True

    def num_friendly(self):
        return len(self.friendly_list)

    
    def get_next_target_loop(self):
        for friednly in self.friendly_list:
            friednly.get_next_target(self)

    def get_order_list(self):
        return list(permutations(range(0, self.num_friendly()) , self.num_friendly()))


    def act_all(self, order):
        for i in order:
            state = self.friendly_list[i].act(self)
            if state == -1:
                return -1
        return 0


    def print_game(self):
        board_dict = {}
        for friendly in self.friendly_list:
            cord = friendly.cord
            if(cord in board_dict):
                board_dict[cord] += friendly.symbol.upper()
            else:
                board_dict[cord] = friendly.symbol.upper()
        for enemy in self.enemy_list:
            if enemy.active:
                cord = enemy.cord
                if(cord in board_dict):
                    board_dict[cord] += ('(' + enemy.symbol + ')')
                else:
                    board_dict[cord] = ('(' + enemy.symbol + ')')
        for block in self.block_list:
            if(block.cord in board_dict):
                board_dict[block.cord] += ('X')
            else:
                board_dict[block.cord] = ('X')
        print_board(board_dict, str(self.turn))

    def apply_move(self):
        for token, move in self.next_move_dict.items():
            (r_a, q_a) = token.cord
            (r_b, q_b) = move
            if move in token.potential_slide(token.cord):
                print_slide(self.turn,r_a, q_a, r_b, q_b)
            else:
                print_swing(self.turn,r_a, q_a,r_b, q_b)
            token.cord = move
            for enemy in self.enemy_list:
                if enemy.active and token.cord == enemy.cord and token.can_defeat(enemy) == 1:
                    enemy.active = False
        self.print_game()



        self.next_move_dict = {}

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
        return -1
