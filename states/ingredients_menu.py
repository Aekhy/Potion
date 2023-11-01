from states.tab_menu import TabMenu
from states.nav import Nav
import pygame



class IngredientsMenu(TabMenu):
    def __init__(self, game):
        super().__init__(game, 1)

    #     self.hover_nav_ingredient = [False, -1]
    #     self.reset()
        
    def reset(self):
        pass
        # self.change_current_nav_ingredient_index = False
        # self.current_nav_ingredients_index = 0
        # self.set_nav_ingredients(self.current_nav_ingredients_index)

    # def set_nav_ingredients(self, index):
    #     self.nav_ingredients = Nav(0, 1*50, 30, self.sprites, index, ["Astraux","Elementaires"])

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

                # self.hover_nav_ingredient = [False, -1]
                # for i in range(0,len(self.nav_ingredients.tabs)):
                #     if self.nav_ingredients.tabs[i]["space"].rect.collidepoint(event.pos):
                #         self.hover_nav_ingredient = [True, i]
                #         break
                
                self.hover_nav_menu = [False, -1]
                for i in range(0,len(self.nav_menu.tabs)):
                    if self.nav_menu.tabs[i]["space"].rect.collidepoint(event.pos):
                        self.hover_nav_menu = [True, i]
                        break

            # To select the next state we want to go in
            elif event.type == pygame.MOUSEBUTTONDOWN:

                for i in range(0,len(self.nav_menu.tabs)):
                    if self.nav_menu.tabs[i]["space"].rect.collidepoint(event.pos):
                        self.choice = i
                        break

                # for i in range(0, len(self.nav_ingredients.tabs)):
                #     if self.nav_ingredients.tabs[i]["space"].rect.collidepoint(event.pos):
                #         self.change_current_nav_ingredient_index = self.current_nav_ingredients_index != i
                #         self.current_nav_ingredients_index = i
                #         break
                

    def update(self):
        # DEV
        # go see comments in states.py
        if not self._in_state:
            self._in_state = True

        # if self.change_current_nav_ingredient_index:
        #     self.set_nav_ingredients(self.current_nav_ingredients_index)

        # Update the hovering of nav_ingredients
        # self.nav_ingredients.reset_colors()
        # if self.hover_nav_ingredient[0] and self.hover_nav_ingredient[1] != self.current_nav_ingredients_index:
        #     self.nav_ingredients.hover_tab(self.hover_nav_ingredient[1])

        self.tab_menu_update(self.reset)
        self.sprites.update()

    def draw(self,screen):
        self.sprites.draw(screen)

