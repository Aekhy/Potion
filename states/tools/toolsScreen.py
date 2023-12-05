from states.state import State
from general_settings.private_settings import *
from inventory.drag_and_drop import DragAndDrop
from states.nav import Nav
from tools.tools import Freezer, Alembic

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
        self._drag_and_drop = DragAndDrop(self.sprites, self.update_drag_and_drop)

        self.nav_menu = Nav(0, 0*50, 64, self.sprites, 0, ["Chaudron en cours d'utilisation"])
        
        # Tools
        self.freezer = Freezer(self,TILE_SIZE*8,TILE_SIZE*2)
        self.alembic = Alembic(self,TILE_SIZE*10,TILE_SIZE*2) 


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
                if self.alembic.finish_button.rect.collidepoint(event.pos):
                    self.alembic.apply_effect()
                elif self.freezer.finish_button.rect.collidepoint(event.pos):
                    self.freezer.apply_effect()
                else:
                    authorized_slots_take = self._game.game_inventory.slots["take"]+self.slots["take"]
                    iterable_slots_take = self.game.game_inventory.get_slot_list()
                    self._drag_and_drop.take(authorized_slots_take, iterable_slots_take, event)
                      
            elif event.type == pyg.MOUSEBUTTONUP:  
                itemAdded = [False]
                # if we dropped in the cauldron sprite   
               
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
