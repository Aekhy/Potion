from .cauldron import CauldronScreen 
from states.state import State
from utils.texts import TextOutlined
from general_settings.private_settings import *
from inventory.inventory import Inventory
import pygame as pyg

class GameScreen(State):
    # For now, the Game class looks pretty much the same as the title class since the gameplay isnt much different
    def __init__(self, game):
        super().__init__(game)
        self.sprites = pyg.sprite.LayeredUpdates()

        self.cauldron_title = TextOutlined(SCREEN_WIDTH/2, SCREEN_HEIGHT/4, "Chaudron", 1, font_size=50, font_color=COLORS['black'])
        self.cauldron_title.add_to_group(self.sprites)

        self.choice = None
        self.onclick_redirect = {
            0:{"rect": self.cauldron_title.rect}
        }

    
    def events(self):
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                self.game.inGame = False
                
            elif event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for key, value in self.onclick_redirect.items():
                        if value['rect'].collidepoint(event.pos):
                            self.choice = key

            elif event.type == pyg.KEYDOWN:
                match event.key:
                    case pyg.K_o:
                        self.game.states("Options").enter_state()
                    case pyg.K_TAB:
                        self.game.states("InventoryMenu").enter_state()
            
    def update(self):
        if not self._in_state:
            self._in_state = True

        if self.choice is not None:
            if self.choice == 0:
                self.choice = None
                self.game.states("CauldronScreen").enter_state()
                
            self.choice = None
                
        self.sprites.update()

    def draw(self, surface):
        self.sprites.draw(surface)