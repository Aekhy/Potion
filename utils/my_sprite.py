import pygame


class MySprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, layer, *groups) -> None:
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.layer = layer

        self.add(*groups)