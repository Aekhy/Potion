from states.state import State
from states.nav import Nav
import pygame

class IngredientMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.sprites = pygame.sprite.LayeredUpdates()

        # Nav that is shared among all menu
        # Int that indicated which option of the nav we are in. ex : 0 -> Ingredients
        self.current_nav_menu_index = 0
        self.nav_menu = Nav(0, 0*50, 50, self.sprites, self.current_nav_menu_index, ["Ingredients", "Potions", "Recettes", "Options"])
        self.hover_nav_menu = [False, -1]

        self.current_nav_ingredients_index = 0
        self.nav_ingredients = Nav(0, 1*50, 30, self.sprites, self.current_nav_ingredients_index, ["Astraux","Elementaires"])
        self.hover_nav_ingredient = [False, -1]

        self.choices = {0:self._game.all_states["Ingredients"],# TO DO ADD STATE in all_states of Game 
                        1:self._game.all_states["Potions"],# TO DO ADD STATE in all_states of Game  
                        2:self._game.all_states["Recettes"],# TO DO ADD STATE in all_states of Game 
                        3:self._game.all_states["Options"],# TO DO ADD STATE in all_states of Game 
                        }
        self.choice = None
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game.inGame = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_state()
           
            # For hovering the navs
            elif event.type == pygame.MOUSEMOTION:
                self.hover_nav_ingredient = [False, -1]
                for i in range(0,len(self.nav_ingredients.tabs)):
                    if self.nav_ingredients.tabs[i]["space"].rect.collidepoint(event.pos):
                        self.hover_nav_ingredient = [True, i]
                        break
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
    
    def update(self):
        # Update the hovering of nav_ingredients
        if self.hover_nav_ingredient[0]:
            self.nav_ingredients.hover_tab(self.hover_nav_ingredient[1])
        else:
            self.nav_ingredients.reset_colors()

        # Update the hovering of nav_menu
        if self.hover_nav_menu[0]:
            self.nav_menu.hover_tab(self.hover_nav_menu[1])
        else:
            self.nav_menu.reset_colors()

        # Go to another state if we chosed one state of the nav_menu's states
        if self.choice != None and self.choice != self.current_nav_menu_index:
            new_state = self.choices[self.choice]
            self.choice == None
            new_state.enter_state()

        self.sprites.update()

    def draw(self,screen):
        self.sprites.draw(screen)