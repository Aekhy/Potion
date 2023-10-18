import pygame
from utils.settings import DEFAULT_CASE_SIZE, DEFAULT_CASE_COLOR, DEFAULT_CASE_TYPE
class Case(pygame.sprite.Sprite):
    def __init__(self, x, y, path="", size=DEFAULT_CASE_SIZE, color=DEFAULT_CASE_COLOR):
        super().__init__()
        if path == "":
            self.image = pygame.Surface((size,size))
            self.image.fill(color)
        else:
            self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.type = DEFAULT_CASE_TYPE