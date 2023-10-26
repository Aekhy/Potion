from config import *
import pygame as pyg

class Cauldron(pyg.sprite.Sprite):
    # Cauldron is a subclass of Sprite
    def __init__(self, game, x, y):

        self.game = game
        self.group = self.game.game_sprites
        pyg.sprite.Sprite.__init__(self, self.group)

        self._layer = LAYERS['cauldron']
        # The cauldron is always on the center of the screen
        self._x = x
        self._y = y
        self._width = CAULDRON_SIZE
        self._height = CAULDRON_SIZE

        self._image = pyg.Surface((self._width, self._height))
        self._image.fill(CAULDRON_COLOR)

        self._rect = self._image.get_rect()
        self._rect.x = self._x # type: ignore
        self._rect.y = self._y # type: ignore

    @property
    def image(self):
        return self._image
    
    @property
    def rect(self):
        return self._rect

    def update(self):
        pass