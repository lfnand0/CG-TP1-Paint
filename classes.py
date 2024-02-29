import pygame


class Button:
    def __init__(self, text, pos, size, color, screen):
        self.text = text
        self.pos = pos
        self.size = size
        self.color = color
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.pos, self.size))
        font = pygame.font.SysFont(None, 36)
        text = font.render(self.text, 1, (255, 255, 255))
        self.screen.blit(text, (self.pos[0] + 10, self.pos[1] + 10))
