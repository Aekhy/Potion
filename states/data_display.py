from utils.texts import TextOutlined
from utils.my_sprite import MySprite
from items.settings import *
import pygame

class DataDisplay:
    def __init__(self, knowledge, data, sprites_group, x, y, tilesize) -> None:
        self._knowledge = knowledge
        self._data = data
        self._group = sprites_group
        self._x = x 
        self._y = y
        self._tilesize = tilesize
    
        self.MakeImg()
        self.MakeName()

    def MakeName(self):
        if self._knowledge["name"]:
            self._name_text = self._data["name"]
        else:
            self._name_text = "?"
        
        self._name_x = self._x + self._tilesize * 2
        self._name_y = self._y + self._tilesize * 3/2
        self._name_layer = 1

        self._name_sprite = TextOutlined(self._name_x, self._name_y, self._name_text, self._name_layer)
        self._name_sprite.add_to_group(self._group)


    def MakeImg(self):
        if self._knowledge["img"]:
            self._image_path = self._data["img"]
        else:
            self._image_path = None

        
        if self._image_path == "":
            self._image_surface = pygame.Surface(((self._tilesize-32),(self._tilesize-32)))
            self._image_surface.fill("yellow")
        elif self._image_path is not None:
            self.image_surface = pygame.image.load(self._image_path).convert_alpha()
        else:
            # we are supposed to use the default unknown image
            if False:
                pass
            else:
                self._image_surface = pygame.Surface(((self._tilesize-32),(self._tilesize-32)))
                self._image_surface.fill("orange")

        self._image_x = self._x  + self._tilesize * 2
        self._image_y = self._y  + self._tilesize / 2
        self._image_layer = 1

        self._image_sprite = MySprite(self._image_surface, self._image_x, self._image_y, self._image_layer, None, self._group)
        self._image_sprite.rect.center = (self._image_x, self._image_y)


    def MakeEasySpriteText(self, coeff_x, coeff_y, text, layer):
        easy_x = self._x  + self._tilesize * coeff_x
        easy_y = self._y + self._tilesize * coeff_y
        easy_text = text
        easy_layer = layer
        easy_sprite = TextOutlined(easy_x, easy_y, easy_text, easy_layer)
        easy_sprite.add_to_group(self._group)
        return easy_sprite
    
    def MakeEasyImage(self, coeff_x, coeff_y, image_path, layer):
        # DEV
        if image_path == "":
            image_surface = pygame.Surface(((self._tilesize-32),(self._tilesize-32)))
            image_surface.fill("yellow")
        else:
            image_surface = pygame.image.load(image_path).convert_alpha()

        image = MySprite(image_surface,  
                            0, 
                            0, 
                            layer, 
                            None, 
                            self._group)
        
        image.rect.center = (self._x  + self._tilesize * coeff_x,self._y  + self._tilesize * coeff_y)
        return image
    
    def MakeEasySpriteList(self, coeff_y, id, data):
        sprite_list = []
        x = 1
        for key, value in self._knowledge[id].items():
            if value:
                img = self.MakeEasyImage(x, coeff_y, data[key]["img"], 0)
                text = self.MakeEasySpriteText(x, coeff_y, data[key]["name"], 1)
                sprite_list.append(img)
            else:
                text = self.MakeEasySpriteText(x, 6/2, "?", 1)
            sprite_list.append(text)
            x += 1
            
        return sprite_list
    
    def kill(self):
        self._image_sprite.kill()
        self._name_sprite.kill()

        
class IngredientDisplay(DataDisplay):
    def __init__(self, knowledge, data, sprites_group, x, y, tilesize) -> None:
        super().__init__(knowledge, data, sprites_group, x, y, tilesize)

        self._type_sprite = self.MakeEasySpriteText(2, 5/2, "Type :", 1)

        self._characteristics_sprite = self.MakeEasySpriteText(2, 7/2, "Caractéristiques :", 1)

        self._max_stack_sprite = self.MakeEasySpriteText(2, 9/2, "Quantité maximale de stack :", 1)

        # TO DO -> Complet the sprites bases on knowledge and data 
        if self._knowledge["type"]:
            if self._data["type"] == ID["base"]:
                t = "Astral"
            else:
                t = "Elementaire"
            self._known_type_sprite = self.MakeEasySpriteText(2, 6/2, t, 1)
        else:
            self._unknown_type_sprite = self.MakeEasySpriteText(2, 6/2, "?", 1)


        if self._knowledge["characteristics"]:
            self._known_characteristics_sprite_liste = []
            x = 1
            for chara in self._data["characteristics"]:
                img = self.MakeEasyImage(x, 8/2, CHARACTERISTIC_DATA[chara]["img"], 0)
                text = self.MakeEasySpriteText(x, 8/2, CHARACTERISTIC_DATA[chara]["name"], 1) 

                self._known_characteristics_sprite_liste.append(img)
                self._known_characteristics_sprite_liste.append(text)
                
                x += 1

        else:
            self._unknown_characteristics_sprite = self.MakeEasySpriteText(2, 8/2, "?", 1)


        if self._knowledge["max_stack"]:
            self._known_max_stack_sprite = self.MakeEasySpriteText(2, 10/2, self._data["max_stack"], 1)
        else:
            self._unknown_max_stack_sprite = self.MakeEasySpriteText(2, 10/2, "?", 1)

    def kill(self):
        self._image_sprite.kill()
        self._name_sprite.kill()
        self._type_sprite.kill()
        self._characteristics_sprite.kill()
        self._max_stack_sprite.kill()

        if self._knowledge["type"]:
            self._known_type_sprite.kill()
        else:
            self._unknown_type_sprite.kill()

        if self._knowledge["characteristics"]:
            for sprite in self._known_characteristics_sprite_liste:
                sprite.kill()
        else:
            self._unknown_characteristics_sprite.kill()

        if self._knowledge["max_stack"]:
            self._known_max_stack_sprite.kill()
        else:
            self._unknown_max_stack_sprite.kill()

class CharacteristicDisplay(DataDisplay):
    def __init__(self, knowledge, data, sprites_group, x, y, tilesize) -> None:
        super().__init__(knowledge, data, sprites_group, x, y, tilesize)

        self._opposites_sprite = self.MakeEasySpriteText(2, 5/2, "Caractéristiques opposée(s) :", 1)

        # TO DO -> Complet the sprites bases on knowledge and data
        self._opposites_sprite_list = self.MakeEasySpriteList(6/2, "opposites", CHARACTERISTIC_DATA)

    def kill(self):
        self._image_sprite.kill()
        self._name_sprite.kill()
        self._opposites_sprite.kill()
        for opposite in self._opposites_sprite_list:
            opposite.kill()

class EffectDisplay(DataDisplay):
    def __init__(self, knowledge, data, sprites_group, x, y, tilesize) -> None:
        super().__init__(knowledge, data, sprites_group, x, y, tilesize)

        self._type_sprite = self.MakeEasySpriteText(2, 5/2, "Type de mixture adaptée :", 1)

        # TO DO -> Complet the sprites bases on knowledge and data 
        if self._knowledge["type"]:
            if self._data["type"] == ID["base"]:
                t = "Mixture Astrale"
            else:
                t = "Mixture Elémentaire"
            self._know_type_sprite = self.MakeEasySpriteText(2, 6/2, t, 1)
        else:
            self._unknown_type_sprite = self.MakeEasySpriteText(2, 6/2, "?", 1)

    def kill(self):
        self._image_sprite.kill()
        self._name_sprite.kill()
        self._type_sprite.kill()
        if self._knowledge["type"]:
            self._know_type_sprite.kill()
        else:
            self._unknown_type_sprite.kill()

class BaseDisplay(DataDisplay):
    def __init__(self, knowledge, data, sprites_group, x, y, tilesize) -> None:
        super().__init__(knowledge, data, sprites_group, x, y, tilesize)

        self._neighbours_sprite = self.MakeEasySpriteText(2, 5/2, "Planètes proches :", 1)

        # TO DO -> Complet the sprites bases on knowledge and data 
        self._neighbours_sprite_list = self.MakeEasySpriteList(6/2, "neighbours", BASE_DATA)

    def kill(self):
        self._image_sprite.kill()
        self._name_sprite.kill()
        self._neighbours_sprite.kill()
        for sprite in self._neighbours_sprite_list:
            sprite.kill()
class ActiveDisplay(DataDisplay):
    def __init__(self, knowledge, data, sprites_group, x, y, tilesize) -> None:
        super().__init__(knowledge, data, sprites_group, x, y, tilesize)

        self._neighbours_sprite = self.MakeEasySpriteText(2, 5/2, "Eléments proches :", 1)

        # TO DO -> Complet the sprites bases on knowledge and data 
        self._neighbours_sprite_list = self.MakeEasySpriteList(6/2, "neighbours", ACTIVE_DATA)

    def kill(self):
        self._image_sprite.kill()
        self._name_sprite.kill()
        self._neighbours_sprite.kill()
        for sprite in self._neighbours_sprite_list:
            sprite.kill()

class AlchemicalPropertyDisplay(DataDisplay):
    def __init__(self, knowledge, data, sprites_group, x, y, tilesize) -> None:
        super().__init__(knowledge, data, sprites_group, x, y, tilesize)

        self._base_effect_sprite = self.MakeEasySpriteText(2, 5/2, "Effet de la mixture Astrale :", 1)

        # TO DO -> Complet the sprites bases on knowledge and data
        self._base_sprite_list = []
        if self._knowledge["base_effect"]:
            img = self.MakeEasyImage(0, 6/2, EFFECT_DATA[self._data["base_effect"]]["img"], 0)
            text = self.MakeEasySpriteText(0, 6/2, EFFECT_DATA[self._data["base_effect"]]["name"], 1)
            self._base_sprite_list.append(img)
        else:
            text = self.MakeEasySpriteText(0, 6/2, "?", 1)

        self._base_sprite_list.append(text)


        self._active_effect_sprite = self.MakeEasySpriteText(2, 7/2, "Effet de la mixture Elémentaire :", 1)
        
        # TO DO -> Complet the sprites bases on knowledge and data 
        self._active_sprite_list = []
        if self._knowledge["active_effect"]:
            img = self.MakeEasyImage(0, 8/2, EFFECT_DATA[self._data["active_effect"]]["img"], 0)
            text = self.MakeEasySpriteText(0, 8/2, EFFECT_DATA[self._data["active_effect"]]["name"], 1)
            self._active_sprite_list.append(img)
        else:
            text = self.MakeEasySpriteText(0, 8/2, "?", 1)
        self._active_sprite_list.append(text)

    def kill(self):
        self._image_sprite.kill()
        self._name_sprite.kill()
        self._base_effect_sprite.kill()
        self._active_effect_sprite.kill() 
        for sprite in self._base_sprite_list:
            sprite.kill()
        for sprite in self._active_sprite_list:
            sprite.kill()

class PotionDisplay(DataDisplay):
    def __init__(self, knowledge, data, sprites_group, x, y, tilesize) -> None:
        super().__init__(knowledge, data, sprites_group, x, y, tilesize)

        self._description_sprite = self.MakeEasySpriteText(2, 5/2, "Description :", 1)

        # TO DO -> Complet the sprites bases on knowledge and data
        if self._knowledge["description"]:
            self._known_description_sprite = self.MakeEasySpriteText(2, 6/2, self._data["description"], 1)
        else:
            self._unknown_description_sprite = self.MakeEasySpriteText(2, 6/2, "?", 1)


        self._base_sprite = self.MakeEasySpriteText(2, 7/2, "Mixture Astrale :", 1)

        # TO DO -> Complet the sprites bases on knowledge and data
        self._base_sprite_list = []
        if self._knowledge["base"]:
            id_base = self._data["base"]
            if id_base != "":
                img = self.MakeEasyImage(0, 8/2, BASE_DATA[id_base]["img"], 0)
                text = self.MakeEasySpriteText(0, 8/2, BASE_DATA[id_base]["name"], 1)
                self._base_sprite_list.append(img)
            else:
                text = self.MakeEasySpriteText(2, 8/2, "Une certaine mixture Astrale", 0)
        else:
            text = self.MakeEasySpriteText(0, 8/2, "?", 1)
        self._base_sprite_list.append(text)

        self._active_sprite = self.MakeEasySpriteText(2, 9/2, "Mixture Elementaire :", 1)

        # TO DO -> Complet the sprites bases on knowledge and data 
        self._active_sprite_list = []
        if self._knowledge["active"]:
            id_active = self._data["active"]
            if id_active != "":
                img = self.MakeEasyImage(0, 10/2, ACTIVE_DATA[id_active]["img"], 0)
                text = self.MakeEasySpriteText(0, 10/2, ACTIVE_DATA[id_active]["name"], 1)
                self._active_sprite_list.append(img)
            else:
                text = self.MakeEasySpriteText(2, 10/2, "Une certaine mixture Elémentaire", 0)
        else:
            text = self.MakeEasySpriteText(0, 10/2, "?", 1)
        self._active_sprite_list.append(text)

        self._alchemical_property_sprite = self.MakeEasySpriteText(2, 11/2, "Propriété alchimique :", 1)

        # TO DO -> Complet the sprites bases on knowledge and data 
        self._alchemical_property_sprite_list = []
        if self._knowledge["alchemical_property"]:
            id_alchemical_property = self._data["alchemical_property"]
            if id_alchemical_property != "":
                img = self.MakeEasyImage(0, 12/2, ALCHEMICAL_PROPERTY_DATA[id_alchemical_property]["img"], 0)
                text = self.MakeEasySpriteText(0, 12/2, ALCHEMICAL_PROPERTY_DATA[id_alchemical_property]["name"], 1)
                self._alchemical_property_sprite_list.append(img)
            else:
                text = self.MakeEasySpriteText(2, 12/2, "Une certaine propriété alchimique", 0)
        else:
            text = self.MakeEasySpriteText(0, 12/2, "?", 1)
        self._alchemical_property_sprite_list.append(text)


    def kill(self):
        self._image_sprite.kill()
        self._name_sprite.kill()
        self._description_sprite.kill()
        self._base_sprite.kill()
        self._base_sprite.kill() 
        self._alchemical_property_sprite.kill()

        if self._knowledge["description"]:
            self._known_description_sprite.kill()
        else:
            self._unknown_description_sprite.kill()
            
        for sprite in self._active_sprite_list:
            sprite.kill()

        for sprite in self._base_sprite_list:
            sprite.kill()
        
        for sprite in self._alchemical_property_sprite_list:
            sprite.kill()
        