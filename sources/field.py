from sources.globals import *
import pygame


class Field:
    def __init__(self, offset, is_player_field=False):
        self.offset = offset
        self.field_image = pygame.image.load('sources/images/fields/field.png')
        self.ships = [pygame.image.load(f'sources/images/ships/{i}.png') for i in range(1, 5)]
        self.pick_ships = [pygame.image.load(f'sources/images/ships/pick{i}.png') for i in range(1, 5)]
        self.select_image = pygame.image.load('sources/images/fields/select.png')
        self.hit_image = pygame.image.load('sources/images/fields/hit.png')
        self.miss_image = pygame.image.load('sources/images/fields/miss.png')
        self.arrow_image = pygame.image.load('sources/images/fields/arrow.png')
        
        self.hits = [['0' for i in range(12)] for i in range(12)]
        self.field = [['0' for i in range(12)] for i in range(12)]
        self.available_ships = ['4', '3', '2', '1']
        self.selected_ship = int(self.available_ships[3])
        
        self.pick_ships_rect = [pygame.Rect(250, 542, 32, 32),
                                pygame.Rect(250, 494, 63, 32),
                                pygame.Rect(52, 542, 94, 32),
                                pygame.Rect(52, 494, 125, 32)]
        
        self.is_player_field = is_player_field
        self.ships_count = 0
        self.x_cell = 0
        self.y_cell = 0
        self.dir = 'r'

        # sounds
        self.hit_sound = pygame.mixer.Sound('sources/sounds/hit.mp3')
        self.hit_sound.set_volume(0.5)
        self.miss_sound = pygame.mixer.Sound('sources/sounds/miss.mp3')
        self.miss_sound.set_volume(0.1)
    

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


    def hit(self, x, y):
        if self.hits[x][y] in ['1', '2', '3'] or len(self.hits[x][y]) == 2:
            return False

        if self.field[x][y] in ['0', '*']:
            self.hits[x][y] = '2'
            return True
        
        if len(self.field[x][y]) == 2:
            self.hits[x][y] = self.field[x][y]
        elif self.field[x][y] == '#':
            self.hits[x][y] = '1'
        
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
        
        check_count = 0
        count = int(self.field[x][y][0])
        dir = self.field[x][y][1]

        for i in range(count):
            if dir == 'r':
                if self.hits[x + i][y] == '1' or len(self.hits[x + i][y]) == 2: 
                    check_count += 1
            else:
                if self.hits[x][y + i] == '1' or len(self.hits[x][y + i]) == 2: 
                    check_count += 1
        
        if check_count == count:
            for i in range(count):
                if dir == 'r':
                    self.hits[x + i][y - 1] = '2'
                    self.hits[x + i][y + 1] = '2'
                else:
                    self.hits[x - 1][y + i] = '2'
                    self.hits[x + 1][y + i] = '2'
            
            if dir == 'r':
                self.hits[x - 1][y - 1] = '2'
                self.hits[x - 1][y] = '2'
                self.hits[x - 1][y + 1] = '2'
                self.hits[x + count][y - 1] = '2'
                self.hits[x + count][y] = '2'
                self.hits[x + count][y + 1] = '2'
            else:
                self.hits[x - 1][y - 1] = '2'
                self.hits[x][y - 1] = '2'
                self.hits[x + 1][y - 1] = '2'
                self.hits[x - 1][y + count] = '2'
                self.hits[x][y + count] = '2'
                self.hits[x + 1][y + count] = '2'

            self.hits[x][y] = '3'
        
        return True


    def placement_mouse_update(self):
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
                    if self.set_ship(self.x_cell, self.y_cell, str(self.selected_ship) + self.dir):
                        self.dec_available_ships(self.selected_ship)
                # choose ship
                for i in range(len(self.pick_ships_rect)):
                    if self.pick_ships_rect[i].collidepoint(m_x, m_y):
                        self.selected_ship = i + 1
            
            # RMB
            if mouse_click[2]:
                if self.in_field():
                    self.del_ship(self.x_cell, self.y_cell)


    def singleplayer_hit_mouse_update(self):
        m_x, m_y = pygame.mouse.get_pos()
        self.x_cell = (m_x - self.offset[0] + m_x // 32 % 14) // 32
        self.y_cell = (m_y - self.offset[1] + m_y // 32 % 14) // 32

        mouse_click = pygame.mouse.get_pressed()
        if mouse_click:
            # LMB
            if mouse_click[0] and self.in_field() and PLAYER_TURN[0]:
                if self.hit(self.x_cell, self.y_cell):
                    if self.hits[self.x_cell][self.y_cell] in ['1', '3'] or len(self.hits[self.x_cell][self.y_cell]) == 2:
                        self.hit_sound.play()
                        if self.win(self.hits):
                            GAME_STATE[0] = END_GAME
                        return
                    PLAYER_TURN[0] = False
                    pygame.time.set_timer(pygame.USEREVENT, 2000, True)
                    self.miss_sound.play()


    def multiplayer_hit_mouse_update(self, client=None, server=None):
        m_x, m_y = pygame.mouse.get_pos()
        self.x_cell = (m_x - self.offset[0] + m_x // 32 % 14) // 32
        self.y_cell = (m_y - self.offset[1] + m_y // 32 % 14) // 32

        mouse_click = pygame.mouse.get_pressed()
        if mouse_click:
            # LMB
            if mouse_click[0] and self.in_field() and PLAYER_TURN[0]:
                if self.hit(self.x_cell, self.y_cell):
                    if client:
                        client.do_shot(self.x_cell, self.y_cell)
                    elif server:
                        server.do_shot(self.x_cell, self.y_cell)
                    
                    if self.hits[self.x_cell][self.y_cell] in ['1', '3'] or len(self.hits[self.x_cell][self.y_cell]) == 2:
                        self.hit_sound.play()
                        if self.win(self.hits):
                            GAME_STATE[0] = END_GAME
                        return
                    
                    if client:
                        client.turn = False
                    elif server:
                        server.turn = False
                    
                    self.miss_sound.play()


    def update(self, client=None, server=None):
        if self.is_player_field and GAME_STATE[0] not in [SINGLEPLAYER, SERVER_MULTIPLAYER, CLIENT_MULTIPLAYER]:
            self.placement_mouse_update()

        elif not self.is_player_field and GAME_STATE[0] == SINGLEPLAYER:
            self.singleplayer_hit_mouse_update()
        
        elif not self.is_player_field and GAME_STATE[0] in [SERVER_MULTIPLAYER, CLIENT_MULTIPLAYER]:
            self.multiplayer_hit_mouse_update(client, server)


    def draw(self, window):
        # draw field
        window.blit(self.field_image, self.offset)
        
        # draw arrow
        if self.is_player_field and GAME_STATE[0] not in [SINGLEPLAYER, SERVER_MULTIPLAYER, WAITING, CLIENT_MULTIPLAYER]:
            arrow_pos = (0, 0)
            self.arrow = pygame.transform.rotate(self.arrow_image, 90) if self.dir == 'd' else self.arrow_image
            if self.dir == 'd':
                arrow_pos = (self.offset[0] + 8, self.offset[1] + 2)
            if self.dir == 'r':
                arrow_pos = (self.offset[0] + 2, self.offset[1] + 8)
            window.blit(self.arrow, arrow_pos)

        if GAME_STATE[0] != END_GAME:
            # draw select frame
            if self.in_field():
                window.blit(self.select_image, (self.offset[0] + self.x_cell * 32 - self.x_cell,
                                                self.offset[1] + self.y_cell * 32 - self.y_cell))

        if self.is_player_field or GAME_STATE[0] == END_GAME:
            # draw ships
            for i in range(1, 11):
                for j in range(1, 11):
                    if len(self.field[i][j]) == 2:
                        ship_type = int(self.field[i][j][0])
                        right = True if (self.field[i][j][1] == 'r') else False
                    
                        ship_img = pygame.transform.rotate(self.ships[ship_type - 1], -90) if right else self.ships[ship_type - 1]
                        window.blit(ship_img, (self.offset[0] + i * 32 - i, self.offset[1] + j * 32 - j))

        # draw hits
        for i in range(1, 11):
            for j in range(1, 11):
                if self.hits[i][j] == '1' or len(self.hits[i][j]) == 2:
                    window.blit(self.hit_image, (self.offset[0] + i * 32 - i + 1, self.offset[1] + j * 32 - j + 1))
                elif self.hits[i][j] == '2':
                    window.blit(self.miss_image, (self.offset[0] + i * 32 - i + 1, self.offset[1] + j * 32 - j + 1))
                
                if self.hits[i][j] == '3':
                    ship_type = int(self.field[i][j][0])
                    right = True if (self.field[i][j][1] == 'r') else False
                
                    ship_img = pygame.transform.rotate(self.ships[ship_type - 1], -90) if right else self.ships[ship_type - 1]
                    window.blit(ship_img, (self.offset[0] + i * 32 - i, self.offset[1] + j * 32 - j))
                    window.blit(self.hit_image, (self.offset[0] + i * 32 - i + 1, self.offset[1] + j * 32 - j + 1))


    def win(self, hits):
        ships_count = 0
        for i in range(len(hits)):
            for j in range(len(hits[0])):
                if self.hits[i][j] == '3':
                    ships_count += 1
        return ships_count == 10


    def inc_available_ships(self, i):
        self.available_ships[i - 1] = str(int(self.available_ships[i - 1]) + 1)


    def dec_available_ships(self, i):
        self.available_ships[i - 1] = str(int(self.available_ships[i - 1]) - 1)


    def in_field(self):
        return 0 < self.x_cell < 11 and 0 < self.y_cell < 11
