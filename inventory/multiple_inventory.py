import pygame
from inventory.inventory import Inventory
from states.nav import Nav

class MultipleInventory():
    def __init__(self, struct_json:dict, state, x, y) -> None:
        self._struct = struct_json
        self._state = state
        self._x = x
        self._y = y
        self._len = self._struct["meta"]["number"]
        self._inventories = {}
        self._nav_text = []


        for i in range(0, self._len):
            self._nav_text.append(str(i))
            tmp = {}
            tmp["alive"] = False     
            tmp["group"] =  pygame.sprite.LayeredUpdates()
            tmp["inventory"] = Inventory(self._state, tmp["group"], self._x, self._y+60,self._struct[str(i)])
        
            self._inventories[i] = tmp

        
        self._nav_group = pygame.sprite.LayeredUpdates()
        self.reset()
        
    def reset(self):
        self.previous_index = None
        self._nav_index = 0
        self.change_nav_index = False
        self.hover_nav = [False, -1]
        self.set_nav(self._nav_index)

    def set_nav(self, index):
        for sprite in self._nav_group:
            sprite.kill()

        self.nav = Nav(self._x, self._y+30, 30, self._nav_group, index, self._nav_text, 500/5)

        for sprite in self._nav_group:
            sprite.add(self._state.sprites)


    def update(self, event, is_holding):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(0, len(self.nav.tabs)):
                if self.nav.tabs[i]["space"].rect.collidepoint(event.pos):
                    self.change_nav_index = self._nav_index != i
                    self.previous_index = self._nav_index
                    self._nav_index = i
                    break

        elif event.type == pygame.MOUSEMOTION:
            # self._drag_and_drop.move(event)
            self.hover_nav = [False, -1]
            for i in range(0,len(self.nav.tabs)):
                if self.nav.tabs[i]["space"].rect.collidepoint(event.pos):
                    # Holding an item over the nav tab is like clicking on it
                    if is_holding: 
                        self.change_nav_index = self._nav_index != i
                        self.previous_index = self._nav_index
                        self._nav_index = i
                    else:
                        self.hover_nav = [True, i]
                    break

        if self.change_nav_index:
            self.change_nav_index = False
            if self.previous_index != None:
                for sprite in self._inventories[self.previous_index]["group"]:
                    sprite.remove(self._state.sprites)
            self.set_nav(self._nav_index)
            for sprite in self._inventories[self._nav_index]["group"]:
                sprite.add(self._state.sprites)

        self.nav.reset_colors()
        if self.hover_nav[0] and self.hover_nav[1] != self._nav_index:
            self.nav.reset_colors()
            self.nav.hover_tab(self.hover_nav[1])

    def open(self):
        self.reset()
        for sprite in self._inventories[self._nav_index]["group"]:
            # sprite.add(self._group)
            sprite.add(self._state.sprites)


    def close(self):
        for sprite in self._inventories[self._nav_index]["group"]:
            sprite.remove(self._state.sprites)
        for sprite in self._nav_group:
            sprite.remove(self._state.sprites)

    def get_slot_list(self):
        return self._inventories[self._nav_index]["inventory"].slot_list

    def update_slots(self):
        for sprite in self._inventories[self._nav_index]["group"]:
            sprite.add(self._state.sprites)