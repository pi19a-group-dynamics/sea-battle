import os
import sys
import pygame
import requests
from sources.globals import *
from sources.field import Field
from sources.text import Text
from sources.ui import UI
from sources.bot import Bot
from sources.server import Server
from sources.client import Client


# for pyinstaller
def my_except_hook(exctype, value, traceback):
    sys.exit(0)
sys.excepthook = my_except_hook


class Game:    
    def __init__(self):
        # icon
        self.icon = pygame.image.load('sources/images/icon.ico')
        pygame.display.set_icon(self.icon)

        # window
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.window = pygame.display.set_mode(SETTINGS['window_size'])
        pygame.display.set_caption('Sea Battle')

        # game clock
        self.clock = pygame.time.Clock()

        # menu
        self.ui = UI(self.window)
        
        # background
        self.bg_frame = 0
        self.backgrounds = [pygame.image.load(f'sources/images/menu_backgrounds/{i}.png') for i in range(122)]
        self.end_frame = 0
        self.end_clock = 0
        self.end_backgrounds = [pygame.image.load(f'sources/images/end_backgrounds/{i}.png') for i in range(101)]
        self.end2_frame = 0
        self.end2_backgrounds = [pygame.image.load(f'sources/images/end2_backgrounds/{i}.png') for i in range(84)]
        self.end2_extra = pygame.image.load('sources/images/end2_backgrounds/00.png')

        # curtain for enemy field
        self.curtain = pygame.image.load('sources/images/fields/curtain.png')

        # pick frame
        self.pick_frame = pygame.image.load('sources/images/ships/pick_frame.png')

        # music
        pygame.mixer.music.load('sources/sounds/theme.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        
        # fields
        self.field = Field((38, 129), is_player_field=True)
        self.field2 = Field((418, 129))

        # available ships
        self.avsh_text = Text(48)
        self.avsh_pos = [(330, 535), (330, 485), (190, 535), (190, 485)]

        # main header
        self.header = Text(64)

        # bot
        self.bot = Bot(self.field)
        self.win = True

        # try to get global ip
        try:
            self.ip = str(requests.get('http://ipinfo.io/json').json()['ip'])
        except:
            self.ip = '127.0.0.1'
        self.server = None
        self.client = None

        self.saved = False


    def update(self):
        self.backgrounds_update()
            
        if GAME_STATE[0] in [PLACEMENT_SINGLEPLAYER, SINGLEPLAYER, CONNECT, CLIENT_PLACEMENT, SERVER_PLACEMENT]:
            self.field.update()
            self.field2.update()

        elif GAME_STATE[0] == CLIENT_MULTIPLAYER:
            self.field.update()
            self.field2.update(client=self.client)
        
        elif GAME_STATE[0] == SERVER_MULTIPLAYER:
            self.field.update()
            self.field2.update(server=self.server)

    
    def render(self):
        self.window.fill(BLACK)

        # draw background
        self.window.blit(self.backgrounds[self.bg_frame], (0, 0))
        
        if GAME_STATE[0] == END_GAME:
            pygame.time.set_timer(pygame.USEREVENT + 1, 5, True)

            # draw fields
            self.field.draw(self.window)
            self.field2.draw(self.window)

        if GAME_STATE[0] == WIN:
            self.window.blit(self.end_backgrounds[self.end_frame], (0, 0))
            
            if not self.saved:
                try:
                    file = open('sources/stats')
                    self.wins, self.defeats = map(int, file.read().split())
                    file.close()
                except:
                    self.wins, self.defeats = 0, 0
                    file = open('sources/stats', 'w')
                    file.write('0 0')
                    file.close()
                
                self.wins += 1

                file = open('sources/stats', 'w')
                file.write(f'{self.wins} {self.defeats}')
                file.close()

                self.saved = True

            self.win_text = Text(130, "You won", (0, 0, 255), (260, 260))
            self.stat1_text = Text(70, "Wins: " + str(self.wins), WHITE, (0, 490))
            self.stat2_text = Text(70, "Defeats: " + str(self.defeats), WHITE, (0, 540))
            self.win_text.draw(self.window)
            self.stat1_text.draw(self.window)
            self.stat2_text.draw(self.window)
        
        if GAME_STATE[0] == LOSE:
            self.window.blit(self.end2_extra, (0, 0))
            self.window.blit(self.end2_backgrounds[self.end2_frame], (144, 156))

            if not self.saved:
                try:
                    file = open('sources/stats')
                    self.wins, self.defeats = map(int, file.read().split())
                    file.close()
                except:
                    self.wins, self.defeats = 0, 0
                    file = open('sources/stats', 'w')
                    file.write('0 0')
                    file.close()
                
                self.defeats += 1

                file = open('sources/stats', 'w')
                file.write(f'{self.wins} {self.defeats}')
                file.close()

                self.saved = True
            
            self.lose_text = Text(130, "You lost", (0, 225, 150), (260, 430))
            self.stat1_text = Text(70, "Wins: " + str(self.wins), WHITE, (0, 490))
            self.stat2_text = Text(70, "Defeats: " + str(self.defeats), WHITE, (0, 540))
            self.lose_text.draw(self.window)
            self.stat1_text.draw(self.window)
            self.stat2_text.draw(self.window)

        # draw ui
        self.ui.draw()

        if GAME_STATE[0] == SINGLEPLAYER:
            # draw header
            if PLAYER_TURN[0]:
                self.header.dynamic_draw(self.window, (320, 3), 'Your turn', WHITE)
            else:
                self.header.dynamic_draw(self.window, (310, 3), 'Enemy turn', WHITE)

            # draw fields
            self.field.draw(self.window)
            self.field2.draw(self.window)
        
        # server multiplayer
        if GAME_STATE[0] == SERVER_MULTIPLAYER:
            PLAYER_TURN[0] = self.server.turn
            # draw header
            if PLAYER_TURN[0]:
                self.header.dynamic_draw(self.window, (320, 3), 'Your turn', WHITE)
            else:
                self.header.dynamic_draw(self.window, (310, 3), 'Enemy turn', WHITE)

            if self.server.shot:
                self.field.hit(self.server.x, self.server.y)
                if self.bot.damage(self.server.x, self.server.y):
                    self.field.hit_sound.play()
                    self.server.turn = False

                    if self.field.win(self.field.hits):
                        GAME_STATE[0] = END_GAME
                        self.win = False
                else:
                    self.field.miss_sound.play()
                    self.server.turn = True
                self.server.shot = False

            # draw fields
            self.field.draw(self.window)
            self.field2.draw(self.window)
        
        # client multiplayer
        if GAME_STATE[0] == CLIENT_MULTIPLAYER:
            PLAYER_TURN[0] = self.client.turn
            # draw header
            if PLAYER_TURN[0]:
                self.header.dynamic_draw(self.window, (320, 3), 'Your turn', WHITE)
            else:
                self.header.dynamic_draw(self.window, (310, 3), 'Enemy turn', WHITE)

            if self.client.shot:
                self.field.hit(self.client.x, self.client.y)
                if self.bot.damage(self.client.x, self.client.y):
                    self.field.hit_sound.play()
                    self.client.turn = False

                    if self.field.win(self.field.hits):
                        GAME_STATE[0] = END_GAME
                        self.win = False
                else:
                    self.field.miss_sound.play()
                    self.client.turn = True
                self.client.shot = False

            # draw fields
            self.field.draw(self.window)
            self.field2.draw(self.window)

        if GAME_STATE[0] == WAITING:
            self.header.dynamic_draw(self.window, (270, 3), self.ip, WHITE)
            self.header.dynamic_draw(self.window, (218, 40), 'Waiting for the player...', WHITE)

            # draw fields
            self.field.draw(self.window)
            self.field2.draw(self.window)

            self.window.blit(self.curtain, (418, 129))

        if GAME_STATE[0] in [PLACEMENT_SINGLEPLAYER, SERVER_PLACEMENT, CLIENT_PLACEMENT]:
            # draw header
            self.header.dynamic_draw(self.window, (270, 3), 'Place your ships', WHITE)

            # draw fields
            self.field.draw(self.window)
            self.field2.draw(self.window)

            self.window.blit(self.curtain, (418, 129))
            self.window.blit(self.pick_frame, (38, 480))
        
            # draw available ships count
            for i in range(len(self.avsh_pos)):
                self.avsh_text.dynamic_draw(self.window, self.avsh_pos[i], 'x' + str(self.field.available_ships[i]), WHITE)
            
            # draw select frame
            current_ship = int(self.field.selected_ship) - 1
            self.window.blit(self.field.pick_ships[current_ship], self.field.pick_ships_rect[current_ship].topleft)
    
        if GAME_STATE[0] == CONNECTED and not self.client.socket:
            GAME_STATE[0] = CONNECT

        pygame.display.update()


    def run(self):
        while True:
            self.events()
            self.update()
            self.render()

            self.clock.tick(SETTINGS['fps'])


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.post(pygame.event.Event((pygame.USEREVENT + 2)))

            # rotate arrow on click
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                rect = pygame.Rect(self.field.offset[0], self.field.offset[1], 32, 32)
                if event.button == 2 or rect.collidepoint(mouse):
                    if self.field.dir == 'r':
                        self.field.dir = 'd'
                    else:
                        self.field.dir = 'r'

            old_state = GAME_STATE[0]
            GAME_STATE[0] = self.ui.update(event)
            
            if (old_state != GAME_STATE[0]):
                # from game, win, lose to menu
                if (old_state in [PLACEMENT_SINGLEPLAYER, SERVER_PLACEMENT, SINGLEPLAYER, WIN, LOSE, WAITING, CLIENT_PLACEMENT, CONNECT, SERVER_MULTIPLAYER, CLIENT_MULTIPLAYER] and GAME_STATE[0] == MENU):
                    self.field.field = [['0' for i in range(12)] for i in range(12)]
                    self.field2.field = [['0' for i in range(12)] for i in range(12)]
                    self.field.available_ships = ['4', '3', '2', '1']
                    self.field.selected_ship = int(self.field.available_ships[3])
                    self.win = True
                    self.saved = False
                    self.close_connections()
                
                # from menu to game
                if (old_state == MENU and GAME_STATE[0] in [PLACEMENT_SINGLEPLAYER, MULTIPLAYER_SELECT]):
                    self.field.hits = [['0' for i in range(12)] for i in range(12)]
                    self.field2.hits = [['0' for i in range(12)] for i in range(12)]
                    self.win = True
                
                # from server multiplayer to menu
                if (old_state in [WAITING, SERVER_MULTIPLAYER] and GAME_STATE[0] == MENU):
                    if self.server.conn:
                        self.server.conn.close()
                    self.server.socket.close()
                
                # from client multiplayer to menu
                if (old_state == CLIENT_MULTIPLAYER and GAME_STATE[0] == MENU):
                    self.client.socket.close()
            
            # after ships placement
            if GAME_STATE[0] == PLACEMENT_SINGLEPLAYER and all([i == '0' for i in self.field.available_ships]):
                GAME_STATE[0] = SINGLEPLAYER
                Bot.auto_placement(self.field2)
                PLAYER_TURN[0] = True
            elif GAME_STATE[0] == SERVER_PLACEMENT and all([i == '0' for i in self.field.available_ships]):
                self.server = Server(self.field.field)
                self.server.start()
                GAME_STATE[0] = WAITING
            elif GAME_STATE[0] == CLIENT_PLACEMENT and all([i == '0' for i in self.field.available_ships]):
                GAME_STATE[0] = CONNECT
            
            # connected to server event
            if GAME_STATE[0] == WAITING and self.server.player_connected:
                self.field2.field = self.server.field
                GAME_STATE[0] = SERVER_MULTIPLAYER

            # connected to client event
            if GAME_STATE[0] == CONNECTED:
                self.client = Client(self.ui.line.text[:self.ui.curr_char], self.field.field)
                if self.client.socket:
                    self.client.start()
                    self.field2.field = self.client.field
                    GAME_STATE[0] = CLIENT_MULTIPLAYER

            # hit event
            if event.type == pygame.USEREVENT:
                if GAME_STATE[0] == SINGLEPLAYER:
                    if self.bot.turn():
                        pygame.time.set_timer(pygame.USEREVENT, 500, True)
                        self.field.hit_sound.play()
                        if self.field.win(self.field2.hits):
                            self.win = False
                            GAME_STATE[0] = END_GAME
                        return
                    PLAYER_TURN[0] = True
                    self.field.miss_sound.play()
            
            # end game event
            if event.type == pygame.USEREVENT + 1 and GAME_STATE[0] == END_GAME:
                if self.win:
                    GAME_STATE[0] = WIN
                else:
                    GAME_STATE[0] = LOSE
            
            # exit event
            if event.type == pygame.USEREVENT + 2:
                self.close_connections()
                sys.exit(0)


    def close_connections(self):
        if self.server:
            self.server.do_run = False
            if self.server.conn:
                self.server.conn.close()
            if self.server.socket:
                self.server.socket.close()
        if self.client:
            self.client.do_run = False
            if self.client.socket:
                self.client.socket.close()


    def backgrounds_update(self):
        if GAME_STATE[0] not in [WIN, LOSE]:
            self.bg_frame += 1
            if self.bg_frame == 122:
                self.bg_frame = 0

        if GAME_STATE[0] == WIN:
            self.end_clock += 1
            if self.end_clock == 2:
                self.end_frame += 1
                if self.end_frame == 101:
                    self.end_frame = 0
                self.end_clock = 0

        if GAME_STATE[0] == LOSE:
            self.end2_frame += 1
            if self.end2_frame == 84:
                self.end2_frame = 0