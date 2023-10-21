DEFAULT_MAX_STACK = 10

DEFAULT_POTION_MAX_STACK = 3





#__________ Ingredients __________
DEFAULT_INGREDIENT_MAX_STACK = 5
# path relative to where we call the class Ingredient.
# it's actually the path that works for all file that are at the same level as main
INGREDIENT_DATA_PATH = "items/ingredients.json"
#-- characteristics --
# used
HOT = "chaud"
COLD = "froid"
DRY = "sec"
HUMID = "humide"
DARK = "sombre"
LIGHT = "lumineux"
GAS = "gaz"
MINOR = "mineur"
MAJOR = "majeur"
LIQUID = "liquide"
SOLID = "solide"
# not used 
PHYSIC = "physique"
PSYCHIC = "psychique"


#_________ BASE ACTIVE ________

# types
BASE = "base"
ACTIVE = "actif"

# base & active
NEUTRAL = "neutre"

BASE_ACTIVE_COMPATIBILITY_MATRIX = {
    HOT : {
        HOT : 1,
        COLD : 0,
        DRY : 1,
        HUMID : 1,
        DARK : 1,
        LIGHT : 1,
        MINOR : 1,
        MAJOR : 1,
        GAS : 1,
        LIQUID : 1,
        SOLID : 1,
    },
    COLD : {
        HOT : 0,
        COLD : 1,
        DRY : 1,
        HUMID : 1,
        DARK : 1,
        LIGHT : 1,
        MINOR : 1,
        MAJOR : 1,
        GAS : 1,
        LIQUID : 1,
        SOLID : 1,
    },
    DRY : {
        HOT : 1,
        COLD : 1,
        DRY : 1,
        HUMID : 0,
        DARK : 1,
        LIGHT : 1,
        MINOR : 1,
        MAJOR : 1,
        GAS : 1,
        LIQUID : 1,
        SOLID : 1,
    },
    HUMID : {
        HOT : 1,
        COLD : 1,
        DRY : 0,
        HUMID : 1,
        DARK : 1,
        LIGHT : 1,
        MINOR : 1,
        MAJOR : 1,
        GAS : 1,
        LIQUID : 1,
        SOLID : 1,
    },
    DARK : {
        HOT : 1,
        COLD : 1,
        DRY : 1,
        HUMID : 1,
        DARK : 1,
        LIGHT : 0,
        MINOR : 1,
        MAJOR : 1,
        GAS : 1,
        LIQUID : 1,
        SOLID : 1,
    },
    LIGHT : {
        HOT : 1,
        COLD : 1,
        DRY : 1,
        HUMID : 1,
        DARK : 0,
        LIGHT : 1,
        MINOR : 1,
        MAJOR : 1,
        GAS : 1,
        LIQUID : 1,
        SOLID : 1,
    },
    MINOR : {
        HOT : 1,
        COLD : 1,
        DRY : 1,
        HUMID : 1,
        DARK : 1,
        LIGHT : 1,
        MINOR : 1,
        MAJOR : 0,
        GAS : 1,
        LIQUID : 1,
        SOLID : 1,
    },
    MAJOR : {
        HOT : 1,
        COLD : 1,
        DRY : 1,
        HUMID : 1,
        DARK : 1,
        LIGHT : 1,
        MINOR : 0,
        MAJOR : 1,
        GAS : 1,
        LIQUID : 1,
        SOLID : 1,
    },
    # Now, gas liquid and solid are all non-compatible
    GAS : {
        HOT : 1,
        COLD : 1,
        DRY : 1,
        HUMID : 1,
        DARK : 1,
        LIGHT : 1,
        MINOR : 1,
        MAJOR : 1,
        GAS : 1,
        LIQUID : 0,
        SOLID : 0,
    },
    LIQUID : {
        HOT : 1,
        COLD : 1,
        DRY : 1,
        HUMID : 1,
        DARK : 1,
        LIGHT : 1,
        MINOR : 1,
        MAJOR : 1,
        GAS : 0,
        LIQUID : 1,
        SOLID : 0,
    },
    SOLID : {
        HOT : 1,
        COLD : 1,
        DRY : 1,
        HUMID : 1,
        DARK : 1,
        LIGHT : 1,
        MINOR : 1,
        MAJOR : 1,
        GAS : 0,
        LIQUID : 0,
        SOLID : 1,
    },
}


# base

SUN = "soleil"
MERCURY = "mercure"
VENUS = "venus"
EARTH = "terre"
MOON = "lune"
MARS =  "mars"
JUPITER = "jupiter"
SATURN = "saturne"
URANUS = "uranus"
NEPTUNE = "neptune"

BASE_GRAPH = {
    NEUTRAL : {
        "neighbours" : [
            {
                "name" : SUN,
                "weight" : [[MAJOR, GAS],[GAS, MAJOR]]
            },
            {
                "name" : EARTH,
                "weight" : [[LIQUID, LIGHT],[LIGHT, LIQUID]]
            }
        ]    
    },
    SUN : {
        "neighbours" : [
            {
                "name" : SUN,
                "weight" : [[MAJOR, GAS],[GAS, MAJOR]]
            }
        ]
    },
    EARTH : {
        "neighbours" : [
            {
                "name" : EARTH,
                "weight" : [[LIQUID, LIGHT],[LIGHT, LIQUID]]
            }
        ]
    }
}

# active

FIRE = "feu"
WATER = "eau"
GROUND = "terre"
AIR = "air"

ACTIVE_GRAPH = {
    NEUTRAL : {
        "neighbours": [
            {
                "name" : FIRE,
                "weight" : [[DRY, HOT],[HOT, DRY]]
            },
            {
                "name" : WATER,
                "weight" : [[HUMID, COLD],[COLD, HUMID]]
            },
            {
                "name" : GROUND,
                "weight" : [[DRY, COLD],[COLD, DRY]]
            },
            {
                "name" : AIR,
                "weight" : [[HOT, HUMID],[HUMID, HOT]]
            }
        ]
    },
    FIRE : {
        "neighbours": [
            {
                "name" : FIRE,
                "weight" : [[DRY, HOT],[HOT, DRY]]
            }
        ]
    },
    WATER: {
        "neighbours": [
            {
                "name" : WATER,
                "weight" : [[HUMID, COLD],[COLD, HUMID]]
            }
        ]
    },
    GROUND : {
        "neighbours": [
            {
                "name" : GROUND,
                "weight" : [[DRY, COLD],[COLD, DRY]]
            }
        ]
    },
    AIR : {
        "neighbours": [
            {
                "name" : AIR,
                "weight" : [[HOT, HUMID],[HUMID, HOT]]
            }
        ]
    }
}

# alchemical property 

NOTHING = "rien"

HEATING = "chauffer"
FREEZING = "geler"
MIXING = "mixer"

# neutral
DISTILLATION = "distillation"
# bad
FERMENTATION = "fermentation"
# good
SUBLIMATION = "sublimation"


# neutral -> distillation
SPELL = "sortilège"
CHARM = "charme"
TRANSFIGURATION = "transfiguration"

# bad -> fermentation
HEX = "maléfice"
BEWITCHMENT = "ensorcellement"
CURSE = "malédiction"

# good -> sublimation
COUNTER_SPELL = "contre-sort" 
ENCHANTMENT = "enchantement"
BLESSING = "bénédiction"


ALCHEMICAL_PROPERTY_MATRIX = {
    NOTHING : {
        NOTHING : NOTHING,
        FERMENTATION : NOTHING,
        DISTILLATION : NOTHING,
        SUBLIMATION : NOTHING,
    },
    HEATING : {
        NOTHING : NOTHING,
        FERMENTATION : HEX,
        DISTILLATION : SPELL,
        SUBLIMATION : COUNTER_SPELL,
    },
    FREEZING : {
        NOTHING : NOTHING,
        FERMENTATION : BEWITCHMENT,
        DISTILLATION : CHARM,
        SUBLIMATION : ENCHANTMENT
    },
    MIXING : {
        NOTHING : NOTHING,
        FERMENTATION : CURSE,
        DISTILLATION : TRANSFIGURATION,
        SUBLIMATION : BLESSING
    },
    
}

#__________ Potions __________
#levels
TOP = 3
MIDDLE = 2
BOTTOM = 1
END = 0

HEALTH_POTION_TREE = {
    "level" : MIDDLE,
    "name" : "santé ",
    CHARM : 
    {
        "level" : BOTTOM,
        "name" : "régénération",
        WATER : {"level": END, "name" : "AquaVivacité",  "description": "Effet lent mais fort."},
        FIRE : {"level": END, "name" : "PyroRenouveau", "description": "Effet rapide mais faible."},
        NEUTRAL : {"level": END, "name" : "Potion de Guérison Standard", "description": "Une potion qui soigne les écorchures"}
    },
    TRANSFIGURATION : 
    {
        "level": BOTTOM,
        "name": "taille", 
        NEUTRAL : {"level": END, "name" : "Potion de Guérison Standard", "description": "Une potion qui soigne les écorchures"}
    },
    NEUTRAL : {"level": END, "name" : "Mixture étrange", "description": "Cette propriété alchimique ne semble pas convenir ici..."} 
}


MAIN_POTION_TREE = {
    "level" : TOP,
    EARTH : HEALTH_POTION_TREE,
    NEUTRAL : {"level": END, "name" : "Mixture étrange", "description": "Cette planète n'est pas appropriée..."}
}

