import pygame as pyg
from .settings import *

class PopUp(pyg.sprite.Sprite):
    def __init__(self, spritesGroup, text:str):
        self._group = spritesGroup
        self._text = text
        
        self._width, self._height = POPUP_SIZE
        self._height = POPUP_HEIGHT

        self._rect = self._image.get_rect()
        self._rect.x = self._x
        self._rect.y = self._y
        
        self.button = 

    
    # GETTERS
    @property
    def group(self):
        return self._group
    
    def update(self):
        d
        
    def kill():
        self.group
        
        
        