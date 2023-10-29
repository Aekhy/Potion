from items.item import Item
from items.ingredients import Ingredient
from inventory.slot import Slot
from utils.group import draw_grp
from inventory.case import Case
from inventory.settings import *
from general_settings.private_settings import LAYERS

class Inventory:
    def __init__(self, game, group, x, y, inventory_structure=INVENTORY_LAYOUT):
        self.game = game
        self.group = group
        self.x = x
        self.y = y
        self._inventory_structure = inventory_structure
        self._inventory, self._slot_list = self.make_inventory_and_slot_list(inventory_structure)
        self._rect = self.make_inventory_rect(self._slot_list)
    
    # ////////// PUBLIC \\\\\\\\\\

    # ***** GETTERS *****

    @property
    def rect(self):
        return self._rect
    
    @property
    def inventory_layout(self):
        return self._inventory
    
    @property
    def slot_list(self):
        return self._slot_list

    # ////////// PRIVATE \\\\\\\\\\

    def make_usable_slot(self, element, i, j):
        # TEMPORAIRE POUR LE DEBUG ----------
        if 'item_name' in element.keys():
            item = Ingredient(element["item_name"])
            quantity = element["quantity"]
        else:
            item = None
            quantity = 0
        return Slot(self.game, self.group, True, True, item, quantity, self.x+j*INVENTORY_SLOT_SIZE, self.y+i*INVENTORY_SLOT_SIZE, LAYERS["inventory"], INVENTORY_SLOT_SIZE)
        # ---------------------------------

    def make_unusable_slot(self, i, j):
        Kase = Case(self.group, self.x+j*INVENTORY_SLOT_SIZE,self.y+i*INVENTORY_SLOT_SIZE, LAYERS["inventory"],"",INVENTORY_SLOT_SIZE) # type: ignore
        self.group.add(Kase) # type: ignore
    
    def make_inventory_and_slot_list(self, inventory_structure):
        inventory = []
        slot_list = []
        for i in range(0, len(inventory_structure)):
            row = []
            for j in range(0,len(inventory_structure[i])):
                element = inventory_structure[i][j]
                if element["type"] == "Slot":
                    tmp = self.make_usable_slot(element, i, j)
                    slot_list.append(tmp)
                else:
                    tmp = self.make_unusable_slot(i, j)
                row.append(tmp)
            inventory.append(row)
        return inventory, slot_list
    
    def make_inventory_rect(self, slot_list):
        if len(slot_list)>=0:
            inventory_rect = slot_list[0].rect
            if len(self._slot_list)>=2:
                for slot in slot_list[1:]:
                    inventory_rect = inventory_rect.union(slot.rect)
        return inventory_rect # type: ignore

        