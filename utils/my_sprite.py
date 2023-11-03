import pygame


class MySprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, layer, data:dict|None, *groups) -> None:
        super().__init__()
        self._data = data
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.layer = layer

        self.add(*groups)

    def get_data(self):
        return self._data