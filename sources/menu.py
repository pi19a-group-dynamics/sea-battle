import pygame
from sources.globals import *
from sources.text import Text


class Menu:
    def __init__(self):
        # frames
        self.frame = pygame.image.load('sources/images/frames/menu_frame1.png')
        self.selected_frame = pygame.image.load('sources/images/frames/menu_frame2.png')
        self.frame_rect = self.frame.get_rect()
        self.frame_size = (self.frame_rect.width, self.frame_rect.height)

        # menu buttons
        frame1_rect = pygame.Rect((10, WINDOW_SIZE[1] / 2), self.frame_size)
        frame2_rect = pygame.Rect((10, WINDOW_SIZE[1] / 2 + 108), self.frame_size)
        self.frame1_text = Text("Start game", WHITE, (45, WINDOW_SIZE[1] / 2 + 10), 80)
        self.frame2_text = Text("Exit", WHITE, (115, WINDOW_SIZE[1] / 2 + 120), 80)
        self.frame_rects = [frame1_rect, frame2_rect]
        self.mouse = (0, 0)


    def update(self, event):
        self.mouse = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONUP and self.frame_rects[0].collidepoint(self.mouse):
            if event.button == 1:
                return 'start'
        if event.type == pygame.MOUSEBUTTONUP and self.frame_rects[1].collidepoint(self.mouse):
            if event.button == 1:
                exit()
        
        return 'menu'


    def draw(self, window):
        for rect in self.frame_rects:
            if rect.collidepoint(self.mouse):
                window.blit(self.selected_frame, rect)
            else:
                window.blit(self.frame, rect)

        self.frame1_text.draw(window)
        self.frame2_text.draw(window)