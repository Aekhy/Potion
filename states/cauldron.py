from states.state import State
from tools.tools import Cauldron
from general_settings.private_settings import SCREEN_WIDTH
from inventory.drag_and_drop import DragAndDrop
from inventory.game_inventory import GameInventory
from states.nav import Nav
import pygame as pyg

class CauldronScreen(State):
    def __init__(self,game):
        super().__init__(game)
        self.sprites = pyg.sprite.LayeredUpdates()
        self.slots = {"take":[],"add":[]}

        self.cauldron = Cauldron(self, self.sprites, SCREEN_WIDTH - 300, 100)
        
        # Very important to do that in each state that use
        # game_inventory. It crashes if not done
        self.game.game_inventory.set_state(self)
        # this open the inventory 
        self.game.game_inventory.open()
        # We don't want to be able to close the game_inventory when we are in here
        self._drag_and_drop = DragAndDrop(self.sprites, self.game.game_inventory.update_slots)

        self.nav_menu = Nav(0, 0*50, 50, self.sprites, 0, ["Chaudron en cours d'utilisation"])

        
    def events(self):
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                self.game.inGame = False
                
            elif event.type == pyg.MOUSEMOTION:
                self._drag_and_drop.move(event)
                self.hover_nav_menu = [False, -1]
                for i in range(0,len(self.nav_menu.tabs)):
                    if self.nav_menu.tabs[i]["space"].rect.collidepoint(event.pos):
                        self.hover_nav_menu = [True, i]
                        break

            elif event.type == pyg.MOUSEBUTTONDOWN:
                self._drag_and_drop.take(self.game.game_inventory.slots["take"]+self.slots["take"], self.game.game_inventory.get_slot_list()+[self.cauldron.mixture_slot], event)
                #If we pressed the finish button, we call the cauldron's finish function
                if self.cauldron.finish_button.rect.collidepoint(event.pos):
                    self.cauldron.finish()
                else:
                    #If we didnt drag the item from the cauldron output
                    if not self._drag_and_drop.take([self.cauldron.mixture_slot], [self.cauldron.mixture_slot], event):
                        #We look for if we're dragging an item from the inventory
                        for i in range(0,len(self.nav_menu.tabs)):
                            if self.nav_menu.tabs[i]["space"].rect.collidepoint(event.pos):
                                self.choice = i
                                break
                    
            elif event.type == pyg.MOUSEBUTTONUP:       
                if self.cauldron.rect.collidepoint(event.pos):
                    itemAdded = self.cauldron.add_thing(self._drag_and_drop.item, self._drag_and_drop._quantity)[0]
                    if itemAdded:
                        self._drag_and_drop.reinit()
                else:
                    self._drag_and_drop.drop(self._game.game_inventory.slots["add"]+self.slots["add"], self._game.game_inventory.get_slot_list(), event, self.cauldron.reset)

            elif event.type == pyg.KEYDOWN:
                match event.key:
                    case pyg.K_ESCAPE:
                        #DEBUG: Cela arrive aussi quand on fait n'importe quelle autre touche, ce bug doit etre du a un probleme de gestion des events avec les autres states
                        self.exit_state()
                    case _:
                        print("Oulala cette touche va pas")
                        
            self.game.game_inventory.update(event, self._drag_and_drop.is_holding())
                
    def update(self):
        self.sprites.update()

    def draw(self,surface):
        self.sprites.draw(surface)
