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












# BASE_GRAPH = {
#     NEUTRAL: {
#         "neighbours": [
#             {
#                 "name": SUN,
#                 "weight": [[MAJOR, GAS], [GAS, MAJOR]]
#             },
#             {
#                 "name": EARTH,
#                 "weight": [[LIQUID, LIGHT], [LIGHT, LIQUID]]
#             }
#         ]
#     },
#     SUN: {
#         "neighbours": [
#             {
#                 "name": SUN,
#                 "weight": [[MAJOR, GAS], [GAS, MAJOR]]
#             }
#         ]
#     },
#     EARTH: {
#         "neighbours": [
#             {
#                 "name": EARTH,
#                 "weight": [[LIQUID, LIGHT], [LIGHT, LIQUID]]
#             }
#         ]
#     }
# }



# ALCHEMICAL_PROPERTY_MATRIX = {
#     NOTHING: {
#         NOTHING: NOTHING,
#         FERMENTATION: NOTHING,
#         DISTILLATION: NOTHING,
#         SUBLIMATION: NOTHING,
#     },
#     HEATING: {
#         NOTHING: NOTHING,
#         FERMENTATION: HEX,
#         DISTILLATION: SPELL,
#         SUBLIMATION: COUNTER_SPELL,
#     },
#     FREEZING: {
#         NOTHING: NOTHING,
#         FERMENTATION: BEWITCHMENT,
#         DISTILLATION: CHARM,
#         SUBLIMATION: ENCHANTMENT
#     },
#     MIXING: {
#         NOTHING: NOTHING,
#         FERMENTATION: CURSE,
#         DISTILLATION: TRANSFIGURATION,
#         SUBLIMATION: BLESSING
#     },

# }


# HEALTH_POTION_TREE = {
#     "level": MIDDLE,
#     "name": "santé ",
#     CHARM:
#     {
#         "level": BOTTOM,
#         "name": "régénération",
#         WATER: {"level": END, "name": "AquaVivacité",  "description": "Effet lent mais fort."},
#         FIRE: {"level": END, "name": "PyroRenouveau", "description": "Effet rapide mais faible."},
#         NEUTRAL: {"level": END, "name": "Potion de Guérison Standard",
#                   "description": "Une potion qui soigne les écorchures"}
#     },
#     TRANSFIGURATION:
#     {
#         "level": BOTTOM,
#         "name": "taille",
#         NEUTRAL: {"level": END, "name": "Potion de Guérison Standard",
#                   "description": "Une potion qui soigne les écorchures"}
#     },
#     NEUTRAL: {"level": END, "name": "Potion raté",
#               "description": "Cette propriété alchimique ne semble pas convenir ici..."}
# }

# MAIN_POTION_TREE = {
#     "level": TOP,
#     EARTH: HEALTH_POTION_TREE,
#     NEUTRAL: {"level": END, "name": "Potion raté",
#               "description": "Cette planète n'est pas appropriée..."}
# }

# ACTIVE_GRAPH = {
#     NEUTRAL: {
#         "neighbours": [
#             {
#                 "name": FIRE,
#                 "weight": [[DRY, HOT], [HOT, DRY]]
#             },
#             {
#                 "name": WATER,
#                 "weight": [[HUMID, COLD], [COLD, HUMID]]
#             },
#             {
#                 "name": GROUND,
#                 "weight": [[DRY, COLD], [COLD, DRY]]
#             },
#             {
#                 "name": AIR,
#                 "weight": [[HOT, HUMID], [HUMID, HOT]]
#             }
#         ]
#     },
#     FIRE: {
#         "neighbours": [
#             {
#                 "name": FIRE,
#                 "weight": [[DRY, HOT], [HOT, DRY]]
#             }
#         ]
#     },
#     WATER: {
#         "neighbours": [
#             {
#                 "name": WATER,
#                 "weight": [[HUMID, COLD], [COLD, HUMID]]
#             }
#         ]
#     },
#     GROUND: {
#         "neighbours": [
#             {
#                 "name": GROUND,
#                 "weight": [[DRY, COLD], [COLD, DRY]]
#             }
#         ]
#     },
#     AIR: {
#         "neighbours": [
#             {
#                 "name": AIR,
#                 "weight": [[HOT, HUMID], [HUMID, HOT]]
#             }
#         ]
#     }
# }


# BASE_ACTIVE_COMPATIBILITY_MATRIX = {
#     HOT: {
#         HOT: 1,
#         COLD: 0,
#         DRY: 1,
#         HUMID: 1,
#         DARK: 1,
#         LIGHT: 1,
#         MINOR: 1,
#         MAJOR: 1,
#         GAS: 1,
#         LIQUID: 1,
#         SOLID: 1,
#     },
#     COLD: {
#         HOT: 0,
#         COLD: 1,
#         DRY: 1,
#         HUMID: 1,
#         DARK: 1,
#         LIGHT: 1,
#         MINOR: 1,
#         MAJOR: 1,
#         GAS: 1,
#         LIQUID: 1,
#         SOLID: 1,
#     },
#     DRY: {
#         HOT: 1,
#         COLD: 1,
#         DRY: 1,
#         HUMID: 0,
#         DARK: 1,
#         LIGHT: 1,
#         MINOR: 1,
#         MAJOR: 1,
#         GAS: 1,
#         LIQUID: 1,
#         SOLID: 1,
#     },
#     HUMID: {
#         HOT: 1,
#         COLD: 1,
#         DRY: 0,
#         HUMID: 1,
#         DARK: 1,
#         LIGHT: 1,
#         MINOR: 1,
#         MAJOR: 1,
#         GAS: 1,
#         LIQUID: 1,
#         SOLID: 1,
#     },
#     DARK: {
#         HOT: 1,
#         COLD: 1,
#         DRY: 1,
#         HUMID: 1,
#         DARK: 1,
#         LIGHT: 0,
#         MINOR: 1,
#         MAJOR: 1,
#         GAS: 1,
#         LIQUID: 1,
#         SOLID: 1,
#     },
#     LIGHT: {
#         HOT: 1,
#         COLD: 1,
#         DRY: 1,
#         HUMID: 1,
#         DARK: 0,
#         LIGHT: 1,
#         MINOR: 1,
#         MAJOR: 1,
#         GAS: 1,
#         LIQUID: 1,
#         SOLID: 1,
#     },
#     MINOR: {
#         HOT: 1,
#         COLD: 1,
#         DRY: 1,
#         HUMID: 1,
#         DARK: 1,
#         LIGHT: 1,
#         MINOR: 1,
#         MAJOR: 0,
#         GAS: 1,
#         LIQUID: 1,
#         SOLID: 1,
#     },
#     MAJOR: {
#         HOT: 1,
#         COLD: 1,
#         DRY: 1,
#         HUMID: 1,
#         DARK: 1,
#         LIGHT: 1,
#         MINOR: 0,
#         MAJOR: 1,
#         GAS: 1,
#         LIQUID: 1,
#         SOLID: 1,
#     },
#     # Now, gas liquid and solid are all non-compatible
#     GAS: {
#         HOT: 1,
#         COLD: 1,
#         DRY: 1,
#         HUMID: 1,
#         DARK: 1,
#         LIGHT: 1,
#         MINOR: 1,
#         MAJOR: 1,
#         GAS: 1,
#         LIQUID: 0,
#         SOLID: 0,
#     },
#     LIQUID: {
#         HOT: 1,
#         COLD: 1,
#         DRY: 1,
#         HUMID: 1,
#         DARK: 1,
#         LIGHT: 1,
#         MINOR: 1,
#         MAJOR: 1,
#         GAS: 0,
#         LIQUID: 1,
#         SOLID: 0,
#     },
#     SOLID: {
#         HOT: 1,
#         COLD: 1,
#         DRY: 1,
#         HUMID: 1,
#         DARK: 1,
#         LIGHT: 1,
#         MINOR: 1,
#         MAJOR: 1,
#         GAS: 0,
#         LIQUID: 0,
#         SOLID: 1,
#     },
# }
