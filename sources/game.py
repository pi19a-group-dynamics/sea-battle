import os
import pygame
from sources.globals import *


class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption('Sea battle')
        self.clock = pygame.time.Clock()


    def update(self):
        pass

    
    def render(self):
        self.window.fill((0, 0, 0))
        ''' draw '''
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