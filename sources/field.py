import pygame


class Field:
    def __init__(self, offset):
        self.offset = offset
        self.field_image = pygame.image.load('sources/images/field.png')
        self.ships = [pygame.image.load(f'sources/images/ships/{i}.png') for i in range(1, 5)]
        self.pick_ships = [pygame.image.load(f'sources/images/ships/pick{i}.png') for i in range(1, 5)]
        self.select_image = pygame.image.load('sources/images/select.png')
        
        self.field = [['0' for i in range(12)] for i in range(12)]
        self.available_ships = ['4', '3', '2', '1']
        self.selected_ship = int(self.available_ships[3])
        
        self.pick_ships_rect = [pygame.Rect(250, 542, 32, 32),
                                pygame.Rect(250, 494, 63, 32),
                                pygame.Rect(52, 542, 94, 32),
                                pygame.Rect(52, 494, 125, 32)]
        
        self.ships_count = 0
        self.x_cell = 0
        self.y_cell = 0
    

    def set_ship(self, x, y, ship, recover=False):
        ship_len = int(ship[0])
        right = True if (ship[1] == 'r') else False 

        if not recover:
            for i in range(ship_len):
                try:
                    if right and (self.field[x + i][y] != '0' or x + i == 11): return False
                    if not right and (self.field[x][y + i] != '0' or y + i == 11): return False
                except: return False

        if self.field[x][y] == '0' or recover:
            for i in range(1, ship_len):
                if right: self.field[x + i][y] = '#'
                else: self.field[x][y + i] = '#'
            
            for i in range(ship_len):
                if right:
                    self.field[x + i][y - 1] = '*'
                    self.field[x + i][y + 1] = '*'
                else:
                    self.field[x - 1][y + i] = '*'
                    self.field[x + 1][y + i] = '*'
            
            if right:
                self.field[x - 1][y - 1] = '*'
                self.field[x - 1][y] = '*'
                self.field[x - 1][y + 1] = '*'
                self.field[x + ship_len][y - 1] = '*'
                self.field[x + ship_len][y] = '*'
                self.field[x + ship_len][y + 1] = '*'
            else:
                self.field[x - 1][y - 1] = '*'
                self.field[x][y - 1] = '*'
                self.field[x + 1][y - 1] = '*'
                self.field[x - 1][y + ship_len] = '*'
                self.field[x][y + ship_len] = '*'
                self.field[x + 1][y + ship_len] = '*'
            
            self.field[x][y] = ship
            return True


    def del_ship(self, x, y):
        if self.field[x][y] in ['0', '*']:
            return False
        
        if self.field[x][y] == '#':
            i = 0
            j = 0
            dir = 0
            if self.field[x - 1][y] != '*':
                dir = 'l'
            if self.field[x][y - 1] != '*':
                dir = 'u'
            while self.field[x - i][y - j] == '#':
                if dir == 'l':
                    i += 1
                else:
                    j += 1
            x -= i
            y -= j

        count = int(self.field[x][y][0]) + 2
        self.inc_available_ships(count - 2)
        self.field[x][y] = '0'
        
        for i in range(len(self.field)):
            for j in range(len(self.field[0])):
                if self.field[i][j] in ['*', '#']:
                    self.field[i][j] = '0' 

        for i in range(len(self.field)):
            for j in range(len(self.field[0])):
                if len(self.field[i][j]) == 2:
                    self.set_ship(i, j, self.field[i][j], recover=True)


    def mouse_update(self):
        m_x, m_y = pygame.mouse.get_pos()
        self.x_cell = (m_x - self.offset[0] + m_x // 32 % 14) // 32
        self.y_cell = (m_y - self.offset[1] + m_y // 32 % 14) // 32

        mouse_click = pygame.mouse.get_pressed()
        if mouse_click:
            # LMB
            if mouse_click[0]:
                # set ship
                count = int(self.available_ships[self.selected_ship - 1])
                if self.in_field() and self.field[self.x_cell][self.y_cell] == '0' and count > 0:
                    if self.set_ship(self.x_cell, self.y_cell, str(self.selected_ship) + 'r'):
                        self.dec_available_ships(self.selected_ship)
                # choose ship
                for i in range(len(self.pick_ships_rect)):
                    if self.pick_ships_rect[i].collidepoint(m_x, m_y):
                        self.selected_ship = i + 1
            
            # RMB
            if pygame.mouse.get_pressed()[2]:
                if self.in_field():
                    self.del_ship(self.x_cell, self.y_cell)


    def update(self, is_player_field=False):
            if is_player_field:
                self.mouse_update()


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
                except: continue  
                
                ship_img = pygame.transform.rotate(self.ships[ship_type - 1], -90) if right else self.ships[ship_type - 1]
                
                window.blit(ship_img, (self.offset[0] + i * 32 - i, self.offset[1] + j * 32 - j))


    def inc_available_ships(self, i):
        self.available_ships[i - 1] = str(int(self.available_ships[i - 1]) + 1)


    def dec_available_ships(self, i):
        self.available_ships[i - 1] = str(int(self.available_ships[i - 1]) - 1)


    def in_field(self):
        return 0 < self.x_cell < 11 and 0 < self.y_cell < 11
