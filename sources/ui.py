import pygame
import webbrowser
from sources.globals import *
from sources.text import Text


class UI:
    def __init__(self, window):
        # window and load string
        self.window = window
        self.load_string()
        self.title_string = Text(150, "Sea Battle", (133, 44, 250), (10, 0))

        # frames buttons
        self.frame = pygame.image.load('sources/images/frames/menu_frame1.png')
        self.selected_frame = pygame.image.load('sources/images/frames/menu_frame2.png')

        # back buttons
        self.back_button = pygame.image.load('sources/images/back_button1.png')
        self.selected_back_button = pygame.image.load('sources/images/back_button2.png')

        # music buttons
        self.music_play = True
        self.music_button = pygame.image.load('sources/images/music_button1.png')
        self.selected_music_button = pygame.image.load('sources/images/music_button2.png')

        # music buttons

        self.rules_button = pygame.image.load('sources/images/rules_button1.png')
        self.selected_rules_button = pygame.image.load('sources/images/rules_button2.png')

        # buttons frames and texts
        frame1_rect = pygame.Rect((10, SETTINGS['window_size'][1] / 2), self.frame.get_size())
        frame2_rect = pygame.Rect((10, SETTINGS['window_size'][1] / 2 + 138), self.frame.get_size())
        self.music_rect = pygame.Rect((747, 3), self.music_button.get_size())
        self.back_rect = pygame.Rect((10, 10), self.music_button.get_size())
        self.rules_rect = pygame.Rect((747, 56), self.rules_button.get_size())
        self.frame1_text = Text(85, "Single game", (225, 225, 170), (26, SETTINGS['window_size'][1] / 2 + 8))
        self.frame2_text = Text(85, "Exit", (225, 225, 180), (115, SETTINGS['window_size'][1] / 2 + 150))

        # rects
        self.frame_rects = [frame1_rect, frame2_rect, self.rules_rect]
        self.buttons = [self.frame, self.frame, self.rules_button]
        self.selected_buttons = [self.selected_frame, self.selected_frame, self.selected_rules_button]

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
            # music click
            if event.type == pygame.MOUSEBUTTONUP and self.music_rect.collidepoint(self.mouse):
                if event.button == 1:
                    if self.music_play:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1)
                    self.music_play = not self.music_play  
            # rules click
            if event.type == pygame.MOUSEBUTTONUP and self.rules_rect.collidepoint(self.mouse):
                if event.button == 1:
                    webbrowser.open('https://github.com/pi19a-group-dynamics/sea-battle/wiki/Морской-бой')       
        
        elif GAME_STATE[0] in [PLACEMENT_SINGLE_GAME, SINGLE_GAME]:
            # back button click
            if event.type == pygame.MOUSEBUTTONUP and self.back_rect.collidepoint(self.mouse):
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
                button_rect = self.frame_rects[i]
                button = self.buttons[i]
                selected_button = self.selected_buttons[i]
                if button_rect.collidepoint(self.mouse):
                    self.window.blit(selected_button, button_rect)
                    if self.played != i:
                        self.tick_sound.play()
                        self.played = i
                else:
                    not_selected += 1
                    self.window.blit(button, button_rect)
            
            if not_selected == buttons_count:
                self.played = -1
            
            if self.music_play:
                self.window.blit(self.selected_music_button, self.music_rect)
            else:
                self.window.blit(self.music_button, self.music_rect)

            self.frame1_text.draw(self.window)
            self.frame2_text.draw(self.window)

        # Other
        elif GAME_STATE[0] in [PLACEMENT_SINGLE_GAME, SINGLE_GAME]:
            if self.back_rect.collidepoint(self.mouse):
                self.window.blit(self.selected_back_button, self.back_rect)
                if not self.played:
                    self.tick_sound.play()
                    self.played = True
            else:
                self.window.blit(self.back_button, self.back_rect)
                self.played = False


    def load_string(self):
        load_string = Text(100, "Loading...", WHITE, (SETTINGS['window_size'][0] / 2 - 110, SETTINGS['window_size'][1] / 2 - 60))
        load_string.draw(self.window)
        pygame.display.update()