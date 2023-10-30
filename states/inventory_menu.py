import pygame
import json
from states.tab_menu import TabMenu
from inventory.game_inventory import GameInventory
from utils.drag_and_drop import DragAndDrop


class InventoryMenu(TabMenu):
    def __init__(self, game):
        super().__init__(game, 0)

        self.slots = {"take":[],"add":[]}
        with open("inventory/game_inventory_layout.json") as file:
            data = json.load(file)

        self._game_inventory = GameInventory(self, data, 0, 50, True)
        self._game_inventory.toggle_open_close()
        self._drag_and_drop = DragAndDrop(self.sprites, self._game_inventory.update_slots)
    
    def reset(self):
        pass

    def events(self):
       for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game.inGame = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_TAB:
                    self._game_inventory.close()
                    self.exit_state()

                elif event.key == pygame.K_ESCAPE:
                    new_event = self._game.states("Options")
                    new_event.enter_state()


            # For hovering the navs
            elif event.type == pygame.MOUSEMOTION:
                self._drag_and_drop.move(event)
                self.hover_nav_menu = [False, -1]
                for i in range(0,len(self.nav_menu.tabs)):
                    if self.nav_menu.tabs[i]["space"].rect.collidepoint(event.pos):
                        self.hover_nav_menu = [True, i]
                        break

            # To select the next state we want to go in
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._drag_and_drop.take(self.slots["take"], self._game_inventory.get_slot_list(), event)

                for i in range(0,len(self.nav_menu.tabs)):
                    if self.nav_menu.tabs[i]["space"].rect.collidepoint(event.pos):
                        self.choice = i
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                self._drag_and_drop.drop(self.slots["add"], self._game_inventory.get_slot_list(), event)

            self._game_inventory.update(event, self._drag_and_drop.is_holding())
            
    def update(self):

        self.tab_menu_update(self.reset)

        self.sprites.update()

    def draw(self,screen):

        self.sprites.draw(screen)
 