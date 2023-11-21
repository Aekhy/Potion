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

        self.nav_menu = Nav(0, 0*50, 64, self.sprites, 0, ["Chaudron en cours d'utilisation"])
        
        self._dragged_from_tool = False
        
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
                # if we pressed the finish button, we call the cauldron's finish function
                if self.cauldron.finish_button.rect.collidepoint(event.pos):
                    self.cauldron.finish()
                elif self.cauldron.mixture_slot.rect.collidepoint(event.pos):
                    # if we dragged the item from the cauldron's output
                    self._drag_and_drop.take([self.cauldron.mixture_slot], [self.cauldron.mixture_slot], event)
                    newIndex = 2 if self._drag_and_drop.item.isPotion else 1
                    self.game.game_inventory.change_nav_index(newIndex)
                    # we open the right nav index so we don't have to do it manually
                    
            elif event.type == pyg.MOUSEBUTTONUP:  
                itemAdded = [False]
                # if we dropped in the cauldron sprite   
                if self.cauldron.rect.collidepoint(event.pos):
                    self._dragged_from_tool = True
                    # we add the item into the cauldron's attributes
                    itemAdded = self.cauldron.add_thing(self._drag_and_drop.item, self._drag_and_drop._quantity)
                    # if the item was added, we update to the new quantity
                    if itemAdded[0]:
                        self._drag_and_drop.quantity = itemAdded[2]
                if not itemAdded[0]:
                    fct = None if self._dragged_from_tool else self.cauldron.reset
                    self._drag_and_drop.drop(self._game.game_inventory.slots["add"]+self.slots["add"], self._game.game_inventory.get_slot_list(), event, fct)

            elif event.type == pyg.KEYDOWN:
                match event.key:
                    case pyg.K_ESCAPE:
                        self.game.game_inventory.close()
                        self.exit_state()
                    case pyg.K_TAB:
                        self.game.game_inventory.close()
                        self.game.states("InventoryMenu").enter_state()
                    case pyg.K_i:
                        pass # it's okay, the inventory toogle itself
                    case pyg.K_o:
                        self.game.states("Options").enter_state()
                    case _:
                        print("Oulala cette touche va pas")
                        
            self.game.game_inventory.update(event, self._drag_and_drop.is_holding())
                
    def update(self):
        # DEV
        # go see comments in states.py
        if not self._in_state:
            self._in_state = True
            self.game.game_inventory.set_state(self)
            self._game.game_inventory.open()


        self.sprites.update()

    def draw(self,surface):
        self.sprites.draw(surface)
