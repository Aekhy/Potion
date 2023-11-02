import pygame
from inventory.multiple_inventory import MultipleInventory
from items.potions import Potion, Base, Active
from states.nav import Nav

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
            0: MultipleInventory(self._struct["ingredients"], self._state, self, 0, 50, {"black_list":[Potion, Base, Active],"white_list":None}),
            1: MultipleInventory(self._struct["mixtures"], self._state, self, 0, 50, {"black_list":None,"white_list":[Base, Active]}),
            2: MultipleInventory(self._struct["potions"], self._state, self, 0, 50, {"black_list":None,"white_list":[Potion]})
        }

        self._open = False

        self._nav_group = pygame.sprite.LayeredUpdates()
        self.reset()

    def set_state(self, new_state):
        self._state = new_state
        for key, value in self._multiple_inventories.items():
            value.set_state(self._state)

    def lock(self):
        self._locked = True

    def unlock(self):
        self._locked = False

    def reset(self):
        self.change_nav_index = False
        self.nav_index = 0
        self.previous_index = None
        self.hover_nav = [False, -1]
        self.set_nav(self.nav_index)

    def get_slot_list(self):
        return self._multiple_inventories[self.nav_index].get_slot_list()
    
    def get_slots(self):
        return self._slots
    
    slots = property(get_slots)

    def set_nav(self, index):
        for sprite in self._nav_group:
            sprite.kill()

        self.nav = Nav(0, self._y, 30, self._nav_group, index, ["Ingredients","Mixtures","Potions"], 500/3)

        for sprite in self._nav_group:
            sprite.add(self._group)
    
    def update(self, event, is_holding):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i and not self._locked and not is_holding:
                self.toggle_open_close()

        if self._open:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(0, len(self.nav.tabs)):
                    if self.nav.tabs[i]["space"].rect.collidepoint(event.pos):
                        self.change_nav_index = self.nav_index != i
                        self.previous_index = self.nav_index
                        self.nav_index = i
                        break

            elif event.type == pygame.MOUSEMOTION:
                self.hover_nav = [False, -1]
                for i in range(0,len(self.nav.tabs)):
                    if self.nav.tabs[i]["space"].rect.collidepoint(event.pos):
                        self.hover_nav = [True, i]
                        break
            else:
                pass

            if self.change_nav_index:
                self.change_nav_index = False
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

    
    def update_slots(self):
        self._multiple_inventories[self.nav_index].update_slots()


    