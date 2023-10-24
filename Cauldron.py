from config import *
import pygame as pyg

class Cauldron(pyg.sprite.Sprite):
    # Cauldron is a subclass of Sprite
    def __init__(self, game):

        self.game = game
        self.group = self.game.game_sprites
        pyg.sprite.Sprite.__init__(self, self.group)

        self._layer = LAYERS['cauldron']
        # The cauldron is always on the center of the screen
        self._x = SCREEN_WIDTH / 2 - CAULDRON_WIDTH / 2
        self._y = SCREEN_HEIGHT / 2 - CAULDRON_HEIGHT / 2
        self._width = CAULDRON_WIDTH
        self._height = CAULDRON_HEIGHT

        self._image = pyg.Surface((self._width, self._height))
        self._image.fill(CAULDRON_COLOR)

        self._rect = self._image.get_rect()
        self._rect.x = self._x
        self._rect.y = self._y

    @property
    def image(self):
        return self._image
    
    @property
    def rect(self):
        return self._rect

    def update(self):
        pass