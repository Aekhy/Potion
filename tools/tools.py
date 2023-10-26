from items.ingredients import Ingredient
from items.settings import *
from items.settings import BASE
from items.potions import Base, Active, Potion
from .settings import *
from general_settings.private_settings import LAYERS
import pygame as pyg
# we probably want this class to be a child of pygame.sprite.Sprite
class Tool(pyg.sprite.Sprite):
    def __init__(self, name: str, substance_type: Base | Active, effect:str, path: str = ""):
        self._name = name
        self._path = path
        # _substance_type is used to know which kind of
        # subtances it can work with
        self._substance_type = substance_type
        self._substance = None

        # effect should match the substance_type : 
        # Base should have HEATING, FREEZING or MIXING
        # Active should have DISTILLATION, SUBLIMATION or FERMENTATION
        self._effect = effect

    # ______ getter & setter _______

    def get_substance(self):
        return self._substance
    
    # ______ Methods _______
    def add_substance(self, new_substance):
        res = isinstance(new_substance, self._substance_type) and self._substance == None 
        if res:
            self._substance = new_substance
        return res

    def apply_effect(self):
        res = self._substance.effect == None
        if res :
            self._substance.effect = self._effect
        return res

# Each tool have it's own class because we
# probably want to add some specific kind of mini-game 
# to apply the effect

# Please change my class name and my name property
# The heater will probably be one aspect of the cauldron
class Heater(Tool):
    def __init__(self):
        super().__init__("outil de chauffe", Base, HEATING)

# Please change my class name and my name property
class Freezer(Tool):
    def __init__(self):
        super().__init__("outil de gèle", Base, FREEZING)

class Mortar(Tool):
    def __init__(self):
        super().__init__("mortier", Base, MIXING)

class Alembic(Tool):
    def __init__(self):
        super().__init__("alambic", Active, DISTILLATION)

# Please change my class name and my name property
class Sublime(Tool):
    def __init__(self):
        super().__init__("outil de sublimation", Active, SUBLIMATION)

# Please change my class name and my name property
class Ferment(Tool):
    def __init__(self):
        super().__init__("outil de fermentation", Active, FERMENTATION)

# We propably want this class to herit from Tool
class Cauldron(pyg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._base = None
        self._active = None
        self._potion = None
    
        self.game = game
        self.group = self.game.game_sprites
        pyg.sprite.Sprite.__init__(self, self.group)

        self._layer = LAYERS['cauldron']
        # The cauldron is always on the center of the screen
        self._x = x
        self._y = y
        self._width = CAULDRON_SIZE
        self._height = CAULDRON_SIZE

        self._image = pyg.Surface((self._width, self._height))
        self._image.fill(CAULDRON_COLOR)

        self._rect = self._image.get_rect()
        self._rect.x = self._x # type: ignore
        self._rect.y = self._y # type: ignore

    

    
    # ______ getter & setter _______

    @property
    def image(self):
        return self._image
    
    @property
    def rect(self):
        return self._rect
    
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

    def add_thing(self, something):
        """
        If we can add something, return true.
        """
        if isinstance(something, Ingredient):
            res = self.add_ingredient(something)
        elif isinstance(something, Base):
            res = self.add_base(something)
        elif isinstance(something, Active):
            res = self.add_active(something)
        elif isinstance(something, Potion):
            res = self.add_potion(something)
        return res
