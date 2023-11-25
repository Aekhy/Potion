from items.item import *
from items.ingredients import *
from items.settings import EFFECT_DATA
from utils.texts import *
from general_settings.private_settings import TILE_SIZE
import pygame


class SubstanceRecipe(Item):
    def __init__(self):
        super().__init__("Nouvelle recette", 1, "")
        self._ingredients = []
        self._effect = None
        self.finished = False

    def update_data(self, substance):
        self._effect = substance.effect
        self._ingredients = substance.ingredients
        self.name = substance.name


class PotionRecipe(Item):
    def __init__(self, base_recipe, active_recipe):
        super().__init__("Nouvelle recette", 1, "")
        self._base_recipe = base_recipe
        self._active_recipe = active_recipe
        self.finished = False

    def update_data(self, base, active, potion):
        self._base_recipe.update_data(base)
        self._active_recipe.update_data(active)
        self.name = potion.name

class SubstanceRecipeDraw:
    def __init__(self, substance_recipe, state, sprites, x, y, width=6, height = 10):
        self.state = state
        self._sprites = sprites
        self._group = {
            "ingredients": [],
            "name": None,
            "effect": None,
            "nb_ingredient": None
        }
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._nb_cols = 3
        

        self.ini_sprites()


    def ini_sprites(self):
        x = (self._x) * TILE_SIZE
        y = (self._y + 1/2) * TILE_SIZE
        text = "Nouvelle recette"
        layer = 1
        sprite = TextOutlined(x, y, text, layer)

        self._sprites.add(sprite)
        self._group["name"] = sprite
        
        x = (self._x + self._width/2) * TILE_SIZE
        y = (self._y + 1/2) * TILE_SIZE
        text = "pas d'effet"
        layer = 1
        sprite = TextOutlined(x, y, text, layer)

        self._sprites.add(sprite)
        self._group["effect"] = sprite


    def add_ingredient(self, ingredient):
        x = (self._x + len(self._group["ingredients"]) % self._nb_cols) * TILE_SIZE
        y = (self._y + (len(self._group["ingredients"]) - 1) / 3 + 1) * TILE_SIZE
        text = ingredient.name
        layer = 1
        ingredient = TextOutlined(x, y, text, layer)

        self._group["ingredient"].append(ingredient)
        self._sprites.add(ingredient)


    def update_name(self, name):
        x = (self._x) * TILE_SIZE
        y = (self._y + 1/2) * TILE_SIZE
        text = name
        layer = 1
        name = TextOutlined(x, y, text, layer)

        self._group["name"].kill()
        self._sprites.add(name)
        self._group["name"] = name
        
    def set_effect(self, effect):
        x = (self._x + self._width/2) * TILE_SIZE
        y = (self._y + 1/2) * TILE_SIZE
        text = effect
        layer = 1
        effect = TextOutlined(x, y, text, layer)

        self._group["effect"].kill()
        self._sprites.add(effect)
        self._group["effect"] = effect

    def kill(self):
        self._group["background"].kill()
        self._group["name"].kill()
        self._group["effect"].kill()
        self._group["nb_ingredient"].kill()
        for ingredient in self._group["ingredients"]:
            ingredient.kill()


class PotionRecipeDraw:
    def __init__(self, state, sprites, x, y, width=6, height = 20):

        self._group = {
            "name": None,
            "base": None,
            "active": None,
        }


    def update_data(self, potion):
        self._recipe["base"] = potion.base.recipe
        self._recipe["active"] = potion.active.recipe
        self._recipe["name"] = potion.name
        self.name = potion.name


class RecipeDraw:
    """
    have 2 slots.
    One to modify, one to read
    XRecipeDraw according to what recipe is in this slot
    """
    def __init__(self, state, sprites, x, y, width=6, height = 20):
   
        pass


    # add recipe

    # get recipe

    # update recipe (thing: Potion)