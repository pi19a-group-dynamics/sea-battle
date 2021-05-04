import os
import pygame
from sources.globals import *
from sources.field import Field
from sources.text import Text
from sources.menu import Menu


class Game:
    def __init__(self):
        # icon
        self.icon = pygame.image.load('sources/images/icon.jpg')
        pygame.display.set_icon(self.icon)

        # window
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption('Sea Battle')

        self.clock = pygame.time.Clock()

        self.load_string()
        self.title_string = Text("Sea Battle", (133, 44, 250), (10, 0), 150)
        
        # background
        self.bg_frame = 0
        self.backgrounds = [pygame.image.load(f'sources/images/menu_backgrounds/{i}.png') for i in range(122)]
        self.end_frame = 0
        self.end_clock = 0
        #self.end_backgrounds = [pygame.image.load(f'sources/images/end_backgrounds/{i}.png') for i in range(101)]
        self.end2_frame = 0
        #self.end2_backgrounds = [pygame.image.load(f'sources/images/end2_backgrounds/{i}.png') for i in range(84)]

        # menu
        self.menu = Menu()
        self.state = MENU

        # music
        pygame.mixer.music.load('sources/sound/theme.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        
        # fields
        self.field = Field((38, 129))
        self.field2 = Field((418, 129))


    def update(self):
        self.backgrounds_update()
            
        if self.state == SINGLE_GAME:
            self.field.update()
            self.field2.update()

    
    def render(self):
        self.window.fill(BLACK)

        # draw background
        self.window.blit(self.backgrounds[self.bg_frame], (0, 0))
        #self.window.blit(self.end_backgrounds[self.end_frame], (0, 0))
        #self.window.blit(self.end2_backgrounds[self.end2_frame], (0, 0))

        # draw menu
        if self.state == MENU:
            self.menu.draw(self.window)
            self.title_string.draw(self.window)

        # draw fields
        if self.state == SINGLE_GAME:
            self.field.draw(self.window)
            self.field2.draw(self.window)
    
        pygame.display.update()


    def run(self):
        while True:
            self.events()
            self.update()
            self.render()

            self.clock.tick(FPS)


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if self.state == MENU:
                self.state = self.menu.update(event)
    

    def backgrounds_update(self):
        if self.state == MENU or self.state == SINGLE_GAME:
            self.bg_frame += 1
            if self.bg_frame == 122:
                self.bg_frame = 0

        self.end_clock += 1
        if self.end_clock == 2 :
            self.end_frame += 1
            if self.end_frame == 101:
                self.end_frame = 0
            self.end_clock = 0

        self.end2_frame += 1
        if self.end2_frame == 84 and self.state == LOSE:
            self.end2_frame = 0


    def load_string(self):
        load_string = Text("Loading...", WHITE, (WINDOW_SIZE[0] / 2 - 110, WINDOW_SIZE[1] / 2 - 60), 100)
        load_string.draw(self.window)
        pygame.display.update()