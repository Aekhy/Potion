import pygame
from inventory.multiple_inventory import MultipleInventory
from states.nav import Nav


class GameInventory:
    def __init__(self, state, struct_json: dict, x, y, permanent=False) -> None:

        self._state = state
        self._group = pygame.sprite.LayeredUpdates()
        self._struct = struct_json
        self._x = x
        self._y = y
        self._permanent = permanent

        self._multiple_inventories = {
            0: MultipleInventory(self._struct["ingredients"], self._state, 0, 50),
            1: MultipleInventory(self._struct["mixtures"], self._state, 0, 50),
            2: MultipleInventory(self._struct["potions"], self._state, 0, 50)
        }

        self._open = False

        self._nav_group = pygame.sprite.LayeredUpdates()
        self.reset()
        
    def reset(self):
        self.change_nav_index = False
        self.nav_index = 0
        self.previous_index = None
        self.hover_nav = [False, -1]
        self.set_nav(self.nav_index)

    def set_nav(self, index):
        for sprite in self._nav_group:
            sprite.kill()

        self.nav = Nav(0, self._y, 30, self._nav_group, index, ["Ingredients","Mixtures","Potions"], 500/3)

        for sprite in self._nav_group:
            sprite.add(self._group)
    
    def update(self, event, is_holding):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i and not self._permanent:
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

    def close(self):
        for sprite in self._group:
            sprite.remove(self._state.sprites)
        for sprite in self._nav_group:
            sprite.remove(self._state.sprites)
        self._multiple_inventories[self.nav_index].close()

    def toggle_open_close(self):
        if self._open:
            self.close()
        else:
            self.open()
        self._open = not self._open

    def get_slot_list(self):
        return self._multiple_inventories[self.nav_index].get_slot_list()
    
    def update_slots(self):
        self._multiple_inventories[self.nav_index].update_slots()