from items.ingredients import Ingredient
from items.settings import *
from items.settings import BASE
from items.potions import Base, Active, Potion
from inventory.case import Case
from inventory.slot import Slot
from inventory.settings import CASE_SIZE_DEFAULT
from utils.texts import TextOutlined
from .settings import *
from general_settings.private_settings import LAYERS, COLORS
import pygame as pyg
# we probably want this class to be a child of pygame.sprite.Sprite
class Tool(pyg.sprite.Sprite):
    def __init__(self, game, name: str, mixture_type: Base | Active, effect:str, x, y, color, size=100, path: str = "",):
        # Engine
        self._game = game
        self._name = name
        # _mixture_type is used to know which kind of
        # subtances it can work with
        self._mixture_type = mixture_type
        self._mixture = None
        # effect should match the mixture_type : 
        # Base should have HEATING, FREEZING or MIXING
        # Active should have DISTILLATION, SUBLIMATION or FERMENTATION
        self._effect = effect

        # Graphism
        self._x = x
        self._y = y
        self._path = path
        self.group = self._game.game_sprites
        self._layer = LAYERS["tools"]
        if path == "":
            self.image = pyg.Surface((size,size))
            self.image.fill(color)
        else:
            self.image = pyg.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self._mixture_slot = Slot(self._game, self.group ,True,False,None,0,self._x - 10 ,self._y - 10 ,self._layer+0.1, 50)
        
        self.finish_button = TextOutlined(self._x , self._y + size, self._effect, self.layer+0.1,"topleft")
        self.finish_button.add_to_group(self.group)
        pyg.sprite.Sprite.__init__(self, self.group) 
    # ______ getter & setter _______

    
    # ______ Methods _______
    def add_mixture(self, new_mixture, quantity):
        mix_none = self._mixture == None  
        mix_substance_effect_none = isinstance(new_mixture, self._mixture_type) and new_mixture.effect == None
        mix_potion_good_substance_effect_none = isinstance(new_mixture, Potion) and ((new_mixture.get_base().effect == None and self._mixture_type == Base) or new_mixture.get_active().effect == None and self._mixture_type == Active)
        res = mix_none and (mix_substance_effect_none or mix_potion_good_substance_effect_none)
        if res:
            self._mixture = new_mixture
            res_q = quantity - 1
            res_s = self._mixture
            if res_q == 0:
                res_s = None
            end_res = (True, res_s, res_q)
        else:
            end_res = (False,new_mixture,quantity)
        return end_res

    def apply_effect(self):
        if self._mixture != None:
            res = True
            if isinstance(self._mixture, Potion):
                self._mixture.add_effect(self._effect)
                self._mixture.update_info()
            else:
                self._mixture.effect = self._effect
            self._mixture_slot.add_item(self._mixture)
            print("effet ajouté")
        else:
            res = False
            print("effet appelé mais pas ajouté")
        return res
    
    def reset(self):
        self._mixture = None
        
    def verify_slot(self, slot_to_verify):
        return slot_to_verify == self._mixture_slot

# Each tool have it's own class because we
# probably want to add some specific kind of mini-game 
# to apply the effect

# Please change my class name and my name property
# The heater will probably be one aspect of the cauldron
class Heater(Tool):
    def __init__(self, game, x, y):
        super().__init__(game,"outil de chauffe", Base, HEATING, x, y, "orange")

# Please change my class name and my name property
class Freezer(Tool):
    def __init__(self, game, x, y):
        super().__init__(game, "outil de gèle", Base, FREEZING, x, y, "blue")

class Mortar(Tool):
    def __init__(self, game, x, y):
        super().__init__(game, "mortier", Base, MIXING, x, y, "brown")

class Alembic(Tool):
    def __init__(self, game, x, y):
        super().__init__(game, "alambic", Active, DISTILLATION, x, y, "pink")

# Please change my class name and my name property
class Sublime(Tool):
    def __init__(self, game, x, y):
        super().__init__(game, "outil de sublimation", Active, SUBLIMATION, x, y, "purple")

# Please change my class name and my name property
class Ferment(Tool):
    def __init__(self, game, x, y):
        super().__init__(game, "outil de fermentation", Active, FERMENTATION, x, y, "green")

# We propably want this class to herit from Tool
class Cauldron(pyg.sprite.Sprite):
    def __init__(self, game, spritesGroup, x, y):

        # The cauldron is always on the center of the screen
        self._x = x
        self._y = y
        self._layer = LAYERS['cauldron']
        self.group = spritesGroup

        self._base = None
        self._active = None
        self._potion = None
        self._mixture_slot = Slot(game, self.group,True,False,None,0,self._x - 50,self._y - 50,self._layer+0.1)
        self._finished = False
        pyg.sprite.Sprite.__init__(self, self.group)

        
        self._width = CAULDRON_SIZE
        self._height = CAULDRON_SIZE

        self._image = pyg.Surface((self._width, self._height))
        self._image.fill(CAULDRON_COLOR)

        self._rect = self._image.get_rect()
        self._rect.x = self._x
        self._rect.y = self._y


        # finish button, better code needed for buttons
        # self.finish_button = Case(self.group, self._x - 50,self._y - 50+CASE_SIZE_DEFAULT,self.layer+0.1,"",20,COLORS["darkred"])
        self.finish_button = TextOutlined(self._x - 50,self._y - 50+CASE_SIZE_DEFAULT,"Finir",self.layer+0.1,"topleft")
        self.finish_button.add_to_group(self.group)
    # ______ getter & setter _______

    @property
    def image(self):
        return self._image
    
    @property
    def rect(self):
        return self._rect
    
    @property
    def mixture_slot(self):
        return self._mixture_slot
    
    def get_mixture(self):
        # return the base
        if self._base != None and self._active == None:
            res = self._base
        # return the active
        elif self._base == None and self._active != None:
            res = self._active
        # return the potion
        else:
            
            if self._potion != None:
                # this set the proper name/description of the potion
                # based on his planet(base), element(active) and 
                # alchemical_property(base effect x active effect)
                self._potion.update_info()
            # If base & active == None then potion == None
            # else potion != None
            res = self._potion
        return res

    mixture = property(get_mixture)
    # _______________________
    def update(self):
        pass

    def add_ingredient(self, new_ingredient):

        if self._potion != None:
            res = True
            self._potion.add_ingredient(new_ingredient)
        else:
            # Add to self._base
            if new_ingredient.type == BASE:
                if self._base == None:
                    self._base = Base()
                res = self._base.add_ingredient(new_ingredient)
            # Add to self._active
            else:  # Type == ACTIVE
                if self._active == None:
                    self._active = Active()
                res = self._active.add_ingredient(new_ingredient)
            # Time to make a potion
            if self._base != None and self._active != None:
                self._potion = Potion("Mixture", self._base, self._active)
                res = self._potion.add_ingredient(new_ingredient)
        return res

    # I use methods and not setters
    # because i return a value to say
    # if i successfully added

    def add_base(self, new_base):
        res = self._base == None
        if res:
            self._base = new_base
            if self._active != None:
                self._potion = Potion("No name", self._base, self._active)
        return res

    def add_active(self, new_active):
        res = self._active == None
        if res:
            self._active = new_active
            if self._base != None:
                self._potion = Potion("No name", self._base, self._active)
        return res

    def add_potion(self, new_potion):
        res = (
            self._base == None and
            self._active == None and
            self._potion == None and
            not new_potion.finished
        )

        if res:
            self._potion = new_potion
            self._base = self._potion.base
            self._active = self._potion.active
        return res

    def add_thing(self, something, quantity):
        """
        If we can add something, return true.
        """
        if not self._finished:
            if isinstance(something, Ingredient):
                res = self.add_ingredient(something)
            elif isinstance(something, Base):
                res = self.add_base(something)
            elif isinstance(something, Active):
                res = self.add_active(something)
            elif isinstance(something, Potion):
                res = self.add_potion(something)
            else:
                res = False
            print(res)
            if res:
                res_q = quantity - 1
                res_s = something
                if res_q == 0:
                    res_s = None
                end_res = (True, res_s, res_q)
            else:
                end_res = (False,something,quantity)
        else:
            end_res = (False,something,quantity)
        return end_res
    

    def finish(self):
        if self._base != None or self._active != None:
            print("potion finie")
            self._finished = True
            if self._mixture_slot.is_empty:
                self._mixture_slot.add_item(self.mixture)
        else:
            print("click finish but potion as no ingerdient yet")

    def reset(self):
        self._finished = False
        self._base = None
        self._active = None
        self._potion = None
        
    def verify_slot(self, slot_to_verify):
        return slot_to_verify == self._mixture_slot
        