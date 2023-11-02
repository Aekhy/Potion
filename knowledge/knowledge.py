
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
        self.case = MySprite(image,x,y,layer,self._group)
  
    def MakeImg(self, new_image):
        if self.img is not None:
            self.img.kill()

        image = new_image
        x,y = self._x *self._size + 16 , self._y *self._size + 16
        layer = 2

        self.img = MySprite(image,x,y,layer,self._group)

    def MakeName(self, new_name):
        if self.name is not None:
            self.name.kill()

        n_x, n_y = self._x * self._size + 32, self._y * self._size + 3 * 16
        self.name = TextOutlined(n_x, n_y, new_name, 3)
        self.name.add_to_group(self._group)



    def set_ready_to_update(self):
        self._ready_to_update = True
    



class Knowledge():
    def __init__(self, struct:dict) -> None:
        self._knowledge = struct

        self.grids = {}
        size = 64
        self.grids["ingredient"] = self.MakeGrid(self._knowledge["ingredient"], INGREDIENT_DATA, 0, 110/64, size, 6, 5) 
        self.grids["characteristic"] = self.MakeGrid(self._knowledge["characteristic"], CHARACTERISTIC_DATA, 0, 110/64, size, 6, 5) 
        self.grids["effect"] = self.MakeGrid(self._knowledge["effect"], EFFECT_DATA, 0, 110/64, size, 6, 5) 

        self.grids["base"] = self.MakeGrid(self._knowledge["base"], BASE_DATA, 0, 110/64, size, 6, 5) 
        self.grids["active"] = self.MakeGrid(self._knowledge["active"], ACTIVE_DATA, 0, 110/64, size, 6, 5) 

        self.grids["alchemical_property"] = self.MakeGrid(self._knowledge["alchemical_property"], ALCHEMICAL_PROPERTY_DATA, 0, 110/64, size, 6, 5) 
        self.grids["potion"] = self.MakeGrid(self._knowledge["potion"], POTION_DATA, 0, 110/64, size, 6, 5) 


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


         
    def get_struct(self):
        return self._knowledge