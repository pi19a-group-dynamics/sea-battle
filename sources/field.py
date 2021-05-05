import pygame


class Field:
    def __init__(self, offset):
        self.offset = offset
        self.field_image = pygame.image.load('sources/images/field.png')
        self.ships = [pygame.image.load(f'sources/images/ships/{i}.png') for i in range(1, 5)]
        self.select_image = pygame.image.load('sources/images/select.png')
        
        self.field = [['0' for i in range(12)] for i in range(12)]
        self.ships_count = 0
        self.x_cell = 0
        self.y_cell = 0
    

    def set_ship(self, ship):
        ship_len = int(ship[0])
        right = True if (ship[1] == 'r') else False 

        for i in range(ship_len):
            try:
                if right and (self.field[self.x_cell + i][self.y_cell] != '0' or self.x_cell + i == 11): return
                if not right and (self.field[self.x_cell][self.y_cell + i] != '0' or self.y_cell + i == 11): return
            except: return

        if self.field[self.x_cell][self.y_cell] == '0':
            for i in range(1, ship_len):
                if right: self.field[self.x_cell + i][self.y_cell] = '#'
                else: self.field[self.x_cell][self.y_cell + i] = '#'
            
            for i in range(ship_len):
                if right:
                    self.field[self.x_cell + i][self.y_cell - 1] = '*'
                    self.field[self.x_cell + i][self.y_cell + 1] = '*'
                else:
                    self.field[self.x_cell - 1][self.y_cell + i] = '*'
                    self.field[self.x_cell + 1][self.y_cell + i] = '*'
            
            if right:
                self.field[self.x_cell - 1][self.y_cell - 1] = '*'
                self.field[self.x_cell - 1][self.y_cell] = '*'
                self.field[self.x_cell - 1][self.y_cell + 1] = '*'
                self.field[self.x_cell + ship_len][self.y_cell - 1] = '*'
                self.field[self.x_cell + ship_len][self.y_cell] = '*'
                self.field[self.x_cell + ship_len][self.y_cell + 1] = '*'
            else:
                self.field[self.x_cell - 1][self.y_cell - 1] = '*'
                self.field[self.x_cell][self.y_cell - 1] = '*'
                self.field[self.x_cell + 1][self.y_cell - 1] = '*'
                self.field[self.x_cell - 1][self.y_cell + ship_len] = '*'
                self.field[self.x_cell][self.y_cell + ship_len] = '*'
                self.field[self.x_cell + 1][self.y_cell + ship_len] = '*'
            
            self.field[self.x_cell][self.y_cell] = ship
            '''print('\n')
            for i in range(len(self.field)):
                for j in range(len(self.field[0])):
                    print(self.field[j][i], end='')
                print()'''


    def mouse_update(self):
        m_x, m_y = pygame.mouse.get_pos()
        self.x_cell = (m_x - self.offset[0] + m_x // 32 % 14) // 32
        self.y_cell = (m_y - self.offset[1] + m_y // 32 % 14) // 32

        mouse_click = pygame.mouse.get_pressed()
        if mouse_click:
            # LMB
            if mouse_click[0]:
                if self.in_field() and self.ships_count < 20:
                    self.set_ship('1r')
            
            # RMB
            if pygame.mouse.get_pressed()[2]:
                if self.in_field() and self.ships_count < 20:
                    self.set_ship('2d')
                #if self.in_field() and self.field[self.x_cell][self.y_cell] == '1':
                #    self.field[self.x_cell][self.y_cell] = '0'


    def update(self):
            self.mouse_update()
            
            # update ships count
            self.ships_count = 0
            for a in range(11):
                for b in range(11):
                    try: self.ships_count += int(self.field[a][b][0])
                    except: pass


    def draw(self, window):
        # draw field
        window.blit(self.field_image, self.offset)
        
        # draw select frame
        if self.in_field(): 
            window.blit(self.select_image, (self.offset[0] + self.x_cell * 32 - self.x_cell, 
                                            self.offset[1] + self.y_cell * 32 - self.y_cell))

        # draw ships
        for i in range(11):
            for j in range(11):
                try: 
                    ship_type = int(self.field[i][j][0])
                    right = True if (self.field[i][j][1] == 'r') else False
                except:
                    continue  
                
                ship_img = pygame.transform.rotate(self.ships[ship_type - 1], 90) if right else self.ships[ship_type - 1]
                
                window.blit(ship_img, (self.offset[0] + i * 32 - i, self.offset[1] + j * 32 - j))


    def in_field(self):
        return 0 < self.x_cell < 11 and 0 < self.y_cell < 11
