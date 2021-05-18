import os
import sys
import pygame
from sources.globals import *
from sources.field import Field
from sources.text import Text
from sources.ui import UI
from sources.bot import Bot


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

        # remove
        # Bot.auto_placement(self.field)
        # Bot.auto_placement(self.field2)
        # self.field.available_ships = ['0' for i in self.field.available_ships]


    def update(self):
        self.backgrounds_update()
            
        if GAME_STATE[0] in [PLACEMENT_SINGLE_GAME, SINGLE_GAME]:
            self.field.update()
            self.field2.update()

    
    def render(self):
        self.window.fill(BLACK)

        # draw background
        self.window.blit(self.backgrounds[self.bg_frame], (0, 0))
        
        if GAME_STATE[0] == WIN:
            self.window.blit(self.end_backgrounds[self.end_frame], (0, 0))
            self.textwin = Text(130, "You won", (0, 0, 255), (260, 260))
            self.textwin.draw(self.window)

        
        if GAME_STATE[0] == LOSE:
            self.window.blit(self.end2_extra, (0, 0))
            self.window.blit(self.end2_backgrounds[self.end2_frame], (144, 156))
            self.textwin = Text(130, "You lost", (0, 225, 150), (260, 430))
            self.textwin.draw(self.window)

        # draw ui
        self.ui.draw()

        if GAME_STATE[0] == SINGLE_GAME:
            # draw header
            if PLAYER_TURN[0]:
                self.header.dynamic_draw(self.window, (320, 3), 'Your turn', WHITE)
            else:
                self.header.dynamic_draw(self.window, (310, 3), 'Enemy turn', WHITE)

            # draw fields
            self.field.draw(self.window)
            self.field2.draw(self.window)

        if GAME_STATE[0] == PLACEMENT_SINGLE_GAME:
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
                sys.exit(0)

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
                if (old_state in [PLACEMENT_SINGLE_GAME, SINGLE_GAME, WIN, LOSE] and GAME_STATE[0] == MENU):
                    self.field.field = [['0' for i in range(12)] for i in range(12)]
                    self.field2.field = [['0' for i in range(12)] for i in range(12)]
                    self.field.available_ships = ['4', '3', '2', '1']
                    self.field.selected_ship = int(self.field.available_ships[3])
                
                # from menu to game
                if (old_state == MENU and GAME_STATE[0] == PLACEMENT_SINGLE_GAME):
                    self.field.hits = [['0' for i in range(12)] for i in range(12)]
                    self.field2.hits = [['0' for i in range(12)] for i in range(12)]
            
            # after ships placement
            if GAME_STATE[0] == PLACEMENT_SINGLE_GAME and all([i == '0' for i in self.field.available_ships]):
                GAME_STATE[0] = SINGLE_GAME
                Bot.auto_placement(self.field2)
                PLAYER_TURN[0] = True
            
            # hit event
            if event.type == pygame.USEREVENT and GAME_STATE[0] == SINGLE_GAME:
                if self.bot.turn():
                    pygame.time.set_timer(pygame.USEREVENT, 2000, True)
                    self.field.hit_sound.play()
                    if self.field.win(self.field2.hits):
                        GAME_STATE[0] = LOSE
                    return
                PLAYER_TURN[0] = True
                self.field.miss_sound.play()


    def backgrounds_update(self):
        if GAME_STATE[0] not in [WIN, LOSE]:
            self.bg_frame += 1
            if self.bg_frame == 122:
                self.bg_frame = 0

        self.end_clock += 1
        if self.end_clock == 2:
            self.end_frame += 1
            if self.end_frame == 101:
                self.end_frame = 0
            self.end_clock = 0

        self.end2_frame += 1
        if self.end2_frame == 84:
            self.end2_frame = 0