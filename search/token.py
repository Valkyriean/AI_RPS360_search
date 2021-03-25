# writen by Lingyuan Jin ID:1020657 and Jiachen Li 1068299
import random
from queue import PriorityQueue


# calculate the Euclidean distance of two tokens
def dist_to(self, enemy):
    (r_o, q_o) = self
    (r_e, q_e) = enemy.cord
    return max(abs(r_e - r_o), abs(q_e - q_o), abs(q_o - q_e + r_o - r_e))

class Token:
    def __init__(self, symbol, cord):
        self.symbol = symbol
        self.cord = cord
        self.active = True


# upper token
class Friendly(Token):
    player = 'upper'
    move_vector_list = [(0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0)]

    def __init__(self, symbol, cord):
        super().__init__(symbol, cord)
        self.path = [cord]
        self.target = None
        self.useless = False
        self.potential_move_list = []
        self.future_cord = None

    # check whether can eliminate lower token
    def can_defeat(self, enemy):
        our = self.symbol
        tar = enemy.symbol
        if (our == "p" and tar == "r") or (our == 'r' and tar == 's') or (our == 's' and tar == 'p'):
            return 1
        elif our == tar:
            return 0
        else:
            return -1


    # find the nearest lower token which can defeat
    def get_next_target(self, game):
        min_dist = None
        nearest_enemy = None
        for enemy in game.enemy_list:
            if enemy.active and self.can_defeat(enemy) == 1:
                dist = dist_to(self.cord, enemy)
                if min_dist is None or dist < min_dist:
                    nearest_enemy = enemy
                    min_dist = dist
        if nearest_enemy is None:
            self.useless = True
            self.target = None
        else:
            self.target = nearest_enemy

    # put all the possible move in a list
    def potential_slide(self, cord):
        surrounding_list = []
        for move_vector in self.move_vector_list:
            tar = (cord[0] + move_vector[0], cord[1] + move_vector[1])
            surrounding_list.append(tar)
        return surrounding_list

    # put possible swing coordinates in the list
    def potential_swing(self, cord, game):
        surrounding_list = self.potential_slide(cord)
        swing_list = []
        for friendly in game.friendly_list:
            if friendly.cord in surrounding_list:
                swing_list += self.potential_slide(friendly.cord)
        return swing_list

    # check the movement is in the boundary
    def remove_out_bound(self):
        for cord in self.potential_move_list.copy():
            if abs(cord[0]) > 4 or abs(cord[1]) > 4 or abs(cord[0] + cord[1]) > 4:
                self.potential_move_list.remove(cord)

    # remove the movement will meet block token
    def remove_on_block(self, game):
        for block in game.block_list:
            if block.cord in self.potential_move_list:
                self.potential_move_list.remove(block.cord)

    # remove the movement will be defeated by lower token
    def remove_enemy_kill(self, game):
        if self.useless:
            return
        for enemy in game.enemy_list:
            hit_enemy = enemy.cord in self.potential_move_list
            killed_by_enemy = self.can_defeat(enemy) == -1
            if enemy.active and hit_enemy and killed_by_enemy:
                self.potential_move_list.remove(enemy.cord)

    # remove thr movement will defeat another upper token
    def remove_friendly_fire(self, game):
        for friendly, cord in game.next_move_dict.items():
            if cord in self.potential_move_list:
                if self.can_defeat(friendly) == 1:
                    self.potential_move_list.remove(cord)
                elif self.useless == False and self.can_defeat(friendly) == -1:
                    self.potential_move_list.remove(cord)

    # filter the possible movement
    def potential_move(self, accurate, cord, game):
        self.potential_move_list = []
        # add slide
        self.potential_move_list += self.potential_slide(cord)
        if accurate:
            # add swing
            self.potential_move_list += self.potential_swing(cord, game)
        # remove repetition
        self.potential_move_list = list(set(self.potential_move_list))
        if cord in self.potential_move_list:
            self.potential_move_list.remove(cord)
        # remove out of bound
        self.remove_out_bound()
        # remove step on block
        self.remove_on_block(game)
        # remove killed by enemy
        self.remove_enemy_kill(game)
        if accurate:
            # remove killed by friendly
            self.remove_friendly_fire(game)

    # select a random valid position to move
    def random_move(self, game):
        self.potential_move(True, self.cord, game)
        if len(self.potential_move_list) == 0:
            # dead end
            return -1
        else:
            move = random.choice(self.potential_move_list)
            game.next_move_dict[self] = move
            return 1

    # find the path through A* algorithm
    def next_move(self, game):
        path = []
        budget = 12
        pq = PriorityQueue()
        node = self.cord

        self.potential_move(True, node, game)
        for move in self.potential_move_list:
            new_path = [move]
            priority = 1 + dist_to(move, self.target)
            pq.put((priority, new_path))

        while not pq.empty():
            path = pq.get()[1]
            if len(path) > budget:
                # over budget may be a useless token
                return self.random_move(game)
            node = path[-1]
            if node == self.target.cord:
                # found
                game.next_move_dict[self] = path[0]
                return 0
            self.potential_move(False, node, game)
            for move in self.potential_move_list:
                new_path = path.copy()
                new_path.append(move)
                priority = len(new_path) + dist_to(move, self.target)
                pq.put((priority, new_path))
        # dead end
        return -1

    def act(self, game):
        if not self.active:
            return 0
        if self.useless:
            return self.random_move(game)
        else:
            return self.next_move(game)


class Enemy(Token):
    player = 'lower'

    def __init__(self, symbol, cord):
        super().__init__(symbol, cord)


class Block(Token):
    player = 'block'

    def __init__(self, cord):
        super().__init__('', cord)
