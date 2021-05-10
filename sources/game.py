import os
import pygame
from sources.globals import *
from sources.field import Field
from sources.text import Text
from sources.ui import UI


class Game:    
    def __init__(self):
        # icon
        self.icon = pygame.image.load('sources/images/icon.jpg')
        pygame.display.set_icon(self.icon)

        # window
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.window = pygame.display.set_mode(SETTINGS['window_size'])
        pygame.display.set_caption('Sea Battle')

        # Game clock
        self.clock = pygame.time.Clock()

        # menu
        self.ui = UI(self.window)
        
        # background
        self.bg_frame = 0
        self.backgrounds = [pygame.image.load(f'sources/images/menu_backgrounds/{i}.png') for i in range(122)]
        self.end_frame = 0
        self.end_clock = 0
        #self.end_backgrounds = [pygame.image.load(f'sources/images/end_backgrounds/{i}.png') for i in range(101)]
        self.end2_frame = 0
        #self.end2_backgrounds = [pygame.image.load(f'sources/images/end2_backgrounds/{i}.png') for i in range(84)]

        # curtain for enemy field
        self.curtain = pygame.image.load('sources/images/curtain.png')

        # pick frame
        self.pick_frame = pygame.image.load('sources/images/frames/pick_frame.png')

        # music
        pygame.mixer.music.load('sources/sound/theme.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        
        # fields
        self.field = Field((38, 129))
        self.field2 = Field((418, 129))

        # available ships
        self.avsh_text = Text(48)
        self.avsh_pos = [(330, 535), (330, 485), (190, 535), (190, 485)]


    def update(self):
        self.backgrounds_update()
            
        if GAME_STATE[0] == PLACEMENT_SINGLE_GAME:
            self.field.update(is_player_field=True)
            self.field2.update()

    
    def render(self):
        self.window.fill(BLACK)

        # draw background
        self.window.blit(self.backgrounds[self.bg_frame], (0, 0))
        #self.window.blit(self.end_backgrounds[self.end_frame], (0, 0))
        #self.window.blit(self.end2_backgrounds[self.end2_frame], (0, 0))

        # draw ui
        self.ui.draw()

        if GAME_STATE[0] == PLACEMENT_SINGLE_GAME:
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
                exit()

            old_state = GAME_STATE[0]
            GAME_STATE[0] = self.ui.update(event)
            
            if (old_state != GAME_STATE[0]):
                # from placement to menu
                if (old_state == PLACEMENT_SINGLE_GAME and GAME_STATE[0] == MENU):
                    self.field.field = [['0' for i in range(12)] for i in range(12)]
                    self.field.available_ships = ['4', '3', '2', '1']
                    self.field.selected_ship = int(self.field.available_ships[3])
    

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
        if self.end2_frame == 84 and GAME_STATE[0] == LOSE:
            self.end2_frame = 0