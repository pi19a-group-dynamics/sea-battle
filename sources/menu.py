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
        frame2_rect = pygame.Rect((10, WINDOW_SIZE[1] / 2 + 138), self.frame_size)
        self.frame1_text = Text("Single game", (225, 225, 170), (26, WINDOW_SIZE[1] / 2 + 8), 85)
        self.frame2_text = Text("Exit", (225, 225, 180), (115, WINDOW_SIZE[1] / 2 + 150), 85)
        self.frame_rects = [frame1_rect, frame2_rect]

        # menu tick sound
        pygame.init()
        self.played = -1
        self.tick_sound = pygame.mixer.Sound('sources/sound/menu_tick.wav')

        self.mouse = (0, 0)


    def update(self, event):
        self.mouse = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONUP and self.frame_rects[0].collidepoint(self.mouse):
            if event.button == 1:
                return SINGLE_GAME
        if event.type == pygame.MOUSEBUTTONUP and self.frame_rects[1].collidepoint(self.mouse):
            if event.button == 1:
                exit()
        
        return MENU


    def draw(self, window):
        not_selected = 0
        buttons_count = len(self.frame_rects)

        for i in range(buttons_count):
            button = self.frame_rects[i]
            if button.collidepoint(self.mouse):
                window.blit(self.selected_frame, button)
                if self.played != i:
                    self.tick_sound.play()
                    self.played = i
            else:
                not_selected += 1
                window.blit(self.frame, button)
        
        if not_selected == buttons_count:
            self.played = -1

        self.frame1_text.draw(window)
        self.frame2_text.draw(window)