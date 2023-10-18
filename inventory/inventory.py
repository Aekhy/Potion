
from items.item import Item
from inventory.slot import Slot
from utils.group import draw_grp
from utils.case import Case
from inventory.settings import *

class Inventory:
    def __init__(self, x, y, inventory_structure=DEFAULT_INVENTORY_LAYOUT):
        self.x = x
        self.y = y
        self.inventory, self.slot_list = self.make_inventory_and_slot_list(inventory_structure)
        self.rect = self.make_inventory_rect(self.slot_list)

    def get_rect(self):
        return self.rect
    
    def get_inventory_layout(self):
        return self.inventory
    
    def get_slot_list(self):
        return self.slot_list
    
    def make_usable_slot(self, element, i, j):
        # TEMPORAIRE POUR LE DEBUG ----------
        if 'item_name' in element.keys():
            item = Item(element["item_name"])
            quantity = element["quantity"]
        else:
            item = None
            quantity = 0
        return Slot(item, quantity, self.x+j*INVENTORY_SLOT_SIZE, self.y+i*INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)
        # ---------------------------------

    def make_unusable_slot(self, i, j):
        tmp = Case(self.x+j*INVENTORY_SLOT_SIZE,self.y+i*INVENTORY_SLOT_SIZE,"",INVENTORY_SLOT_SIZE)
        draw_grp.add(tmp)
        return tmp
    
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
            inventory_rect = slot_list[0].get_rect()
            if len(self.slot_list)>=2:
                for slot in slot_list[1:]:
                    inventory_rect = inventory_rect.union(slot.get_rect())
        return inventory_rect

        