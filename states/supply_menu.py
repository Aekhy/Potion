from inventory.drag_and_drop import DragAndDrop
from inventory.multiple_inventory import MultipleInventory
from general_settings.private_settings import *
from states.tab_menu import TabMenu
from utils.texts import TextOutlined
from items.settings import *
from items.ingredients import *
from items.recipe import Paper
import pygame
import random

class SupplyMenu(TabMenu):
    def __init__(self, game):
        super().__init__(game, 4)
        self.slots = {"take":[],"add":[]}
        # Very important to do that in each state that use
        # _game_inventory. It crashes if not done
        self._game.game_inventory.set_state(self)
        # this open the inventory 
        self._game.game_inventory.open()
        # We don't want to be able to close the _game_inventory when we are in here
        self._game.game_inventory.lock()
       

        dict_supply = {
        "meta": {"number": 1},
        '0': [
            [
                {"type":"Slot"},
                {"type":"Slot"},
                {"type":"Slot"}
            ],
            [
                {"type":"Slot","item_name":"eau","quantity":5},
                {"type":"Slot","item_name":"lavande","quantity":1},
                {"type":"Slot"}
            ]
        ]
        }
        self._supplies_x = 10
        self._supplies_y = 3
        
        self._supplies = MultipleInventory(dict_supply, self, self ,self._supplies_x*TILE_SIZE, self._supplies_y*TILE_SIZE, None, True, True)
        self._supplies.open()

        self._get_supplies_button = TextOutlined((self._supplies_x + 3/2)*TILE_SIZE,
                                                 (self._supplies_y+3.25)*TILE_SIZE,
                                                 "Obtenir des provisions",
                                                 0)
        
        self._get_supplies_button.add_to_group(self.sprites)

        self._drag_and_drop = DragAndDrop(self.sprites, self.update_fct_dragndrop)


    def get_supply(self):
        # if empty
        empty = True
        for slot in self._supplies.get_slot_list():
            if slot.quantity != 0:
                empty = False
                break

        if empty:
            for slot in self._supplies.get_slot_list():
                ingredient_or_paper = random.randint(1,6)
                if ingredient_or_paper == 6:
                    item = Paper()
                    quantity = random.randint(1,5)
                else:
                    ingredient_tuple = random.choice(list(INGREDIENT_DATA.items()))
                    # update ingredient
                    self._game.knowledge.UpdateIngredientKnowledge(ID[ingredient_tuple[0]],
                                                                   "name",
                                                                   "img",
                                                                   "type",
                                                                   "characteristics",
                                                                   "max_stack")
                    # update characteristics of ingredient
                    for chara in INGREDIENT_DATA[ID[ingredient_tuple[0]]]["characteristics"]:
                        self._game.knowledge.UpdateCharacteristicKnowledge(ID[chara],
                                                                           "name",
                                                                           "img")
                        for opposite in CHARACTERISTIC_DATA[ID[chara]]["opposites"]:
                            self._game.knowledge.UpdateCharacteristicKnowledge(ID[chara], op = ID[opposite])

                    item = Ingredient(ID[ingredient_tuple[0]])
                    quantity = random.randint(1,ingredient_tuple[1]["max_stack"])
                slot.add_item(item, quantity)
            self._supplies.update_slots()
        # generate stuff

    def update_fct_dragndrop(self):
        self._game.game_inventory.update_slots()
        self._supplies.update_slots()

    def events(self):
       for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game.inGame = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self._game.game_inventory.unlock()
                    self._game.game_inventory.close()

                    self._supplies.close()

                    self.exit_state()

                elif event.key == pygame.K_o or event.key == pygame.K_ESCAPE:
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
                if self._game.game_inventory._open:
                    self._drag_and_drop.take(self._game.game_inventory.slots["take"]+self.slots["take"], self._game.game_inventory.get_slot_list()+self._supplies.get_slot_list(), event)

                if self._get_supplies_button.rect.collidepoint(event.pos):
                    self.get_supply()
                else:
                    for i in range(0,len(self.nav_menu.tabs)):
                        if self.nav_menu.tabs[i]["space"].rect.collidepoint(event.pos):
                            self.choice = i
                            break

            elif event.type == pygame.MOUSEBUTTONUP:
                if self._game.game_inventory._open:
                    self._drag_and_drop.drop(self._game.game_inventory.slots["add"]+self.slots["add"], self._game.game_inventory.get_slot_list()+self._supplies.get_slot_list(), event)

            self._game.game_inventory.update(event, self._drag_and_drop.is_holding())
            
    def update(self):
        # DEV
        # go see comments in states.py
        if not self._in_state:
            self._in_state = True
            self.game.game_inventory.set_state(self)
            self._game.game_inventory.open()
            self._game.game_inventory.lock()
            self._supplies.open()

        self.tab_menu_update()

        self.sprites.update()

    def draw(self,screen):

        self.sprites.draw(screen)