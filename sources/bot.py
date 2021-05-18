import random


class Bot:
    def __init__(self, field):
        self.field = field
        self.last_hit = ()
    

    def turn(self):
        if self.last_hit:
            x = self.last_hit[0]
            y = self.last_hit[1]
            if self.available(x - 1, y):
                x -= 1
            elif self.available(x, y - 1):
                y -= 1
            elif self.available(x + 1, y):
                x += 1
            elif self.available(x, y + 1):
                y += 1
            if (x, y) != self.last_hit:
                self.field.hit(x, y)
                if self.damage(x, y):
                    self.last_hit = (x, y)
                return self.damage(x, y)

        hited = False
        while not hited:
            x, y = random.randint(1, 10), random.randint(1, 10)
            hited = self.field.hit(x, y)
            if self.damage(x, y):
                self.last_hit = (x, y)
        
        return self.damage(x, y)


    def damage(self, x, y):
        return self.field.hits[x][y] in ['1', '3'] or len(self.field.hits[x][y]) == 2


    def available(self, x, y):
        return 0 < x < 11 and 0 < y < 11 and self.field.hits[x][y] == '0'


    @staticmethod
    def auto_placement(field):
        field.field = [['0' for i in range(12)] for i in range(12)]
        
        def place(ship):
            seted = False
            while not seted:
                dir = random.choice(['r', 'd'])
                x, y = random.randint(1, 10), random.randint(1, 10)
                seted = field.set_ship(x, y, ship + dir)
        
        place('4')
        [place('3') for _ in range(2)]
        [place('2') for _ in range(3)]
        [place('1') for _ in range(4)]
