import pygame
from inventory.multiple_inventory import MultipleInventory
from items.potions import Potion, Base, Active
from items.recipe import Paper, SubstanceRecipe, PotionRecipe
from states.nav import Nav
from inventory.slot import Slot
from utils.texts import TextOutlined
from general_settings.private_settings import *

class GameInventory:
    def __init__(self, struct_json, x, y, locked=False) -> None:
        

        self._state = None
        self._slots = {"take":[],"add":[]}
        self._group = pygame.sprite.LayeredUpdates()
        self._struct = struct_json
        self._x = x
        self._y = y
        self._locked = locked

        self._multiple_inventories = {
            0: MultipleInventory(self._struct["ingredients"], self._state, self, 0, self._y, {"black_list":[Potion, Base, Active, Paper, SubstanceRecipe, PotionRecipe],"white_list":None}),
            1: MultipleInventory(self._struct["mixtures"], self._state, self, 0, self._y, {"black_list":None,"white_list":[Base, Active]}),
            2: MultipleInventory(self._struct["potions"], self._state, self, 0, self._y, {"black_list":None,"white_list":[Potion]}),
            3: MultipleInventory(self._struct["recipe"], self._state, self, 0, self._y, {"black_list":None,"white_list":[Paper, SubstanceRecipe, PotionRecipe]})
        }

        self._open = False

        self._trash_slot = None
        self._trash_label = None

        self._nav_group = pygame.sprite.LayeredUpdates()
        self.reset()

    def set_state(self, new_state):
        self._state = new_state
        for key, value in self._multiple_inventories.items():
            value.set_state(self._state)
        
        # trash can
        self.kill_trashcan()
        self.make_trashcan()

    def kill_trashcan(self):
        if self._trash_label is not None:
            self._trash_label.kill()
        if self._trash_slot is not None:
            self._trash_slot.kill()
        
    def make_trashcan(self):
        # trashcan
        height_of_inventory = 7
        trash_slot_x = self._x + 2
        # 1.5 cause 1 is height of top nav bar
        trash_slot_y = height_of_inventory + 1.5
        trash_slot_layer = 0
        self._trash_slot = Slot(self,self._state.sprites,
                                True,True,
                                None,0,
                                trash_slot_x * TILE_SIZE,
                                trash_slot_y * TILE_SIZE,
                                trash_slot_layer)
        self._trash_slot
        # hardcoded 
        trash_label_x = trash_slot_x + 0.5
        trash_label_y = trash_slot_y + 1.25
        trash_label_text = "Détruire l'item"
        trash_label_layer = 0
        self._trash_label = TextOutlined(trash_label_x * TILE_SIZE,
                                         trash_label_y * TILE_SIZE,
                                         trash_label_text,
                                         trash_label_layer)
        self._trash_label.add_to_group(self._state.sprites)

    def empty_trashcan(self):
        if self._trash_slot is not None:
            q = self._trash_slot.quantity
            if q > 0:
                self._trash_slot.take_item(self._trash_slot.quantity)

    def lock(self):
        self._locked = True

    def unlock(self):
        self._locked = False

    def reset(self):
        self.nav_index_tochange = False
        self.nav_index = 0
        self.previous_index = None
        self.hover_nav = [False, -1]
        self.set_nav(self.nav_index)

    def get_slot_list(self):
        return self._multiple_inventories[self.nav_index].get_slot_list()+[self._trash_slot]
    
    def get_slots(self):
        return self._slots
    
    slots = property(get_slots)

    def set_nav(self, index):
        for sprite in self._nav_group:
            sprite.kill()

        self.nav = Nav(0, self._y, TILE_SIZE/2, self._nav_group, index, ["Ingredients","Mixtures","Potions", "Recettes"], TILE_SIZE*2)

        for sprite in self._nav_group:
            sprite.add(self._group)
    
    def update(self, event, is_holding):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i and not self._locked and not is_holding:
                self.toggle_open_close()

        if self._open:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self._trash_label is not None and self._trash_label.rect.collidepoint(event.pos):
                    self.empty_trashcan()
                else:
                    for i in range(0, len(self.nav.tabs)):
                        if self.nav.tabs[i]["space"].rect.collidepoint(event.pos):
                            self.change_nav_index(i)
                            break

            elif event.type == pygame.MOUSEMOTION:
                self.hover_nav = [False, -1]
                for i in range(0,len(self.nav.tabs)):
                    if self.nav.tabs[i]["space"].rect.collidepoint(event.pos):
                        self.hover_nav = [True, i]
                        break
            else:
                pass

            if self.nav_index_tochange:
                self.nav_index_tochange = False
                if self.previous_index != None:
                    self._multiple_inventories[self.previous_index].close()
                self.set_nav(self.nav_index)
                for sprite in self._nav_group:
                    sprite.add(self._state.sprites)
                self._multiple_inventories[self.nav_index].open()

            self.nav.reset_colors()
            if self.hover_nav[0] and self.hover_nav[1] != self.nav_index:
                self.nav.reset_colors()
                self.nav.hover_tab(self.hover_nav[1])

        self._multiple_inventories[self.nav_index].update(event, is_holding)


    def open(self):
        self.reset()
        for sprite in self._group:
            sprite.add(self._state.sprites)
        self._multiple_inventories[self.nav_index].open()
        self._open = True

    def close(self):
        for sprite in self._group:
            sprite.remove(self._state.sprites)
        for sprite in self._nav_group:
            sprite.remove(self._state.sprites)
        self._multiple_inventories[self.nav_index].close()
        self._open = False

    def toggle_open_close(self, *is_holding):
        if self._state != None:
            if self._open and not is_holding:
                self.close()
            else:
                self.open()

    def change_nav_index(self, index):
        self.nav_index_tochange = self.nav_index != index
        self.previous_index = self.nav_index
        self.nav_index = index

    
    def update_slots(self):
        self._multiple_inventories[self.nav_index].update_slots()


    