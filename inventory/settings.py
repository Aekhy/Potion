# DEFAULT_SLOT_TYPE = "Slot"
# DEFAULT_SLOT_SIZE = 100
# DEFAULT_SLOT_COLOR = "Grey"


# DEFAULT_QUANTITY_FONT_SIZE = 25
# DEFAULT_QUANTITY_FONT_COLOR = "White"
# DEFAULT_ITEM_NAME_FONT_COLOR = "White"
# DEFAULT_ITEM_NAME_FONT_SIZE = 25


from general_settings.private_settings import COLORS

# Inventory
INVENTORY_SLOT_NUMBER = 8
INVENTORY_LAYOUT = [
    [{"type":"Slot","item_type":"ingredient","item_data":"eau","quantity":5},
     {"type":"Slot","item_type":"ingredient","item_data":"lavande","quantity":1},
     {"type":"Slot","item_type":"ingredient","item_data":"eau","quantity":5},
     {"type":"Slot","item_type":"ingredient","item_data":"crapaud","quantity":2},
     {"type":"Slot","item_type":"ingredient","item_data":"braises","quantity":2}],
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