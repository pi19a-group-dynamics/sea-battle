import pygame


class Field:
    def __init__(self, offset):
        self.offset = offset

        self.field_image = pygame.image.load('sources/images/field.png')
        self.hit = pygame.image.load('sources/images/hit.png')
        self.ships = [pygame.image.load(f'sources/images/ships/{i}.png') for i in range(1, 5)]
        self.select_image = pygame.image.load('sources/images/select.png')
        
        self.field = [[0 for i in range(12)] for i in range(12)]
        self.ships_count = 0
        self.x_cell = 0
        self.y_cell = 0
    

    def update(self):
        m_x, m_y = pygame.mouse.get_pos()
        self.x_cell = (-self.offset[0] + m_x + m_x // 32 % 11) // 32
        self.y_cell = (-self.offset[1] + m_y + m_y // 32 % 11) // 32

        if pygame.mouse.get_pressed()[0]:
            self.ships_count = 0
            for a in range(11):
                for b in range(11):
                    self.ships_count += self.field[a][b]

            if 0 < self.x_cell <= 11 and 0 < self.y_cell <= 11 and self.ships_count < 20:
                self.field[self.x_cell][self.y_cell] = 1


    def draw(self, window):
        window.blit(self.field_image, self.offset)
        
        for i in range(11):
            for j in range(11):
                if self.field[i][j] == 1:
                    window.blit(self.ships[0], (self.offset[0] + i * 32 - i, self.offset[1] + j * 32 - j))
        
        if 0 < self.x_cell < 11 and 0 < self.y_cell < 11: 
            window.blit(self.select_image, (self.offset[0] + self.x_cell * 32 - self.x_cell, 
                                            self.offset[1] + self.y_cell * 32 - self.y_cell))
        
        #for i in self.ships:
            #window.blit(i, (0, 0))
