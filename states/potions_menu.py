from states.tab_menu import TabMenu
from states.grid_display import GridDisplay
from states.nav import Nav
import pygame

class PotionsMenu(TabMenu):
    def __init__(self, game):
        super().__init__(game, 3)

        self._group = pygame.sprite.LayeredUpdates()
        self._grids = [GridDisplay(self._game.knowledge.grids["potion"],self,0,80), GridDisplay(self._game.knowledge.grids["alchemical_property"],self,0,80)]
        
        self.reset_nav_body()
        
    def reset_nav_body(self):
        self.previous_index = None
        self.change_nav_index = False
        self.nav_index = 0
        self.hover_nav = [False, -1]

        self.set_nav_body(self.nav_index)


    def set_nav_body(self, index):
        for sprite in self._group:
            sprite.kill()

        # nav
        self.nav = Nav(0, 50, 30, self._group, index, ["Potions","Propriétés Alchimique"])
        # body
        self._grids[self.nav_index].open()

        for sprite in self._group:
            sprite.add(self.sprites)

    def reset(self):
        pass
        

    def events(self):
       for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game.inGame = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.exit_state()
                elif event.key == pygame.K_o:
                    new_event = self._game.states("Options")
                    new_event.enter_state()

            # For hovering the navs
            elif event.type == pygame.MOUSEMOTION:

                self.hover_nav = [False, -1]
                for i in range(0,len(self.nav.tabs)):
                    if self.nav.tabs[i]["space"].rect.collidepoint(event.pos):
                        self.hover_nav = [True, i]
                        break
                
                self.hover_nav_menu = [False, -1]
                for i in range(0,len(self.nav_menu.tabs)):
                    if self.nav_menu.tabs[i]["space"].rect.collidepoint(event.pos):
                        self.hover_nav_menu = [True, i]
                        break

            # To select the next state we want to go in
            elif event.type == pygame.MOUSEBUTTONDOWN:

                for i in range(0, len(self.nav.tabs)):
                    if self.nav.tabs[i]["space"].rect.collidepoint(event.pos):
                        self.change_nav_index = self.nav_index != i
                        self.previous_index = self.nav_index
                        self.nav_index = i
                        break

                for i in range(0,len(self.nav_menu.tabs)):
                    if self.nav_menu.tabs[i]["space"].rect.collidepoint(event.pos):
                        self.choice = i
                        break
            self._grids[self.nav_index].update(event)

    def update(self):
        # DEV
        # go see comments in states.py
        if not self._in_state:
            self._in_state = True

        if self.change_nav_index:
            if self.previous_index is not None:
                self._grids[self.previous_index].close()
            self.change_nav_index = False
            self._grids[self.nav_index].open()
            self.set_nav_body(self.nav_index)
            

        self.nav.reset_colors()
        if self.hover_nav[0] and self.hover_nav[1] != self.nav_index:
            self.nav.reset_colors()
            self.nav.hover_tab(self.hover_nav[1])

        self.tab_menu_update(self.reset_nav_body)
        self.sprites.update()

    def draw(self,screen):
        self.sprites.draw(screen)