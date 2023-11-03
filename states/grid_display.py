import pygame
from math import ceil
from states.nav import Nav
from utils.my_sprite import MySprite
class GridDisplay():
    def __init__(self, knowledge_grid:dict, state, x, y) -> None:
        self._grid = knowledge_grid
        self._state = state
        self._x = x
        self._y = y
      
        self._pages = []
        l = len(self._grid)
        for i in range(0, l):
            self._pages.append(str(i))

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

        self.nav = Nav(self._x, self._y, 32, self._nav_group, index, self._pages)

        for sprite in self._nav_group:
            sprite.add(self._state.sprites)


    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(0, len(self.nav.tabs)):
                if self.nav.tabs[i]["space"].rect.collidepoint(event.pos):
                    self.change_nav_index = self._nav_index != i
                    self.previous_index = self._nav_index
                    self._nav_index = i
                    break

            # clicking on grid cells
            for sprite in self._grid[self._nav_index]["group"]:
                if sprite.rect.collidepoint(event.pos):
                    if isinstance(sprite, MySprite):
                        data = sprite.get_data()
                        if data is not None and data["type"] == "case":
                            if self._state.data_display is not None and data["id"] != self._state.data_display["id"]:
                                self._state.data_display_changed = True
                            self._state.data_display = data

        elif event.type == pygame.MOUSEMOTION:
            self.hover_nav = [False, -1]
            for i in range(0,len(self.nav.tabs)):
                if self.nav.tabs[i]["space"].rect.collidepoint(event.pos):
                    self.hover_nav = [True, i]


        if self.change_nav_index:
            self.change_nav_index = False
            if self.previous_index != None:
                for sprite in self._grid[self.previous_index]["group"]:
                    sprite.remove(self._state.sprites)
            self.set_nav(self._nav_index)
            for sprite in self._grid[self._nav_index]["group"]:
                sprite.add(self._state.sprites)

        if self.hover_nav[0] and self.hover_nav[1] != self._nav_index:
            self.nav.hover_tab(self.hover_nav[1])

    def open(self):
        self.reset()
        for sprite in self._grid[self._nav_index]["group"]:
            sprite.add(self._state.sprites)

    def close(self):
        for sprite in self._grid[self._nav_index]["group"]:
            sprite.remove(self._state.sprites)
        for sprite in self._nav_group:
            sprite.remove(self._state.sprites)
