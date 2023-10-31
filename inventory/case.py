import pygame
from .settings import CASE_COLOR_DEFAULT, CASE_SIZE_DEFAULT
class Case(pygame.sprite.Sprite):
    def __init__(self, group, x, y, layer, path="", size=CASE_SIZE_DEFAULT, color=CASE_COLOR_DEFAULT):
        self._layer = layer
        if path == "":
            self.image = pygame.Surface((size,size))
            self.image.fill(color)
        else:
            self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.type = 'Slot'
        pygame.sprite.Sprite.__init__(self, group)