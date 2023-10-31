from items.settings import *
from utils.json_functions import Read, Write

INGREDIENTS = "ingredient"
CHARACTERISITC_COMPATIBILITY = "characteristic_compatibility"
EFFECT = "effect"
BASE = "base"
ACTIVE = "active"
ALCHEMICAL_PROPERTY = "alchemical_property"
POTION = "potion"

PATH = "knowledge/knowledge.json"

"""
{
    "ingredient":{
    
    },
    "characteristic_compatibility":{
    
    },
    "effect":{
        chauffer : {name: false, type: false}
    }
    "base":{
    
    },
    "active":{
    
    },
    "alchemical_property":{
    
    },
    "potion":{
        "AquaVivacité":{
            "name": false,
            "description": false,
            "base": false,
            "active": false,
            "alchemical_property": false
        }
    }
}
"""

def MakeIngredientDefaultKnowledge():
    ingredient_data = INGREDIENT_DATA

    ingredient_knowledge = {}
    for ingredient, value in ingredient_data.items():
        key_knowledge = {}
        for key in value.keys():
            tmp = False
            if key == "max_stack":
                tmp = True
            key_knowledge[key] = tmp
        ingredient_knowledge[ingredient] = key_knowledge
    return ingredient_knowledge

def MakeIngredientCharacterisicCompatibilityDefaultKnowledge():
    IngredientCompatibility_data = BASE_ACTIVE_COMPATIBILITY_MATRIX
    IngredientCompatibilityCharacterisic_knowledge = {}
    for cara, value in IngredientCompatibility_data.items():
        tmp = {}
        for k in value.keys():
            tmp[k] = False
        IngredientCompatibilityCharacterisic_knowledge[cara] = tmp
    return IngredientCompatibilityCharacterisic_knowledge

def ListToKnowledge(l:list,d:dict):
    lst = l
    lst_knowledge = {}
    for el in lst:
        lst_knowledge[el] = d
    return lst_knowledge

def MakeEffectDefaultKnowledge():
    l = [HEATING, FREEZING, MIXING, DISTILLATION, SUBLIMATION, FERMENTATION]
    d = {"name": False, "type": False}
    return ListToKnowledge(l, d)

def MakeAlchemicalPropertyDefaultKnowledge():
    l = [SPELL, CHARM, TRANSFIGURATION, HEX, BEWITCHMENT, CURSE, COUNTER_SPELL, ENCHANTMENT, BLESSING]
    d = {"name": False, "base_effect": False, "active_effect": False}
    return ListToKnowledge(l, d)


def GraphToKnowledge(graph):
    g_data = graph
    g_knowledge = {}
    for g_key, value in g_data.items():
        g_key_knowledge = {}
        for neighbour in value["neighbours"]:
            g_key_knowledge[neighbour["name"]] = {"name" : False, "weight": False}

        g_knowledge[g_key] = g_key_knowledge
    return g_knowledge

def MakeBaseDefaultKnowledge():
    return GraphToKnowledge(BASE_GRAPH)

def MakeActiveDefaultKnowledge():
    return GraphToKnowledge(ACTIVE_GRAPH)


def MakePotionDefaultKnowledge():
    return POTION

def MakeAllDefaultKnowledge():
    knowledge = {}
    knowledge[INGREDIENTS] = MakeIngredientDefaultKnowledge()
    knowledge[CHARACTERISITC_COMPATIBILITY] = MakeIngredientCharacterisicCompatibilityDefaultKnowledge()
    knowledge[EFFECT] = MakeEffectDefaultKnowledge()
    knowledge[BASE] = MakeBaseDefaultKnowledge()
    knowledge[ACTIVE] = MakeActiveDefaultKnowledge()
    knowledge[ALCHEMICAL_PROPERTY] = MakeAlchemicalPropertyDefaultKnowledge()
    knowledge[POTION] = MakePotionDefaultKnowledge()

    Write(PATH, knowledge)
