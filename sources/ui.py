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
        self.frame = pygame.image.load('sources/images/buttons/menu1.png')
        self.selected_frame = pygame.image.load('sources/images/buttons/menu2.png')

        # back buttons
        self.back_button = pygame.image.load('sources/images/buttons/back1.png')
        self.selected_back_button = pygame.image.load('sources/images/buttons/back2.png')
        self.back_played = False

        # music buttons
        self.music_play = True
        self.music_button = pygame.image.load('sources/images/buttons/music1.png')
        self.selected_music_button = pygame.image.load('sources/images/buttons/music2.png')

        # music buttons
        self.rules_button = pygame.image.load('sources/images/buttons/rules1.png')
        self.selected_rules_button = pygame.image.load('sources/images/buttons/rules2.png')

        # buttons frames and texts
        frame1_rect = pygame.Rect((10, SETTINGS['window_size'][1] / 2 - 100), self.frame.get_size())
        frame2_rect = pygame.Rect((10, SETTINGS['window_size'][1] / 2 + 38), self.frame.get_size())
        frame3_rect = pygame.Rect((10, SETTINGS['window_size'][1] / 2 + 176), self.frame.get_size())
        frame4_rect = pygame.Rect((10, SETTINGS['window_size'][1] / 2 - 100), self.frame.get_size())
        frame5_rect = pygame.Rect((10, SETTINGS['window_size'][1] / 2 + 38), self.frame.get_size())
        self.music_rect = pygame.Rect((747, 3), self.music_button.get_size())
        self.back_rect = pygame.Rect((10, 10), self.music_button.get_size())
        self.rules_rect = pygame.Rect((747, 56), self.rules_button.get_size())
        self.frame1_text = Text(85, 'Singleplayer', (225, 225, 170), (28, SETTINGS['window_size'][1] / 2 - 94))
        self.frame2_text = Text(85, 'Multiplayer', (225, 225, 170), (44, SETTINGS['window_size'][1] / 2 + 44))
        self.frame3_text = Text(85, 'Exit', (225, 225, 170), (120, SETTINGS['window_size'][1] / 2 + 184))
        self.frame4_text = Text(85, 'Create', (225, 225, 170), (90, SETTINGS['window_size'][1] / 2 - 91))
        self.frame5_text = Text(85, 'Connect', (225, 225, 170), (77, SETTINGS['window_size'][1] / 2 + 47))
        self.ip_text = Text(85, 'Enter IP:', (100, 100, 225), (10, SETTINGS['window_size'][1] / 2 - 140))
        self.line = Text(85, '_______________', (100, 100, 225), (10, SETTINGS['window_size'][1] / 2 - 70))
        self.curr_char = 0

        # rects
        self.frame_rects = [frame1_rect, frame2_rect, frame3_rect, self.rules_rect, frame4_rect, frame5_rect, frame5_rect]
        self.buttons = [self.frame, self.frame, self.frame, self.rules_button, self.frame, self.frame, self.frame]
        self.selected_buttons = [self.selected_frame, self.selected_frame, self.selected_frame, self.selected_rules_button, self.selected_frame, self.selected_frame, self.selected_frame]

        # menu tick sound
        pygame.init()
        self.played = -1
        self.tick_sound = pygame.mixer.Sound('sources/sounds/menu_tick.wav')

        self.mouse = (0, 0)


    def update(self, event):
        self.mouse = pygame.mouse.get_pos()
        
        if GAME_STATE[0] == MENU:
            # single game click
            if event.type == pygame.MOUSEBUTTONUP and self.frame_rects[0].collidepoint(self.mouse):
                if event.button == 1:
                    return PLACEMENT_SINGLEPLAYER
            # exit click
            if event.type == pygame.MOUSEBUTTONUP and self.frame_rects[2].collidepoint(self.mouse):
                if event.button == 1:
                    pygame.event.post(pygame.event.Event((pygame.USEREVENT + 2)))
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
            # multiplayer click    
            if event.type == pygame.MOUSEBUTTONUP and self.frame_rects[1].collidepoint(self.mouse):
                if event.button == 1:
                    return MULTIPLAYER_SELECT
                    
        elif GAME_STATE[0] in [PLACEMENT_SINGLEPLAYER, SINGLEPLAYER, WIN, LOSE, MULTIPLAYER_SELECT, SERVER_PLACEMENT, CONNECT, WAITING, CLIENT_PLACEMENT, SERVER_MULTIPLAYER, CLIENT_MULTIPLAYER]:
            # back button click
            if event.type == pygame.MOUSEBUTTONUP and self.back_rect.collidepoint(self.mouse):
                if event.button == 1:
                    return MENU
        
        if GAME_STATE[0] == MULTIPLAYER_SELECT:
            # create click    
            if event.type == pygame.MOUSEBUTTONUP and self.frame_rects[4].collidepoint(self.mouse):
                if event.button == 1:
                    return SERVER_PLACEMENT
            # connnect click    
            if event.type == pygame.MOUSEBUTTONUP and self.frame_rects[5].collidepoint(self.mouse):
                if event.button == 1:
                    return CLIENT_PLACEMENT
        
        if GAME_STATE[0] == CONNECT:
            # ip text box
            if event.type == pygame.KEYDOWN:
                char = event.unicode
                new_text = list(self.line.text)
                
                if event.key == pygame.K_BACKSPACE and self.curr_char >= 0:
                    if self.curr_char != 0:
                        self.curr_char -= 1
                    new_text[self.curr_char] = '_'
                elif (char.isdigit() or (char == '.' and new_text[self.curr_char - 1].isdigit() and new_text.count('.') < 3)) and self.curr_char < 15:
                    new_text[self.curr_char] = event.unicode
                    self.curr_char += 1
                
                self.line.text = ''.join(new_text)
            
            # connect click
            if event.type == pygame.MOUSEBUTTONUP and self.frame_rects[6].collidepoint(self.mouse):
                if event.button == 1 and self.line.text.count('.') == 3 and self.line.text[self.curr_char - 1] != '.':
                    return CONNECTED

        return GAME_STATE[0]


    def draw(self):
        self.mouse = pygame.mouse.get_pos()

        # menu draw
        if GAME_STATE[0] in [MENU, MULTIPLAYER_SELECT, CONNECT]:
            not_selected = 0

            if GAME_STATE[0] == MENU:
                self.title_string.draw(self.window)
                first = 0
                buttons_count = 4
            elif GAME_STATE[0] == MULTIPLAYER_SELECT:
                first = 4
                buttons_count = 2
            else:
                first = 6
                buttons_count = 1

            for i in range(first, first + buttons_count):
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

            # music button draw
            if GAME_STATE[0] == MENU:
                if self.music_play:
                    self.window.blit(self.selected_music_button, self.music_rect)
                else:
                    self.window.blit(self.music_button, self.music_rect)

                self.frame1_text.draw(self.window)
                self.frame2_text.draw(self.window)
                self.frame3_text.draw(self.window)
            elif GAME_STATE[0] == MULTIPLAYER_SELECT:
                self.frame4_text.draw(self.window)
                self.frame5_text.draw(self.window)
            else:
                self.frame5_text.draw(self.window)
                self.ip_text.draw(self.window)
                self.line.draw(self.window)
            

        # back button draw
        if GAME_STATE[0] in [PLACEMENT_SINGLEPLAYER, SINGLEPLAYER, WIN, LOSE, MULTIPLAYER_SELECT, SERVER_PLACEMENT, CONNECT, WAITING, CLIENT_PLACEMENT, SERVER_MULTIPLAYER, CLIENT_MULTIPLAYER]:
            if self.back_rect.collidepoint(self.mouse):
                self.window.blit(self.selected_back_button, self.back_rect)
                if not self.back_played:
                    self.tick_sound.play()
                    self.back_played = True
            else:
                self.window.blit(self.back_button, self.back_rect)
                self.back_played = False


    def load_string(self):
        load_string = Text(100, "Loading...", WHITE, (SETTINGS['window_size'][0] / 2 - 110, SETTINGS['window_size'][1] / 2 - 60))
        load_string.draw(self.window)
        pygame.display.update()