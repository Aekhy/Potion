from items.settings import *
from utils.json_functions import Read, Write
from knowledge.knowledge import Knowledge
from inventory.game_inventory import GameInventory
from items.potions import Base, Active, Potion

INGREDIENTS = "ingredient"
CHARACTERISITC_COMPATIBILITY = "characteristic_compatibility"
EFFECT = "effect"
BASE = "base"
ACTIVE = "active"
ALCHEMICAL_PROPERTY = "alchemical_property"
POTION = "potion"

class SaveManager:
    def __init__(self, game) -> None:
        self._game = game
        self._dirname = None
        self._saved = True

    def Load(self, path, MakeFunction):
        try:
            res = Read(path)
        except:
            res = MakeFunction(path)
        return res

    def MakeClasses(self):
        self._game.knowledge = Knowledge(self._knowledge_strut)
        self._game.game_inventory = GameInventory(self._game_inventory_struct, 0, 50)

    def LoadSave(self, dirname):
        self._dirname = dirname
        path_knowledge = self._dirname + "/" + "current_knowledge.json"
        self._knowledge_strut = self.Load(path_knowledge, self.MakeAllDefaultKnowledge)
        path_game_inv = self._dirname + "/" + "game_inventory.json"
        self._game_inventory_struct = self.Load(path_game_inv, self.MakeDefaultGameInventoryLayout)

        self.MakeClasses()
        self._saved = False

    def Save(self):
        if not self._saved:
            k_struct = self._game.knowledge.get_struct()
            Write(self._dirname + "/" + "current_knowledge.json", k_struct)
            g_i_struct = self.get_GameInventoryLayout()
            Write(self._dirname + "/" + "game_inventory.json", g_i_struct)

            self._saved = True

            # clear the game
            self._game.knowledge = None
            self._game.game_inventory = None


    # Knowledge

    # Private
    def MakeIngredientDefaultKnowledge(self):
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

    # Private
    def MakeIngredientCharacterisicCompatibilityDefaultKnowledge(self):
        IngredientCompatibility_data = BASE_ACTIVE_COMPATIBILITY_MATRIX
        IngredientCompatibilityCharacterisic_knowledge = {}
        for cara, value in IngredientCompatibility_data.items():
            tmp = {}
            for k in value.keys():
                tmp[k] = False
            IngredientCompatibilityCharacterisic_knowledge[cara] = tmp
        return IngredientCompatibilityCharacterisic_knowledge

    # Private
    def ListToKnowledge(self, l:list, d:dict):
        lst = l
        lst_knowledge = {}
        for el in lst:
            lst_knowledge[el] = d
        return lst_knowledge

    # Private
    def GraphToKnowledge(self, graph):
        g_data = graph
        g_knowledge = {}
        for g_key, value in g_data.items():
            g_key_knowledge = {}
            for neighbour in value["neighbours"]:
                g_key_knowledge[neighbour["name"]] = {"name" : False, "weight": False}
            g_knowledge[g_key] = g_key_knowledge
        return g_knowledge

    # Private
    def MakeEffectDefaultKnowledge(self):
        l = [HEATING, FREEZING, MIXING, DISTILLATION, SUBLIMATION, FERMENTATION]
        d = {"name": False, "type": False}
        return self.ListToKnowledge(l, d)
    
    # Private
    def MakeAlchemicalPropertyDefaultKnowledge(self):
        l = [SPELL, CHARM, TRANSFIGURATION, HEX, BEWITCHMENT, CURSE, COUNTER_SPELL, ENCHANTMENT, BLESSING]
        d = {"name": False, "base_effect": False, "active_effect": False}
        return self.ListToKnowledge(l, d)

    # Private
    def MakeBaseDefaultKnowledge(self):
        return self.GraphToKnowledge(BASE_GRAPH)

    # Private
    def MakeActiveDefaultKnowledge(self):
        return self.GraphToKnowledge(ACTIVE_GRAPH)

    # Private
    def MakePotionDefaultKnowledge(self):
        p_data = POTION_DATA
        p_knowledge = {}
        for key, value in p_data.items():
            tmp = {}
            for k in value.keys():
                tmp[k] = False
            p_knowledge[key] = tmp
        return p_knowledge

    # Public ~ kinda
    def MakeAllDefaultKnowledge(self, knowledge_path):
        knowledge = {}
        knowledge[INGREDIENTS] = self.MakeIngredientDefaultKnowledge()
        knowledge[CHARACTERISITC_COMPATIBILITY] = self.MakeIngredientCharacterisicCompatibilityDefaultKnowledge()
        knowledge[EFFECT] = self.MakeEffectDefaultKnowledge()
        knowledge[BASE] = self.MakeBaseDefaultKnowledge()
        knowledge[ACTIVE] = self.MakeActiveDefaultKnowledge()
        knowledge[ALCHEMICAL_PROPERTY] = self.MakeAlchemicalPropertyDefaultKnowledge()
        knowledge[POTION] = self.MakePotionDefaultKnowledge()

        Write(knowledge_path, knowledge)
        return knowledge
    

    # Game Inventory 

    def MakeDefaultGameInventoryLayout(self, path):
        res = {
            "ingredients":{
                "meta":{"number":4, "nb_row": 6, "nb_col" : 5}
            },
            "mixtures":{
                "meta":{"number":3, "nb_row": 6, "nb_col" : 5}
            },
            "potions":{
                "meta":{"number":2, "nb_row": 6, "nb_col" : 5}
            }
        }

        for key, value in res.items():

            for i in range(0, value["meta"]["number"]):
                res[key][str(i)] = []
                for j in range(0, value["meta"]["nb_row"]):
                    d_row = []
                    for k in range(0, value["meta"]["nb_col"]):
                        if i==0 and j==0 and k == 0 and key == "ingredients":
                            tmp = {"type":"Slot","item_type": "ingredient","item_data":"eau","quantity":5}
                        else:
                            tmp = {"type":"Slot"}
                        d_row.append(tmp)
                    res[key][str(i)].append(d_row)

        Write(path, res)
        return res
    
    def get_GameInventoryLayout(self):
        s = self._game.game_inventory._struct

        res = {
            "ingredients":{
                "meta":{"number":4, "nb_row": 6, "nb_col" : 5}
            },
            "mixtures":{
                "meta":{"number":3, "nb_row": 6, "nb_col" : 5}
            },
            "potions":{
                "meta":{"number":2, "nb_row": 6, "nb_col" : 5}
            }
        }

        index = 0
        for key, value in s.items():
            
            for i in range(0, value["meta"]["number"]):
                multiple_inv = self._game.game_inventory._multiple_inventories[index]
                inv_dict = multiple_inv._inventories[i]

                inv = inv_dict["inventory"]
                s_l = inv.slot_list
                res[key][str(i)] = []
                for j in range(0, value["meta"]["nb_row"]):
                    d_row = []
                    for k in range(0, value["meta"]["nb_col"]):
                        slot = s_l[k + j*value["meta"]["nb_col"]]
                        if not slot.is_empty:
                            item = slot.item
                            tmp = {"type":"Slot"}
                            if isinstance(item, Base):
                                tmp["item_type"] = "base"
                                tmp["item_data"] = item.get_info_save()
                            elif isinstance(item, Active):
                                tmp["item_type"] = "base"
                                tmp["item_data"] = item.get_info_save()
                            elif isinstance(item, Potion):
                                tmp["item_type"] = "potion"
                                tmp["item_data"] = slot.item.get_info_save()
                            else:
                                tmp["item_type"] = "ingredient"
                                tmp["item_data"] = item.name
                            tmp["quantity"] = slot.quantity
                        else:
                            tmp = {"type":"Slot"}
                        d_row.append(tmp)
                    res[key][str(i)].append(d_row)
            index += 1

        return res