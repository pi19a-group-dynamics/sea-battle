import pygame


class Text:
    def __init__(self, font_size, text='', color=(0, 0, 0), pos=(0, 0)):
        pygame.font.init()
        self.font = pygame.font.Font('sources/font/font.otf', font_size)
        self.pos = pos
        self.color = color
        self.text = text
    

    def draw(self, window):
        self.button = self.font.render(self.text, True, self.color)
        self.button_rect = self.button.get_rect()
        self.button_rect = self.button_rect.move(self.pos)
        window.blit(self.button, self.button_rect)
    

    def dynamic_draw(self, window, pos, text, color):
        self.button = self.font.render(text, True, color)
        self.button_rect = self.button.get_rect()
        self.button_rect = self.button_rect.move(pos)
        window.blit(self.button, self.button_rect)