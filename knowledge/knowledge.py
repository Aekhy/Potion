
import pygame
from math import ceil
from utils.texts import TextOutlined
from utils.my_sprite import MySprite
from items.settings import *


class KnowledgeElement():
    def __init__(self, knowledge, data, key, group, x, y, size) -> None:
        self.knowledge = knowledge
        self._id = key
        self._group = group

        self._x = x
        self._y = y
        self._size = size

        self.case, self.img, self.name = None, None, None

        self.MakeCase()
        self.Update(knowledge, data)

    def get_id(self):
        return self._id

    def Update(self, knowledge, data):
        
        if knowledge[self._id]["name"]:
            name = data[self._id]["name"]
        else:
            name = "?"

        if knowledge[self._id]["img"]:
            image_path = data[self._id]["img"]
            if image_path == "":
                image = pygame.Surface(((self._size-32),(self._size-32)))
                image.fill("yellow")
            else:
                image = pygame.image.load(image_path).convert_alpha()
        else:
            # we are supposed to use the default unknown image
            if False:
                pass
            else:
                image = pygame.Surface(((self._size-32),(self._size-32)))
                image.fill("orange")

        self.MakeImg(image)
        self.MakeName(name)

    def MakeCase(self):
        image = pygame.Surface((self._size,self._size))
        image.fill("blue")
        x,y = self._x*self._size , self._y *self._size
        layer = 1
        data = {"type": "case", "id": self._id}
        self.case = MySprite(image,x,y,layer,data,self._group)
  
    def MakeImg(self, new_image):
        if self.img is not None:
            self.img.kill()

        image = new_image
        x,y = self._x *self._size + 16 , self._y *self._size + 16
        layer = 2
        data = None
        self.img = MySprite(image,x,y,layer,data,self._group)

    def MakeName(self, new_name):
        if self.name is not None:
            self.name.kill()

        n_x, n_y = self._x * self._size + 32, self._y * self._size + 3 * 16
        self.name = TextOutlined(n_x, n_y, new_name, 3)
        self.name.add_to_group(self._group)

    



class Knowledge():
    def __init__(self, struct:dict) -> None:
        self._knowledge = struct

        size = 64
        self.grids = {}
        self.grids["ingredient"] = self.MakeGrid(self._knowledge["ingredient"], INGREDIENT_DATA, 0, 128/64, size, 6, 5) 
        self.grids["characteristic"] = self.MakeGrid(self._knowledge["characteristic"], CHARACTERISTIC_DATA, 0, 128/64, size, 6, 5) 
        self.grids["effect"] = self.MakeGrid(self._knowledge["effect"], EFFECT_DATA, 0, 128/64, size, 6, 5) 

        self.grids["base"] = self.MakeGrid(self._knowledge["base"], BASE_DATA, 0, 128/64, size, 6, 5) 
        self.grids["active"] = self.MakeGrid(self._knowledge["active"], ACTIVE_DATA, 0, 128/64, size, 6, 5) 

        self.grids["alchemical_property"] = self.MakeGrid(self._knowledge["alchemical_property"], ALCHEMICAL_PROPERTY_DATA, 0, 128/64, size, 6, 5) 
        self.grids["potion"] = self.MakeGrid(self._knowledge["potion"], POTION_DATA, 0, 128/64, size, 6, 5) 


    # __________ Get & Set __________
    def get_struct(self):
            return self._knowledge


    # __________ Creation __________

    def MakeGrid(self, knowledge, data, x, y, size, nb_rows, nb_cols):
        # dico into array
        nb_pages = ceil(len(data) / (nb_rows * nb_cols))
        res = {}

        """
        {0:
            {
                "id" : {"actual_id": KnowledgeElement}
                "group" : LayeredUpdates           
            },
            {}
        }
        """

        for i in range(0, nb_pages):
            res[i] = {}
            res[i]["id"] = {}
            res[i]["group"] = pygame.sprite.LayeredUpdates()
            
        i = 0 # page
        j = 0 # row
        k = 0 # column
        for key in data.keys():
            if k == nb_cols:
                k = 0
                j += 1
            if j == nb_rows:
                j = 0
                i += 1

            res[i]["id"][key] = KnowledgeElement(knowledge, data, key, res[i]["group"], x+k, y+j, size)

            k += 1

        return res


    # __________ Updates __________
    # ingredient, characteristic, effect, base, active, alchemical_property, potion

    def SearchPage(self, grid_id, id):
        right_page = None
        for page in self.grids[grid_id].keys():
            if id in self.grids[grid_id][page]["id"].keys():
                right_page = page
                break
        return right_page

    def UpdateIngredientKnowledge(self, ingredient_id, *parameters):
        """
        *parameters should be any of : "name", "img", "type", "characteristics", "img", "max_stack"
        "max_stack" is special because it's currently arleady something known
        """
        # the res of the operation
        res = True

        # search for the right page
        right_page = self.SearchPage("ingredient", ingredient_id)

        if right_page is None:
            res = False

        if res:

            # update the knowledge
            for param in parameters:
                self._knowledge["ingredient"][ingredient_id][param] = True

            # update the knowledge element to fit the new knowledge
            self.grids["ingredient"][right_page]["id"][ingredient_id].Update(self._knowledge["ingredient"], INGREDIENT_DATA)

        # DEBUG
        else:
            print("This ingredient was not found in our knowledge grid")

        return res

    def UpdateCharacteristicKnowledge(self, characteristic_id, *parameters, **opposites):
        """
        *parameters shoud be everything but opposites
        *parameters should be any of : "name", "img"
        **opposites should only be opposite as whatever="opposite_name"
        Be careful with the opposites, this function doesn't check if it's the right one(s).
        example : UpdateCharacteristicKnowledge("solide", "name", "img", one="liquide", two="gaz")
        """
        res = True

        # search for the right page
        right_page = self.SearchPage("characteristic", characteristic_id)
        if right_page is None:
            res = False

        if res:
            # update the knowledge
            for param in parameters:
                self._knowledge["characteristic"][characteristic_id][param] = True
            
            for opposite in opposites.keys():
                self._knowledge["characteristic"][characteristic_id]["opposites"][opposites[opposite]] = True

            # update the knowledge element to fit the new knowledge
            self.grids["characteristic"][right_page]["id"][characteristic_id].Update(self._knowledge["characteristic"], CHARACTERISTIC_DATA)

        else:
            print("This characteristic was not found in our knowledge grid")

        return False
    
    def UpdateEffectKnowledge(self, effect_id, *parameters):
        """
        *parameters should be any of : "name", "img", "type"
        """
        # the res of the operation
        res = True

        # search for the right page
        right_page = self.SearchPage("effect", effect_id)

        if right_page is None:
            res = False

        if res:

            # update the knowledge
            for param in parameters:
                self._knowledge["effect"][effect_id][param] = True

            # update the knowledge element to fit the new knowledge
            self.grids["effect"][right_page]["id"][effect_id].Update(self._knowledge["effect"], EFFECT_DATA)

        # DEBUG
        else:
            print("This effect was not found in our knowledge grid")

        return res

    def UpdateBaseKnowledge(self, base_id, *parameters, **neighbours):
        """
        *parameters shoud be everything but neighbours
        *parameters should be any of : "name", "img"
        **neighbours should only be opposite as whatever="neighbours_name"
        Be careful with the neighbours, this function doesn't check if it's the right one(s).
        example : UpdateActiveKnowledge("neutre", "name", "img", one="feu", two="terre")
        """

        # the res of the operation
        res = True

        # search for the right page
        right_page = self.SearchPage("base", base_id)

        if right_page is None:
            res = False

        if res:

            # update the knowledge
            for param in parameters:
                self._knowledge["base"][base_id][param] = True

            for neighbour in neighbours.keys():
                self._knowledge["base"][base_id]["neighbours"][neighbours[neighbour]] = True

            # update the knowledge element to fit the new knowledge
            self.grids["base"][right_page]["id"][base_id].Update(self._knowledge["base"], BASE_DATA)

        # DEBUG
        else:
            print("This base was not found in our knowledge grid")

        return res
    

    def UpdateActiveKnowledge(self, active_id, *parameters, **neighbours):
        """
        *parameters shoud be everything but neighbours
        *parameters should be any of : "name", "img"
        **neighbours should only be opposite as whatever="neighbours_name"
        Be careful with the neighbours, this function doesn't check if it's the right one(s).
        example : UpdateActiveKnowledge("neutre", "name", "img", one="feu", two="air")
        """

        # the res of the operation
        res = True

        # search for the right page
        right_page = self.SearchPage("active", active_id)

        if right_page is None:
            res = False

        if res:

            # update the knowledge
            for param in parameters:
                self._knowledge["active"][active_id][param] = True

            for neighbour in neighbours.keys():
                self._knowledge["active"][active_id]["neighbours"][neighbours[neighbour]] = True

            # update the knowledge element to fit the new knowledge
            self.grids["active"][right_page]["id"][active_id].Update(self._knowledge["active"], ACTIVE_DATA)

        # DEBUG
        else:
            print("This active was not found in our knowledge grid")

        return res

    def UpdateAlchemiclPropertyKnowledge(self, alchemical_property_id, *parameters):
        """
        *parameters should be any of : "name", "img", "base_effect", "active_effect"
        """
        # the res of the operation
        res = True

        # search for the right page
        right_page = self.SearchPage("alchemical_property", alchemical_property_id)

        if right_page is None:
            res = False

        if res:

            # update the knowledge
            for param in parameters:
                self._knowledge["alchemical_property"][alchemical_property_id][param] = True

            # update the knowledge element to fit the new knowledge
            self.grids["alchemical_property"][right_page]["id"][alchemical_property_id].Update(self._knowledge["alchemical_property"], ALCHEMICAL_PROPERTY_DATA)

        # DEBUG
        else:
            print("This alchemical_property was not found in our knowledge grid")

        return res

    def UpdatePotionKnowledge(self, potion_id, *parameters):
        """
        *parameters shoud be everything but neighbours
        *parameters should be any of : "name", "img", "description", "base", "active", "alchemical_property"
        example : UpdatePotionKnowledge("GuerisonStandard", "name", "description", "img", "base", "active", "alchemical_property")
        """
         # the res of the operation
        res = True

        # search for the right page
        right_page = self.SearchPage("potion", potion_id)

        if right_page is None:
            res = False

        if res:

            # update the knowledge
            for param in parameters:
                self._knowledge["potion"][potion_id][param] = True

            # update the knowledge element to fit the new knowledge
            self.grids["potion"][right_page]["id"][potion_id].Update(self._knowledge["potion"], POTION_DATA)

        # DEBUG
        else:
            print("This potion was not found in our knowledge grid")

        return res