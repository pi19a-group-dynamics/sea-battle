import pygame


class Text:
    def __init__(self, text, color, pos, size):
        pygame.font.init()
        self.size = size
        self.pos = pos
        self.color = color
        self.text = text
        self.font = pygame.font.Font('sources/font/font.otf', self.size)
    

    def draw(self, window):
        self.button = self.font.render(self.text, True, self.color)
        self.button_rect = self.button.get_rect()
        self.button_rect = self.button_rect.move(self.pos)
        window.blit(self.button, self.button_rect)