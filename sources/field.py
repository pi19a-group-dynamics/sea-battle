import pygame


class Field:
    def __init__(self, offset):
        self.offset = offset
        self.field_image = pygame.image.load('sources/images/field.png')
        self.ships = [pygame.image.load(f'sources/images/ships/{i}.png') for i in range(1, 5)]
        self.select_image = pygame.image.load('sources/images/select.png')
        
        self.field = [[0 for i in range(11)] for i in range(11)]
        self.ships_count = 0
        self.x_cell = 0
        self.y_cell = 0
    

    def update(self):
        m_x, m_y = pygame.mouse.get_pos()
        self.x_cell = (m_x - self.offset[0] + m_x // 32 % 12) // 32
        self.y_cell = (m_y - self.offset[1] + m_y // 32 % 12) // 32

        mouse_click = pygame.mouse.get_pressed()
        if mouse_click:
            # LMB
            if mouse_click[0]:
                if self.in_field() and self.ships_count < 20:
                    self.field[self.x_cell][self.y_cell] = 1
            
            # RMB
            if pygame.mouse.get_pressed()[2]:
                if self.in_field() and self.field[self.x_cell][self.y_cell] == 1:
                    self.field[self.x_cell][self.y_cell] = 0
            
            # update ships count
            self.ships_count = 0
            for a in range(11):
                for b in range(11):
                    self.ships_count += self.field[a][b]


    def draw(self, window):
        # draw field
        window.blit(self.field_image, self.offset)
        
        # draw ships
        for i in range(11):
            for j in range(11):
                if self.field[i][j] == 1:
                    window.blit(self.ships[0], (self.offset[0] + i * 32 - i, self.offset[1] + j * 32 - j))
        
        # draw select frame
        if self.in_field(): 
            window.blit(self.select_image, (self.offset[0] + self.x_cell * 32 - self.x_cell, 
                                            self.offset[1] + self.y_cell * 32 - self.y_cell))


    def in_field(self):
        return 0 < self.x_cell < 11 and 0 < self.y_cell < 11
