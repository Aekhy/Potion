from utils.texts import TextOutlined
from utils.my_sprite import MySprite
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
        return easy_sprite

    def kill(self):
        self._image_sprite.kill()
        self._name_sprite.kill()

        
class IngredientDisplay(DataDisplay):
    def __init__(self, knowledge, data, sprites_group, x, y, tilesize) -> None:
        super().__init__(knowledge, data, sprites_group, x, y, tilesize)

        self._type_sprite = self.MakeEasySpriteText(2, 5/2, "Type :", 1)
        self._type_sprite.add_to_group(self._group)

        self._characteristics_sprite = self.MakeEasySpriteText(2, 7/2, "Caractéristiques :", 1)
        self._characteristics_sprite.add_to_group(self._group)

        self._max_stack_sprite = self.MakeEasySpriteText(2, 9/2, "Quantité maximale de stack :", 1)
        self._max_stack_sprite.add_to_group(self._group)

        # TO DO -> Complet the sprites bases on knowledge and data 

    def kill(self):
        self._image_sprite.kill()
        self._name_sprite.kill()
        self._type_sprite.kill()
        self._characteristics_sprite.kill()
        self._max_stack_sprite.kill()

class CharacteristicDisplay(DataDisplay):
    def __init__(self, knowledge, data, sprites_group, x, y, tilesize) -> None:
        super().__init__(knowledge, data, sprites_group, x, y, tilesize)

        self._opposites_sprite = self.MakeEasySpriteText(2, 5/2, "Caractéristiques opposée(s) :", 1)
        self._opposites_sprite.add_to_group(self._group)

        # TO DO -> Complet the sprites bases on knowledge and data 

    def kill(self):
        self._image_sprite.kill()
        self._name_sprite.kill()
        self._opposites_sprite.kill()

class EffectDisplay(DataDisplay):
    def __init__(self, knowledge, data, sprites_group, x, y, tilesize) -> None:
        super().__init__(knowledge, data, sprites_group, x, y, tilesize)

        self._type_sprite = self.MakeEasySpriteText(2, 5/2, "Type de mixture adapté :", 1)
        self._type_sprite.add_to_group(self._group)

        # TO DO -> Complet the sprites bases on knowledge and data 

    def kill(self):
        self._image_sprite.kill()
        self._name_sprite.kill()
        self._type_sprite.kill()

class BaseDisplay(DataDisplay):
    def __init__(self, knowledge, data, sprites_group, x, y, tilesize) -> None:
        super().__init__(knowledge, data, sprites_group, x, y, tilesize)

        self._neighbours_sprite = self.MakeEasySpriteText(2, 5/2, "Planètes proches :", 1)
        self._neighbours_sprite.add_to_group(self._group)

        # TO DO -> Complet the sprites bases on knowledge and data 

    def kill(self):
        self._image_sprite.kill()
        self._name_sprite.kill()
        self._neighbours_sprite.kill()

class ActiveDisplay(DataDisplay):
    def __init__(self, knowledge, data, sprites_group, x, y, tilesize) -> None:
        super().__init__(knowledge, data, sprites_group, x, y, tilesize)

        self._neighbours_sprite = self.MakeEasySpriteText(2, 5/2, "Eléments proches :", 1)
        self._neighbours_sprite.add_to_group(self._group)

        # TO DO -> Complet the sprites bases on knowledge and data 


    def kill(self):
        self._image_sprite.kill()
        self._name_sprite.kill()
        self._neighbours_sprite.kill()

class AlchemicalPropertyDisplay(DataDisplay):
    def __init__(self, knowledge, data, sprites_group, x, y, tilesize) -> None:
        super().__init__(knowledge, data, sprites_group, x, y, tilesize)

        self._base_effect_sprite = self.MakeEasySpriteText(2, 5/2, "Effet de la mixture Astrale :", 1)
        self._base_effect_sprite.add_to_group(self._group)

        # TO DO -> Complet the sprites bases on knowledge and data 

        self._active_effect_sprite = self.MakeEasySpriteText(2, 7/2, "Effet de la mixture Elémentaire :", 1)
        self._active_effect_sprite.add_to_group(self._group)
        
        # TO DO -> Complet the sprites bases on knowledge and data 


    def kill(self):
        self._image_sprite.kill()
        self._name_sprite.kill()
        self._base_effect_sprite.kill()
        self._active_effect_sprite.kill()  

class PotionDisplay(DataDisplay):
    def __init__(self, knowledge, data, sprites_group, x, y, tilesize) -> None:
        super().__init__(knowledge, data, sprites_group, x, y, tilesize)

        self._description_sprite = self.MakeEasySpriteText(2, 5/2, "Description :", 1)
        self._description_sprite.add_to_group(self._group)

        # TO DO -> Complet the sprites bases on knowledge and data 

        self._base_sprite = self.MakeEasySpriteText(2, 7/2, "Mixture Astrale :", 1)
        self._base_sprite.add_to_group(self._group)

        # TO DO -> Complet the sprites bases on knowledge and data 

        self._active_sprite = self.MakeEasySpriteText(2, 9/2, "Mixture Elementaire :", 1)
        self._active_sprite.add_to_group(self._group)

        # TO DO -> Complet the sprites bases on knowledge and data 

        self._alchemical_property_sprite = self.MakeEasySpriteText(2, 11/2, "Propriété alchimique :", 1)
        self._alchemical_property_sprite.add_to_group(self._group)

        # TO DO -> Complet the sprites bases on knowledge and data 

    def kill(self):
        self._image_sprite.kill()
        self._name_sprite.kill()
        self._description_sprite.kill()
        self._base_sprite.kill()
        self._base_sprite.kill() 
        self._alchemical_property_sprite.kill()

