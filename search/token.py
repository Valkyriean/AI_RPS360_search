import random


class Token:
    def __init__(self, symbol, cord):
        self.symbol = symbol
        self.cord = cord
        self.active = True


class Friendly(Token):
    player = 'upper'
    move_vector_list = [(0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0)]

    def __init__(self, symbol, cord):
        super().__init__(symbol, cord)
        self.path = [cord]
        self.target = None
        self.five = False
        self.potential_move_list = []
        self.future_cord = None

    def can_defeat(self, enemy):
        our = self.symbol
        tar = enemy.symbol
        if (our == "p" and tar == "r") or (our == 'r' and tar == 's') or (our == 's' and tar == 'p'):
            return 1
        elif our == tar:
            return 0
        else:
            return -1

    def dist_to(self, enemy):
        (r_o, q_o) = self.cord
        (r_e, q_e) = enemy.cord
        return abs(r_o - r_e) + abs(q_o - q_e)

    def get_next_target(self, game):
        min_dist = None
        nearest_enemy = None
        for enemy in game.enemy_list:
            if enemy.active and self.can_defeat(enemy) == 1:
                dist = self.dist_to(enemy)
                if min_dist == None or dist < min_dist:
                    nearest_enemy = enemy
                    min_dist = dist
        if nearest_enemy == None:
            self.five = True
            self.target = None
        else:
            self.target = nearest_enemy
 

    def potential_slide(self, cord):
        surrounding_list = []
        for move_vector in self.move_vector_list:
            tar = (cord[0] + move_vector[0], cord[1] + move_vector[1])
            surrounding_list.append(tar)
        return surrounding_list


    def potential_swing(self, cord, game):
        surrounding_list = self.potential_slide(cord)
        swing_list = []
        for friendly in game.friendly_list:
            if friendly.cord in surrounding_list:
                swing_list += self.potential_slide(friendly.cord)
        return swing_list

    def remove_out_bound(self):
        for cord in self.potential_move_list.copy():
            if abs(cord[0]) > 4 or abs(cord[1]) > 4 or abs(cord[0]+cord[1]) > 4:
                self.potential_move_list.remove(cord)
    
    def remove_on_block(self, game):
        for block in game.block_list:
            if block.cord in self.potential_move_list:
                self.potential_move_list.remove(block.cord)

    def remove_enemy_kill(self, game):
        for enemy in game.enemy_list:
            hit_enemy = enemy.cord in self.potential_move_list
            killed_by_enemy = self.can_defeat(enemy) == -1
            if enemy.active and hit_enemy and killed_by_enemy:
                self.potential_move_list.remove(enemy.cord)


    def remove_friendly_fire(self, game):
        for friendly, cord in game.next_move_dict.items():
            if self.can_defeat(friendly) != 0 and cord in self.potential_move_list:
                self.potential_move_list.remove(cord)            




    def potential_move(self, cord, game):
        self.potential_move_list = []
        # add slide
        self.potential_move_list += self.potential_slide(cord)
        # add swing
        self.potential_move_list += self.potential_swing(cord, game)
         # remove replic
        self.potential_move_list = list(set(self.potential_move_list))
        if self.cord in self.potential_move_list:
            self.potential_move_list.remove(self.cord)
        # remove out of bound
        self.remove_out_bound()
        # remove step on block
        self.remove_on_block(game)
        # remove killed by enemy
        self.remove_enemy_kill(game)
        # remove killed by friendly
        self.remove_friendly_fire(game)
    

    def potential_future_move(self, cord, game):
        self.potential_move_list = []
        # add slide
        self.potential_move_list += self.potential_slide(cord)
        # remove replic
        self.potential_move_list = list(set(self.potential_move_list))

        # remove out of bound
        self.remove_out_bound()
        # remove step on block
        self.remove_on_block(game)
        # remove killed by enemy
        self.remove_enemy_kill(game)
        # remove killed by friendly

    def random_move(self, game):
        # try kill self first
        self.potential_move(self.cord, game)
        if len(self.potential_move_list) == 0:
            # dead end
            return -1
        else:
            move = random.choice(self.potential_move_list)
            game.next_move_dict[self] = move
        

    def next_move(self, game):
        path = []
        budget = 10
        queue = []
        node = self.cord
        if node == self.target.cord:
            # found
            game.next_move_dict[self] = path[1]
            return 0
        self.potential_move(node, game)

        for move in self.potential_move_list:
                new_path = path.copy()
                new_path.append(move)
                queue.append(new_path)
        while queue:
            path = queue.pop(0)
            if len(path) > budget:

                # over budget may be a five
                self.random_move(game)
                return 1       
            node = path[-1]
            if node == self.target.cord:
                # found
                game.next_move_dict[self] = path[0]
                return 0
            self.potential_future_move(node, game)
            for move in self.potential_move_list:
                new_path = path.copy()
                new_path.append(move)
                queue.append(new_path)
        # dead end
        return -1



    def act(self, game):
        if self.five == True:
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

