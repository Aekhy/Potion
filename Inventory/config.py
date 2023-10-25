from config import COLORS

# Inventory
INVENTORY_SLOT_NUMBER = 8
INVENTORY_LAYOUT = [
    [{"type":"Slot","item_name":"Soufre","quantity":10},
     {"type":"Slot","item_name":"Soufre","quantity":1},
     {"type":"Slot","item_name":"Orties","quantity":5},
     {"type":"Slot","item_name":"Soufre","quantity":2},
     {"type":"Slot"}],
     [{"type":"Slot"},
      {"type":"Slot"},
      {"type":"Slot"}]
      ]
INVENTORY_SLOT_SIZE = 100


# Slot
TEXT_FONT_COLOR_DEFAULT = COLORS['white']
TEXT_OUTLINE_FONT_COLOR_DEFAULT = COLORS['black']
TEXT_FONT_SIZE_DEFAULT = 25
TEXT_FONT_PATH_DEFAULT = None
QUANTITY_FONT_SIZE_DEFAULT = 25
QUANTITY_FONT_COLOR_DEFAULT = COLORS['white']
ITEM_NAME_FONT_SIZE_DEFAULT = 25
ITEM_NAME_FONT_COLOR_DEFAULT = COLORS['red']
SLOT_COLOR_DEFAULT = COLORS['darkgrey']

# Item
MAX_STACK_DEFAULT = 10

# Case
CASE_SIZE_DEFAULT = 100
CASE_COLOR_DEFAULT = COLORS['grey']
CASE_TYPE_DEFAULT = 'Slot'