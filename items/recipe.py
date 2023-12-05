from items.item import *
from items.ingredients import *
from items.potions import *
from inventory.slot import *
from utils.texts import *
from general_settings.private_settings import TILE_SIZE
import math
import pygame


class Paper(Item):
    def __init__(self, make=None):
        super().__init__("Papier", 50, "")

class SubstanceRecipe(Item):
    def __init__(self, make=None):
        super().__init__("Nouvelle recette", 1, "")
        self._ingredients = []
        self._effect = None
        self.finished = False
        if not make is None:
            self._effect = make["effect"]
            for ingredient in make["ingredients"]:
                self._ingredients.append(Ingredient(ingredient))
            self.finished = make["finished"]
            self.name = make["name"]

    def update_data(self, substance):
        self._effect = substance.effect
        self._ingredients = substance.ingredients
        self.name = "Recette " + substance._node

    def get_info_save(self):
        res = {
            "name": self.name,
            "ingredients" : [],
            "effect" : self._effect,
            "finished" : self.finished,
        }
        for ingredient in self._ingredients:
            res["ingredients"].append(ingredient.name)

        return res

class PotionRecipe(Item):
    def __init__(self, make=None):
        super().__init__("Nouvelle recette", 1, "")
        if make is None:
            self._base_recipe = SubstanceRecipe()
            self._active_recipe = SubstanceRecipe()
            self.finished = False
        else:
            self._base_recipe = SubstanceRecipe(make["base_recipe"]) 
            self._active_recipe = SubstanceRecipe(make["active_recipe"])
            self.finished = make["finished"]
            self.name = make["name"]

    def update_data(self, base, active, potion):
        if base != None:
            self._base_recipe.update_data(base)
        if active != None:
            self._active_recipe.update_data(active)
        self.name = "Recette " + potion.name

    def get_info_save(self):
        res = {
            "name": self.name,
            "base_recipe" : self._base_recipe.get_info_save(),
            "active_recipe" : self._active_recipe.get_info_save(),
            "finished" : self.finished
        }
        return res


class SubstanceRecipeDraw:
    def __init__(self, recipe, state, sprites, x, y, width=6, height = 10, show=True):
        self.state = state
        self._sprites = sprites
        self._group = {
            "ingredients": [],
            "name": None,
            "effect": None,
        }
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._nb_cols = 3
        
        self.update_all(recipe, show)

    def get_height(self):
        return math.ceil(len(self._group["ingredients"])/3) + 1

    def update_all(self, recipe: SubstanceRecipe, show):
        self.kill()
        print(recipe.name)
        self.update_name(recipe.name.replace("Recette ", ""), show)
        self.set_effect(recipe._effect, show)
        
        for ingredient in recipe._ingredients:
            self.add_ingredient(ingredient, show)
    

    def add_ingredient(self, ingredient, show=True):
        x = (self._x + (len(self._group["ingredients"]) % self._nb_cols) * 3/2) * TILE_SIZE
        print( ((len(self._group["ingredients"])) // 3) + 1)
        y = (self._y + (len(self._group["ingredients"])) // 3 + 1) * TILE_SIZE
        text = ingredient.name
        layer = 1
        ingredient = TextOutlined(x, y, text, layer, "topleft")

        self._group["ingredients"].append(ingredient)

        if show:
            ingredient.add_to_group(self._sprites)

    def update_name(self, name, show=True):
        x = (self._x) * TILE_SIZE
        y = (self._y) * TILE_SIZE
        text = name
        layer = 1
        name = TextOutlined(x, y, text, layer, "topleft")

        if not self._group["name"] is None:
            self._group["name"].kill()
        self._group["name"] = name
        if show:
            name.add_to_group(self._sprites)
        
    def set_effect(self, new_effect, show=True):
        x = (self._x + self._width * 3/4) * TILE_SIZE
        y = (self._y) * TILE_SIZE
        text = "?" if new_effect is None else new_effect
        layer = 1
        effect = TextOutlined(x, y, text, layer, "topleft")

        if not self._group["effect"] is None:
            self._group["effect"].kill()

        self._group["effect"] = effect
        if show:
            effect.add_to_group(self._sprites)
        pass

    def kill(self):
        if not self._group["name"] is None:
            self._group["name"].kill()
        if not self._group["effect"] is None:
            self._group["effect"].kill()

        for ingredient in self._group["ingredients"]:
            ingredient.kill()

    def show(self):
        self.kill()
        self._group["name"].add_to_group(self._sprites)
        self._group["effect"].add_to_group(self._sprites)
        for ingredient in self._group["ingredients"]:
            ingredient.add_to_group(self._sprites)

class PotionRecipeDraw:
    def __init__(self, recipe: PotionRecipe, state, sprites, x, y, width=6, height = 20, show=True):
        self._x = x
        self._y = y
        self._sprites = sprites
        
        b = SubstanceRecipeDraw(recipe._base_recipe, state, sprites, x, y, width, 8, show)
        h = b.get_height() 
        a = SubstanceRecipeDraw(recipe._active_recipe, state, sprites, x, y+h, width, 8, show)
        n = TextOutlined(x, y, recipe.name.replace("Recette ", ""), 1, "topleft")
        
        self._group = {
            "name": n,
            "base": b,
            "active": a,
        }

        if show:
            self._group["name"].add_to_group(self._sprites)

    def update_data(self, recipe: PotionRecipe, show=True):
        self._group["base"].update_all(recipe._base_recipe)
        self._group["active"].update_all(recipe._active_recipe)

        self._group["name"].kill()
        self._group["name"] = TextOutlined(self._x, self._y, recipe.name, 1)
        if show:
            self._group["name"].add_to_group(self._sprites)

    def add_ingredient(self, ingredient: Ingredient, show=True):
        self._group["ingredient.type"].add_ingredient(ingredient, show)

    def show(self):
        self.kill()
        self._group["base"].show()
        self._group["active"].show()
        self._group["name"].add_to_group(self._sprites)
        
    def kill(self):
        self._group["base"].kill()
        self._group["active"].kill()
        self._group["name"].kill()
        


class RecipeDraw:
    """
    have 2 slots.
    One to modify, one to read
    XRecipeDraw according to what recipe is in this slot
    """
    def __init__(self, state, x, y, width=6, height = 20):
   
        self._group = {}
        self._state = state
        self._x = x
        self._y = y
        self._width = width
        self._height = height

        self._modify_draw = None
        self._visualise_draw = None

        self.make_slots()
        self.make_labels()
        self.make_background()

    def make_background(self):
        space = pygame.sprite.Sprite(self._state.sprites)
        space.image = pygame.Surface((self._width * TILE_SIZE, self._height * TILE_SIZE))
        space.image.fill((200, 100, 40 ))
        space._layer = 0
        space.rect = space.image.get_rect()
        space.rect.topleft = (self._x * TILE_SIZE, self._y * TILE_SIZE)

    def make_labels(self):
        x = (self._x + 1/2 + self._width//4) * TILE_SIZE
        y = (self._y) * TILE_SIZE
        layer = 1
        text = "Modifier"
        self._label_modifiy = TextOutlined(x, y, text, layer, "topleft")
        self._label_modifiy.add_to_group(self._state.sprites)

        x = (self._x + self._width//4 + self._width/2 ) * TILE_SIZE
        text = "Visualiser"
        self._label_visualise = TextOutlined(x, y, text, layer, "topleft")
        self._label_visualise.add_to_group(self._state.sprites)


    def make_slots(self):
        x = (self._x + 1/2 + self._width//4) * TILE_SIZE
        y = (self._y + 1/2) * TILE_SIZE
        layer = 1
    
        whitelist = {"black_list":None,"white_list":[Paper, SubstanceRecipe, PotionRecipe]}
        self._modify_recipe_slot = Slot(self._state, 
                                    self._state.sprites, 
                                    True, True, None, 
                                    0, x, y, layer, 
                                    64, whitelist)
        
        self._state.slots["take"].append(self._modify_recipe_slot)
        self._state.slots["add"].append(self._modify_recipe_slot)

        x = (self._x + self._width//4 + self._width/2 ) * TILE_SIZE
        whitelist = {"black_list":None,"white_list":[SubstanceRecipe, PotionRecipe]}
        self._visualise_recipe_slot = Slot(self._state, 
                                    self._state.sprites, 
                                    True, True, None, 
                                    0, x, y, layer, 
                                    64, whitelist)
        
        self._state.slots["take"].append(self._visualise_recipe_slot)
        self._state.slots["add"].append(self._visualise_recipe_slot)
    
    def get_slots(self):
        return [self._visualise_recipe_slot, self._modify_recipe_slot]
    
    def get_state(self):
        if not self._visualise_recipe_slot.is_empty:
            res = "visualise"
        elif not self._modify_recipe_slot.is_empty:
            res = "modify"
        else:
            res = "ready"
        return res
    
    def has_modify(self):
        return not self._modify_recipe_slot.is_empty
    
    def has_visualise(self):
        return not self._visualise_recipe_slot.is_empty

    def update_draw(self):
        if self.has_visualise():
            recipe = self._visualise_recipe_slot.item
            x = self._x
            y = self._y + 3/2
            width = self._width
            height = self._height
            show = self.get_state()=="visualise"
            if isinstance(recipe, SubstanceRecipe):
                self._visualise_draw = SubstanceRecipeDraw(recipe, self._state, self._state.sprites,
                                                            x, y, width, height, show)
            else:
                self._visualise_draw = PotionRecipeDraw(recipe, self._state, self._state.sprites, x, y, width, height, show)
        else:
            self._visualise_draw = None

        if self.has_modify():
            if (not self._state.cauldron._base is None) and (not self._state.cauldron._active is None):
                self._modify_recipe_slot.take_item()    
                recipe = PotionRecipe()
                # this is suppose to create now object
                # otherwise, every recipe that goes into modify slot
                # are linked to the cauldron even when there are in the visualise slot
                b = Base(self._state.cauldron._base.get_info_save())
                a = Active(self._state.cauldron._active.get_info_save())
                p = Potion("", Base(), Active(), self._state.cauldron._potion.get_info_save())
                recipe.update_data(b, a ,p)
                self._modify_recipe_slot.add_item(recipe)
                
                x = self._x
                y = self._y + 3/2
                width = self._width
                height = self._height

                self._modify_draw = PotionRecipeDraw(recipe, self._state, self._state.sprites,
                                                        x, y, width, height, self.get_state()=="modify")
                
            elif (not self._state.cauldron._base is None) or (not self._state.cauldron._active is None):
                self._modify_recipe_slot.take_item()    
                recipe = SubstanceRecipe()
                if not self._state.cauldron._base is None:
                    b = Base(self._state.cauldron._base.get_info_save())
                    recipe.update_data(b)
                elif not self._state.cauldron._active is None:
                    a = Active(self._state.cauldron._active.get_info_save())
                    recipe.update_data(a)
                self._modify_recipe_slot.add_item(recipe)

                x = self._x 
                y = self._y + 3/2
                width = self._width
                height = self._height

                self._modify_draw = SubstanceRecipeDraw(recipe, self._state, self._state.sprites,
                                                        x, y, width, height, self.get_state()=="modify")
        else:
            self._modify_draw = None

    def reset_draw(self):
        print("reset")
        if not self._visualise_draw is None:
            self._visualise_draw.kill()
        if not self._modify_draw is None:
            self._modify_draw.kill()

    def show_draw(self):
        if not self._visualise_draw is None:
            self._visualise_draw.show()
        elif not self._modify_draw is None:
            self._modify_draw.show()

    def update_state(self):
        # update_state is used when we move a recipe in/out slot 
        self.reset_draw()
        self.update_draw()
        self.show_draw()
