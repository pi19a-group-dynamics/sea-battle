import os
import pygame
from sources.globals import *
from sources.field import Field


class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption('Sea battle')
        self.clock = pygame.time.Clock()

        self.field = Field((0, 0))
        self.field2 = Field((400, 0))


    def update(self):
        self.field.update()
        self.field2.update()

    
    def render(self):
        self.window.fill((0, 0, 0))
        ''' draw '''
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