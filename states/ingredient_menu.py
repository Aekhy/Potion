from states.state import State
from states.nav import Nav
import pygame

class IngredientMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.sprites = pygame.sprite.LayeredUpdates()
        # Nav that is shared among all menu
        self.nav_menu = Nav(0, 0*50, 50, self.sprites, 0, ["Ingredients", "Potions", "Recettes"])
        self.hover_nav_menu = [False, -1]

        self.nav_ingredients = Nav(0, 1*50, 30, self.sprites, 0, ["Astraux","Elementaires"])
        self.hover_nav_ingredient = [False, -1]

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game.inGame = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_state()

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
                        
    
    def update(self):
        if self.hover_nav_ingredient[0]:
            self.nav_ingredients.hover_tab(self.hover_nav_ingredient[1])
        else:
            self.nav_ingredients.reset_colors()
        if self.hover_nav_menu[0]:
            self.nav_menu.hover_tab(self.hover_nav_menu[1])
        else:
            self.nav_menu.reset_colors()

        self.sprites.update()

    def draw(self,screen):
        self.sprites.draw(screen)