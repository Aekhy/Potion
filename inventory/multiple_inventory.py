import pygame
from inventory.inventory import Inventory
from states.nav import Nav

class MultipleInventory():
    def __init__(self, struct_json:dict, state, game_inventory, x, y, authorized_classes:dict=None) -> None:
        self._struct = struct_json
 
        # The goal of self._state is to get the _sprites (group)
        # And the _slots (dict {"take":[],"add":[]}).
        # In our case, we will get the _slots by game_inventory, not _state
        self._state = state
        self._game_inventory = game_inventory
        self._x = x
        self._y = y
        self._len = self._struct["meta"]["number"]
        self._inventories = {}
        self._nav_text = []
        self._authorized_classes = authorized_classes

        for i in range(0, self._len):
            self._nav_text.append(str(i))
            tmp = {}
            tmp["alive"] = False     
            tmp["group"] =  pygame.sprite.LayeredUpdates()
            # We are passing _game_inventory to make sure that all the slots 
            # that are created, register themselves in _game_inventory._slots
            tmp["inventory"] = Inventory(self._game_inventory, tmp["group"], self._x, self._y+60,self._struct[str(i)], self._authorized_classes)
        
            self._inventories[i] = tmp

        
        self._nav_group = pygame.sprite.LayeredUpdates()
        if self._state != None:
            self.reset()
     
    def set_state(self, new_state):
        self._state = new_state

    def reset(self):
        self.previous_index = None
        self._nav_index = 0
        self.change_nav_index = False
        self.hover_nav = [False, -1]
        self.set_nav(self._nav_index)

    def set_nav(self, index):
        for sprite in self._nav_group:
            sprite.kill()

        self.nav = Nav(self._x, self._y+32, 32, self._nav_group, index, self._nav_text, 500/5)

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

        if self.hover_nav[0] and self.hover_nav[1] != self._nav_index:
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