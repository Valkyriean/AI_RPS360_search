class Token:
    def __init__(self, symbol, cord):
        self.symbol = symbol
        self.cord = cord
        self.active = True


class Friendly(Token):
    player = 'upper'

    def __init__(self, symbol, cord):
        super().__init__(symbol, cord)
        self.path = [cord]

    def can_defeat(self, enemy):
        our = self.symbol
        tar = enemy.symbol
        if (our == "p" and tar == "r") or (our == 'r' and tar == 's') or (our == 's' and tar == 'p'):
            return 1
        elif our == tar:
            return 0
        else:
            return -1
    
class Enemy(Token):
    player = 'lower'
    def __init__(self, symbol, cord):
        super().__init__(symbol, cord)

class Block(Token):
    player = 'block'
    def __init__(self, cord):
        super().__init__('', cord)


# TODO finish class and apply

a = Friendly('r', (1,1))
b = Enemy('p', (1,0))

print(a.can_defeat(b))