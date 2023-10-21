from items.ingredients import Ingredient
from items.settings import BASE
from items.potions import Base, Active, Potion


class Chauldron():

    def __init__(self):
        self._base = None
        self._active = None
        self._potion = None
        pass
    # ______ getter & setter _______

    def get_mixture(self):
        # renvoie la base
        if self._base != None and self._active == None:
            res = self._base
        # renvoie l'actif
        elif self._base == None and self._active != None:
            res = self._active
        # renvoie la potion
        else:
            # If base & active = None then potion = None
            # else potion != None
            self._potion.update_info()
            res = self._potion
        return res

    mixture = property(get_mixture)
    # _______________________

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
        return res

    def add_active(self, new_active):
        res = self._active == None
        if res:
            self._active = new_active
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

    def add(self, something):
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
