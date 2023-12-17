from states.state import State
from general_settings.private_settings import SCREEN_WIDTH
from inventory.drag_and_drop import DragAndDrop
from inventory.game_inventory import GameInventory
from items.recipe import *
from tools.tools import *
from states.nav import Nav
import pygame as pyg

class ToolsScreen(State):
    def __init__(self,game):
        super().__init__(game)
        self.sprites = pyg.sprite.LayeredUpdates()
        self.slots = {"take":[],"add":[]}

        # Very important to do that in each state that use
        # game_inventory. It crashes if not done
        self.game.game_inventory.set_state(self)
        # this open the inventory 
        self.game.game_inventory.open()
        # We don't want to be able to close the game_inventory when we are in here
        self.game.game_inventory.lock()
        # if you give self in draganddrop, self need to have a id attribute
        self.id = "ToolsScreen"
        self._drag_and_drop = DragAndDrop(self.sprites, self.update_drag_and_drop, self)

        self.nav_menu = Nav(0, 0*50, 64, self.sprites, 0, ["Outils"])
        
        self._dragged_from_tool = False

        # tools
        self._heater = Heater(self, 10*TILE_SIZE,2*TILE_SIZE)
        self._freezer = Freezer(self, 12*TILE_SIZE,2*TILE_SIZE)
        self._mortar = Mortar(self, 14*TILE_SIZE,2*TILE_SIZE)
        self._alembic = Alembic(self, 10*TILE_SIZE,6*TILE_SIZE)
        self._sublime = Sublime(self, 12*TILE_SIZE,6*TILE_SIZE)
        self._ferment = Ferment(self, 14*TILE_SIZE,6*TILE_SIZE)


    def update_drag_and_drop(self):
        self.game.game_inventory.update_slots()

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
                if self._heater.finish_button.rect.collidepoint(event.pos):
                    self._heater.apply_effect()
                elif self._freezer.finish_button.rect.collidepoint(event.pos):
                    self._freezer.apply_effect()
                elif self._mortar.finish_button.rect.collidepoint(event.pos):
                    self._mortar.apply_effect()
                elif self._alembic.finish_button.rect.collidepoint(event.pos):
                    self._alembic.apply_effect()
                elif self._sublime.finish_button.rect.collidepoint(event.pos):
                    self._sublime.apply_effect()
                elif self._ferment.finish_button.rect.collidepoint(event.pos):
                    self._ferment.apply_effect()
                else:
                    authorized_slots_take = self._game.game_inventory.slots["take"]+self.slots["take"]
                    iterable_slots_take = self.game.game_inventory.get_slot_list()+self.slots["take"]
                    self._drag_and_drop.take(authorized_slots_take, iterable_slots_take, event)
                    # if we pressed the finish button, we call the cauldron's finish function
                      
            elif event.type == pyg.MOUSEBUTTONUP:  
                itemAdded = [False]
                 
                if not itemAdded[0]:
                    fct = None
                    # self._game.game_inventory.get_slot_list()
                    authorized_slots_add = self._game.game_inventory.slots["add"]+self.slots["add"]
                    iterable_slots_add = self._game.game_inventory.get_slot_list()
                    self._drag_and_drop.drop(authorized_slots_add, iterable_slots_add, event, fct)

            elif event.type == pyg.KEYDOWN:
                match event.key:
                    case pyg.K_ESCAPE:
                        self.game.game_inventory.close()
                        self.exit_state()
                    case pyg.K_TAB:
                        self.game.game_inventory.close()
                        self.game.states("InventoryMenu").enter_state()
                    case pyg.K_o:
                        self.game.states("Options").enter_state()
                    case _:
                        break                        
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
