from config import COLORS, LAYERS

# Inventory
INVENTORY_SLOT_NUMBER = 8
DEFAULT_INVENTORY_LAYOUT = [
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
DEFAULT_TEXT_FONT_COLOR = COLORS['white']
DEFAULT_TEXT_OUTLINE_FONT_COLOR = COLORS['black']
DEFAULT_TEXT_FONT_SIZE = 25
DEFAULT_TEXT_FONT_PATH = None
DEFAULT_QUANTITY_FONT_SIZE = 25
DEFAULT_QUANTITY_FONT_COLOR = COLORS['white']
DEFAULT_ITEM_NAME_FONT_COLOR = COLORS['white']
DEFAULT_ITEM_NAME_FONT_SIZE = 25
QUANTITY_FONT_SIZE_DEFAULT = 25
QUANTITY_FONT_COLOR_DEFAULT = COLORS['red']
ITEM_NAME_FONT_SIZE_DEFAULT = 25
ITEM_NAME_FONT_COLOR_DEFAULT = COLORS['red']
SLOT_COLOR_DEFAULT = COLORS['darkgrey']

# Item
DEFAULT_MAX_STACK = 10

# Case
CASE_SIZE_DEFAULT = 100
CASE_COLOR_DEFAULT = COLORS['grey']
CASE_TYPE_DEFAULT = 'Slot'