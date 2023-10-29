from states.tab_menu import TabMenu
from states.nav import Nav
from inventory.inventory import Inventory
import pygame

class IngredientsMenu(TabMenu):
    def __init__(self, game):
        super().__init__(game, 0)


        self.current_nav_ingredients_index = 0
        self.change_current_nav_ingredient_index = False
        self.set_nav_ingredients(self.current_nav_ingredients_index)

        self.slots = {"take":[],"add":[]}
        self.first_struct =[
            [
            {"type":"Slot","item_name":"eau","quantity":5},
            {"type":"Slot","item_name":"lavande","quantity":1},
            {"type":"Slot","item_name":"eau","quantity":5},
            {"type":"Slot","item_name":"crapaud","quantity":2},
            ],
            [
            {"type":"Slot","item_name":"braises","quantity":2},
            {"type":"Slot"},
            {"type":"Slot"},
            {"type":"Slot"}
            ],
            [
            {"type":"Slot"},
            {"type":"Slot"},
            {"type":"Slot"},
            {"type":"Slot"}
            ]
            ]
        self.second_struct = [
            [
            {"type":"Slot"},
            {"type":"Slot"},
            {"type":"Slot"},
            {"type":"Slot"}
            ],
            [
            {"type":"Slot"},
            {"type":"Slot"},
            {"type":"Slot"},
            {"type":"Slot"}
            ],
            [
            {"type":"Slot"},
            {"type":"Slot"},
            {"type":"Slot"},
            {"type":"Slot"}
            ]
            ]
        self.third_struct = [
           [
            {"type":"Slot"},
            {"type":"Slot"},
            {"type":"Slot"},
            {"type":"Slot"}
            ],
            [
            {"type":"Slot"},
            {"type":"Slot"},
            {"type":"Slot"},
            {"type":"Slot"}
            ] 
        ]
        
        self.inventories_sprites = [[pygame.sprite.LayeredUpdates()],[pygame.sprite.LayeredUpdates()],[pygame.sprite.LayeredUpdates()]]
        self.inventories = [[Inventory(self,self.inventories_sprites[0][0],0,80,self.first_struct)],
                            [Inventory(self,self.inventories_sprites[1][0],0,80,self.second_struct)],
                            [Inventory(self,self.inventories_sprites[2][0],0,80,self.third_struct)]]
    
    
    def set_nav_ingredients(self, index):
        self.nav_ingredients = Nav(0, 1*50, 30, self.sprites, index, ["Tout","Astraux","Elementaires"])

    def events(self):
       for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game.inGame = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.exit_state()
                elif event.key == pygame.K_ESCAPE:
                    new_event = self._game.states("Options")
                    new_event.enter_state()

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

                for i in range(0, len(self.nav_ingredients.tabs)):
                    if self.nav_ingredients.tabs[i]["space"].rect.collidepoint(event.pos):
                        self.change_current_nav_ingredient_index = self.current_nav_ingredients_index != i
                        self.current_nav_ingredients_index = i

    def reset(self):
        self.change_current_nav_ingredient_index = False
        self.current_nav_ingredients_index = 0
        self.set_nav_ingredients(self.current_nav_ingredients_index)  

    def update(self):

        if self.change_current_nav_ingredient_index:
            self.set_nav_ingredients(self.current_nav_ingredients_index)

        # Update the hovering of nav_ingredients
        self.nav_ingredients.reset_colors()
        if self.hover_nav_ingredient[0] and self.hover_nav_ingredient[1] != self.current_nav_ingredients_index:
            self.nav_ingredients.hover_tab(self.hover_nav_ingredient[1])

        self.tab_menu_update(self.reset)
        self.sprites.update()
        self.inventories_sprites[self.current_nav_ingredients_index][0].update()

    def draw(self,screen):
        self.sprites.draw(screen)
        self.inventories_sprites[self.current_nav_ingredients_index][0].draw(screen)

