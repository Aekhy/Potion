from states.state import State
from states.nav import Nav
import pygame

class TabMenu(State):
    def __init__(self, game, nav_menu_index:int):
        super().__init__(game)
        self.sprites = pygame.sprite.LayeredUpdates()

        # Nav that is shared among all menu
        # Int that indicated which option of the nav we are in. ex : 0 -> Ingredients
        self.selected = True
        self.change = True
        self.change_nav_menu_index = False
        self.current_nav_menu_index = nav_menu_index
        self.hover_nav_menu = [False, -1]
        self.set_nav_menu(self.current_nav_menu_index)
        
        self.choice = None
        
    def set_nav_menu(self, index):
        self.nav_menu = Nav(0, 0, 64, self.sprites, index, ["Inventaire", "Ingredients", "Mixtures", "Potions", "Provisions"])
        
    def tab_menu_update(self):
        # The events loop of Tab_menu childrens should update variables like self.choice and self.selected and self.hover_nav_menu

        

        if not self.selected:
            self.selected = not self.selected
            self.set_nav_menu(self.current_nav_menu_index)

        # Update the hovering of nav_menu
        self.nav_menu.reset_colors()
        if self.hover_nav_menu[0] and self.hover_nav_menu[1] != self.current_nav_menu_index:
            self.nav_menu.reset_colors()
            self.nav_menu.hover_tab(self.hover_nav_menu[1])

        # Go to another state if we chosed one state of the nav_menu's states

        if self.choice != None and self.choice != self.current_nav_menu_index:
            self.selected = False
            if self.choice == 0:
                self.selected = False
                new_state = self._game.states("InventoryMenu")
            elif self.choice == 1:
                self.selected = False
                new_state = self._game.states("IngredientsMenu")
            elif self.choice == 2:
                self.selected = False
                new_state = self._game.states("MixturesMenu")
            elif self.choice == 3:
                self.selected = False
                new_state = self._game.states("PotionsMenu")
            elif self.choice == 4:
                self.selected = False
                new_state = self._game.states("SupplyMenu")
            
            self.set_nav_menu(self.choice)
            self.choice = None
            self.exit_state()
            new_state.enter_state()
