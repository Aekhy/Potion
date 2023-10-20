from items.settings import *


# ___ base and active ___
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


#____base

BASE_MAX_CHARS = 10

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

#____active

ACTIVE_MAX_CHARS = 10


# 2 steps
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

# ____ alchemical property _____

# SEPARATION = "separation"
# FREEZING = "freezing"
# SOLUTION = "solution"
# INCINERATION = "incineration"
# CALCINATION = "calcination"
# PROJECTION = "projection"

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