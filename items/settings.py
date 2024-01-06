from utils.json_functions import Read

# -- settings --
DEFAULT_MAX_STACK = 10
DEFAULT_POTION_MAX_STACK = 3

#__________ id __________

ID = Read("items/primary_data/id.json")


# __________ Ingredients __________

# -- settings --
DEFAULT_INGREDIENT_MAX_STACK = 5
# -- characteristics --
CHARACTERISTIC_DATA = Read("items/primary_data/characteristic.json")
# -- ingredients --
INGREDIENT_DATA = Read("items/primary_data/ingredients.json")


# _________ BASE ACTIVE ________

# -- base --
BASE_DATA = Read("items/primary_data/base.json")
BASE_GRAPH = Read("items/secondary_data/base_graph.json")
# -- active --
ACTIVE_DATA = Read("items/primary_data/active.json")
ACTIVE_GRAPH = Read("items/secondary_data/active_graph.json")

# -- both --
BASE_ACTIVE_COMPATIBILITY_MATRIX = Read("items/secondary_data/base_active_compatibility_matrix.json")

# -- effect
EFFECT_DATA = Read("items/primary_data/effect.json")


# __________ Potions __________

# -- settings --
# levels
TOP = 3
MIDDLE = 2
BOTTOM = 1
END = 0

# -- alchemical property --
ALCHEMICAL_PROPERTY_DATA = Read("items/primary_data/alchemical_property.json")
ALCHEMICAL_PROPERTY_MATRIX = Read("items/secondary_data/alchemical_property_matrix.json")

# -- potion --
POTION_DATA = Read("items/primary_data/potions.json")
MAIN_POTION_TREE = Read("items/secondary_data/potion_tree.json")


