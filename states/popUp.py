import pygame as pyg
from states.state import State
from utils.texts import *
from general_settings.private_settings import *

BACKGROUND_COLOR = (255,50,50)
BUTTON_COLOR = (255,100,100)

class PopUp(State):
    def __init__(self, game):
        super().__init__(game)
        
        self.sprites = pyg.sprite.LayeredUpdates()
        self._text = "Défaut"
        self._buttonText = "D'accord"
        dim = (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3)

        # Popup itself
        self.background = pyg.sprite.Sprite(self.sprites)
        self.background.image = pyg.Surface(dim)
        self.background.image.fill(BACKGROUND_COLOR)
        self.background.rect = (dim, dim)
        
        self.spriteText = TextSprite(self._text)
        self.sprites.append(self.spriteText)
      
        # Button
        center = (dim[0]*1.5, dim[1]*2-DEFAULT_FONT_SIZE)  
        self.buttonBackground = pyg.sprite.Sprite(self.sprites)
        self.buttonBackground.image = pyg.Surface(((len(self.buttonText)*DEFAULT_FONT_SIZE)//2, DEFAULT_FONT_SIZE*1.5))
        self.buttonBackground.image.fill(BUTTON_COLOR)
        self.buttonBackground.rect = self.buttonBackground.image.get_rect()
        self.buttonBackground.rect.center = (center[0], center[1])
        
        self.button = TextOutlined(center[0], center[1], self._buttonText, 1)
        self.button.add_to_group(self.sprites)
        
    @property
    def buttonText(self):
        return self._buttonText
    
    @buttonText.setter
    def buttonText(self, text:str):
        self._buttonText = text
        self.button = TextOutlined(dim[0]*1.5, dim[1]*2-DEFAULT_FONT_SIZE, self._buttonText, 1)

    def events(self):
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                self._game.inGame = False
            elif event.type == pyg.MOUSEMOTION:
                if self.buttonBackground.rect.collidepoint(event.pos):
                    self.buttonBackground.image.fill((255 - BUTTON_COLOR[0], 255 - BUTTON_COLOR[1], 255 - BUTTON_COLOR[2]))
                else :
                    self.buttonBackground.image.fill(BUTTON_COLOR)
            elif event.type == pyg.MOUSEBUTTONUP:
                if self.buttonBackground.rect.collidepoint(event.pos):
                    self.exit_state()

    def update(self):
        self.sprites.update()
    
    def draw(self, surface):
        self.sprites.draw(surface)
        