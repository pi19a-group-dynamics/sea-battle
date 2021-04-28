import os
import pygame
from sources.globals import *
from sources.field import Field
from sources.text import Text
from sources.menu import Menu


class Game:
    def __init__(self):
        # window
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption('Sea Battle')

        self.clock = pygame.time.Clock()

        self.load_string()
        self.title_string = Text("Sea Battle", (33, 44, 255), (0, 0), 150)
        
        # background
        self.bg_frame = 0
        self.backgrounds = [pygame.image.load(f'sources/images/menu_backgrounds/{i}.png') for i in range(122)]

        # menu
        self.menu = Menu()
        self.current_state = 'menu'

        # fields
        self.field = Field((38, 129))
        self.field2 = Field((418, 129))


    def update(self):
        if self.current_state == 'start':
            self.field.update()
            self.field2.update()

    
    def render(self):
        self.window.fill(BLACK)

        # draw background
        self.window.blit(self.backgrounds[self.bg_frame], (0, 0))

        # draw menu
        if self.current_state == 'menu':
            self.menu.draw(self.window)
            self.title_string.draw(self.window)

        # draw fields
        if self.current_state == 'start':
            self.field.draw(self.window)
            self.field2.draw(self.window)
    
        pygame.display.update()


    def run(self):
        while True:
            self.events()
            self.update()
            self.render()

            self.bg_frame += 1
            if self.bg_frame == 122:
                self.bg_frame = 0

            self.clock.tick(FPS)


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if self.current_state == 'menu':
                self.current_state = self.menu.update(event)
    

    def load_string(self):
        load_string = Text("Loading...", WHITE, (WINDOW_SIZE[0] / 2 - 110, WINDOW_SIZE[1] / 2 - 60), 100)
        load_string.draw(self.window)
        pygame.display.update()