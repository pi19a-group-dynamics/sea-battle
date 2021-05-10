import pygame
from pygame.display import update
from sources.globals import *
from sources.text import Text


class UI:
    def __init__(self, window):
        self.window = window
        self.load_string()
        self.title_string = Text(150, "Sea Battle", (133, 44, 250), (10, 0))

        # frames
        self.frame = pygame.image.load('sources/images/frames/menu_frame1.png')
        self.selected_frame = pygame.image.load('sources/images/frames/menu_frame2.png')
        self.frame_rect = self.frame.get_rect()
        self.frame_size = (self.frame_rect.width, self.frame_rect.height)

        # menu buttons
        frame1_rect = pygame.Rect((10, SETTINGS['window_size'][1] / 2), self.frame_size)
        frame2_rect = pygame.Rect((10, SETTINGS['window_size'][1] / 2 + 138), self.frame_size)
        self.frame1_text = Text(85, "Single game", (225, 225, 170), (26, SETTINGS['window_size'][1] / 2 + 8))
        self.frame2_text = Text(85, "Exit", (225, 225, 180), (115, SETTINGS['window_size'][1] / 2 + 150))
        self.frame_rects = [frame1_rect, frame2_rect]

        # back buttons
        self.back_button = pygame.image.load('sources/images/back_button1.png')
        self.selected_back_button = pygame.image.load('sources/images/back_button2.png')

        # menu tick sound
        pygame.init()
        self.played = -1
        self.tick_sound = pygame.mixer.Sound('sources/sound/menu_tick.wav')

        self.mouse = (0, 0)


    def update(self, event):
        self.mouse = pygame.mouse.get_pos()
        
        if GAME_STATE[0] == MENU:
            # single game click
            if event.type == pygame.MOUSEBUTTONUP and self.frame_rects[0].collidepoint(self.mouse):
                if event.button == 1:
                    return PLACEMENT_SINGLE_GAME
            # exit click
            if event.type == pygame.MOUSEBUTTONUP and self.frame_rects[1].collidepoint(self.mouse):
                if event.button == 1:
                    exit()
        
        elif GAME_STATE[0] in [PLACEMENT_SINGLE_GAME, SINGLE_GAME]:
            # back button click
            if event.type == pygame.MOUSEBUTTONUP and self.selected_back_button.get_rect().collidepoint(self.mouse):
                if event.button == 1:
                    return MENU
        
        return GAME_STATE[0]


    def draw(self):
        self.mouse = pygame.mouse.get_pos()

        # Menu
        if GAME_STATE[0] == MENU:
            self.title_string.draw(self.window)
            
            not_selected = 0
            buttons_count = len(self.frame_rects)

            for i in range(buttons_count):
                button = self.frame_rects[i]
                if button.collidepoint(self.mouse):
                    self.window.blit(self.selected_frame, button)
                    if self.played != i:
                        self.tick_sound.play()
                        self.played = i
                else:
                    not_selected += 1
                    self.window.blit(self.frame, button)
            
            if not_selected == buttons_count:
                self.played = -1

            self.frame1_text.draw(self.window)
            self.frame2_text.draw(self.window)

        # Other
        elif GAME_STATE[0] in [PLACEMENT_SINGLE_GAME, SINGLE_GAME]:
            if self.back_button.get_rect().collidepoint(self.mouse):
                self.window.blit(self.selected_back_button, (0, 0))
                if not self.played:
                    self.tick_sound.play()
                    self.played = True
                
            else:
                self.window.blit(self.back_button, (0, 0))
                self.played = False


    def load_string(self):
        load_string = Text(100, "Loading...", WHITE, (SETTINGS['window_size'][0] / 2 - 110, SETTINGS['window_size'][1] / 2 - 60))
        load_string.draw(self.window)
        pygame.display.update()