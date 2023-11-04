from items.settings import *
from utils.json_functions import Read, Write
from knowledge.knowledge import Knowledge
from inventory.game_inventory import GameInventory
from items.potions import Base, Active, Potion

KNOW_ALL = True

INGREDIENTS = "ingredient"
CHARACTERISITC = "characteristic"
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


    def LoadSave(self, dirname):
        self._dirname = dirname
        path_knowledge = self._dirname + "/" + "current_knowledge.json"
        self._knowledge_strut = self.Load(path_knowledge, self.MakeAllDefaultKnowledge)
        self._game.knowledge = Knowledge(self._knowledge_strut)

        path_game_inv = self._dirname + "/" + "game_inventory.json"
        self._game_inventory_struct = self.Load(path_game_inv, self.MakeDefaultGameInventoryLayout)
        self._game.game_inventory = GameInventory(self._game_inventory_struct, 0, 64)

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
                tmp = KNOW_ALL
                if key == "max_stack":
                    tmp = True
                key_knowledge[key] = tmp
            ingredient_knowledge[ingredient] = key_knowledge
        return ingredient_knowledge

    # Private
    def MakeCharacterisicDefaultKnowledge(self):
        IngredientCompatibility_data = CHARACTERISTIC_DATA
        IngredientCompatibility_knowledge = {}
        for cara, value in IngredientCompatibility_data.items():
            tmp = {}
            for k in value.keys():
                tmp[k] = KNOW_ALL
                if k == "opposites":
                    tmp[k] = {}
                    for opp in value[k]:
                        tmp[k][opp] = KNOW_ALL
            IngredientCompatibility_knowledge[cara] = tmp
        return IngredientCompatibility_knowledge

    # Private
    # def ListToKnowledge(self, l:list, d:dict):
    #     lst = l
    #     lst_knowledge = {}
    #     for el in lst:
    #         lst_knowledge[el] = d
    #     return lst_knowledge

    # # Private
    # def GraphToKnowledge(self, graph):
    #     g_data = graph
    #     g_knowledge = {}
    #     for g_key, value in g_data.items():
    #         g_key_knowledge = {}
    #         for neighbour in value["neighbours"]:
    #             g_key_knowledge[neighbour["name"]] = {"name" : False, "weight": False}
    #         g_knowledge[g_key] = g_key_knowledge
    #     return g_knowledge

    # Private
    def MakeEffectDefaultKnowledge(self):
        effect_data = EFFECT_DATA

        effect_knowledge = {}
        for ingredient, value in effect_data.items():
            key_knowledge = {}
            for key in value.keys():
                key_knowledge[key] = KNOW_ALL
            effect_knowledge[ingredient] = key_knowledge
        return effect_knowledge
    
    # Private
    def MakeAlchemicalPropertyDefaultKnowledge(self):
        a_p_data = ALCHEMICAL_PROPERTY_DATA
        a_p_knowledge = {}
        for key, value in a_p_data.items():
            tmp = {}
            for k in value.keys():
                tmp[k] = KNOW_ALL
            a_p_knowledge[key] = tmp
        return a_p_knowledge

    # Private
    def MakeBaseDefaultKnowledge(self):
        base_data = BASE_DATA
        base_knowledge = {}
        for key, value in base_data.items():
            tmp = {}
            for k in value.keys():
                if k == "neighbours":
                    tmp[k] = {}
                    for neighbour in value[k]:
                        # if neighbour["id_name"] == "":
                        #     tmp[k][neighbour["id_name"]] = False
                        # else:
                        #     tmp[k][neighbour["id_name"]] = KNOW_ALL
                        tmp[k][neighbour["id_name"]] = KNOW_ALL
                else:
                    tmp[k] = KNOW_ALL
            base_knowledge[key] = tmp
        return base_knowledge

    # Private
    def MakeActiveDefaultKnowledge(self):
        active_data = ACTIVE_DATA
        active_knowledge = {}
        for key, value in active_data.items():
            tmp = {}
            for k in value.keys():
                if k == "neighbours":
                    tmp[k] = {}
                    for neighbour in value[k]:
                        tmp[k][neighbour["id_name"]] = KNOW_ALL
                else:
                    tmp[k] = KNOW_ALL
            active_knowledge[key] = tmp
        return active_knowledge

    # Private
    def MakePotionDefaultKnowledge(self):
        
        p_data = POTION_DATA
        p_knowledge = {}
        for key, value in p_data.items():
            tmp = {}
            for k in value.keys():
                tmp[k] = KNOW_ALL
            p_knowledge[key] = tmp

        return p_knowledge

    # Public ~ kinda
    def MakeAllDefaultKnowledge(self, knowledge_path):
        knowledge = {}
        knowledge[INGREDIENTS] = self.MakeIngredientDefaultKnowledge()
        knowledge[CHARACTERISITC] = self.MakeCharacterisicDefaultKnowledge()
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
                                tmp["item_data"] = item.get_info_save()
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