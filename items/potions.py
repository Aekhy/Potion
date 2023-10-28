from items.item import Item
from items.settings import *
from general_settings.private_settings import DEBUG

# False to use V2
USE_V1 = False


class Substance(Item):
    def __init__(self, name: str, type: str, comp_matrix, graph, max_stack: int = DEFAULT_MAX_STACK, path: str = ""):
        super().__init__(name, max_stack, path)

        self._ingredients = []

        # Base or Active
        self._type = type

        # Result of the characteristics
        self._node = None

        # this variable tells if the substance is failed or not
        # not used yet
        self._failed = False

        # Characteristics are COLD, HOT, HUMID ...
        self._characteristics = []

        # This matrix is used to add a new characteristic
        self._compatibility_matrix = comp_matrix

        # This graphs tells how to access nodes
        self._graph = graph

    # _______ GETTER & SETTERS _______

    def get_ingredients(self):
        return self._ingredients

    ingredients = property(get_ingredients)

    def get_type(self):
        return self._type

    type = property(get_type)

    def get_characteristics(self):
        return self._characteristics

    characteristics = property(get_characteristics)

    def get_node(self):
        return self._node

    node = property(get_node)

    # _______ METHODS _______

    # _____________V1_______________

    def add_characteristics_V1(self, new_ingredient):
        """
        The `add_characteristics_V1` method is used to add the characteristics of a new ingredient
        to the list of characteristics of the Substance. It checks the compatibility between the
        last characteristic in the list and the new characteristic using the compatibility
        matrix. If the compatibility is 0, meaning the characteristics are incompatible, the
        last characteristic is removed from the list. Otherwise, the new characteristic is added
        to the list.
        """
        for characteristic in new_ingredient.characteristics:
            if len(self._characteristics) == 0:
                self._characteristics.append(characteristic)
            else:
                compatibility = self._compatibility_matrix[self._characteristics[-1]
                                                           ][characteristic]
                if compatibility == 0:
                    self._characteristics.pop()
                else:
                    self._characteristics.append(characteristic)

    def find_node_from_characteristics_V1(self):
        """
        The `find_node_from_characteristics_V1` method is supposed to find what the characteristics
        are corresponding to and store it in self._node
        """
        self._node = NEUTRAL
        if self._characteristics != []:
            l = len(self._characteristics)
            # We know that we have nodes with only even number of characteristics
            if l % 2 == 0:
                i = 0
                done = False
                while not done and i < l:
                    found_node = False
                    for node in self._graph[self._node]["neighbours"]:
                        if found_node:
                            break
                        else:
                            for w in node["weight"]:
                                if w == self._characteristics[i:i+2]:
                                    self._node = node["name"]
                                    found_node = True
                    if not found_node:
                        self._node = NEUTRAL
                        done = True
                    i += 2

    def add_ingredient_V1(self, new_ingredient):
        """
        The `add_ingredient` method add an ingredient to the substance.
        It returns a boolean : True if we added the ingredient successfully, False otherwise.\n
        It calls `add_characterisitcs` and `find_node_from_characteristics`\n
        """
        res = new_ingredient.type == self._type
        if res:
            self._ingredients.append(new_ingredient)
            self.add_characteristics_V1(new_ingredient)
            self.find_node_from_characteristics_V1()
        return res

    # _____________V2_______________

    def remove_characteristic_V2(self, *characterisitcs, ):
        """
        The function `remove_characteristic_V2` removes specified characteristics from a list of
        characteristics.
        :return: a boolean value indicating whether any of the specified characteristics were found and
        removed from the list of characteristics.
        """

        l = len(self._characteristics)
        i = l-1
        found = False
        while not found and i >= 0:
            for c in characterisitcs:
                if self._characteristics[i] == c:
                    found = True
                    self._characteristics.pop(i)
                    break
            i -= 1
        return found

    def find_node_from_characteristics_V2(self):
        """
        The function finds a node in a graph based on its characteristics and updates the current node
        accordingly.
        :return: nothing (None). DO NOT USE THE RETURNED VALUE AS THE NODE FOUND BECAUSE IT'S NOT
        """

        if self._node == None:
            self._node = NEUTRAL

        if self._characteristics != []:

            for node in self._graph[self._node]["neighbours"]:
                for w in node["weight"]:
                    if w == self._characteristics:
                        # If we found a valid weight, it means that we are
                        # moving to the corresponding node
                        self._node = node["name"]
                        # Since we are on a new node, we start over with the characterisitcs
                        self._characteristics = []
                        # Since we found a node, we don't need to look for others so we can
                        # "leave" the function
                        return

    def add_characteristics_V2(self, new_ingredient):
        """
        The function `add_characteristics_V2` adds new characteristics to an ingredient object, removes
        any opposite characteristics, and finds the corresponding node based on the characteristics.

        :param new_ingredient: The `new_ingredient` parameter is an object that represents a new
        ingredient. It has a property called `characteristics` which is a list of characteristics
        associated with the ingredient
        """

        opposites = {HOT: COLD, COLD: HOT, DRY: HUMID, HUMID: DRY,
                     LIGHT: DARK, DARK: LIGHT, MAJOR: MINOR, MINOR: MAJOR}

        for characterisitc in new_ingredient.characteristics:
            if DEBUG:
                print(f" Je vais voir si {characterisitc} à un opposé")
            had_opposite = False
            if characterisitc == SOLID:
                had_opposite = self.remove_characteristic_V2(LIQUID, GAS)
            elif characterisitc == LIQUID:
                had_opposite = self.remove_characteristic_V2(SOLID, GAS)
            elif characterisitc == GAS:
                had_opposite = self.remove_characteristic_V2(SOLID, LIQUID)
            elif characterisitc in opposites.keys():
                had_opposite = self.remove_characteristic_V2(
                    opposites[characterisitc])

            if not had_opposite:
                if DEBUG:
                    print("avant", self._characteristics)
                    print("elle n'avais pas d'opposé, j'ajoute a ma liste")
                self._characteristics.append(characterisitc)
                if DEBUG:
                    print("apres", self._characteristics)
            elif DEBUG:
                print("elle avait un opposé, on la enlevé")
                print("apres", self._characteristics)

            if DEBUG:
                print("je vais chercher une node")
                print("je commence avec : ", self._node)
            self.find_node_from_characteristics_V2()
            if DEBUG:
                # The above code is a Python code snippet that prints the value of the variable
                # `self._node` with the message "je finis avec :".
                print("je finis avec :", self._node)

    def add_ingredient_V2(self, new_ingredient):
        """
        The `add_ingredient_V2` method adds an ingredient to the substance and returns True if
        successful, False otherwise.

        :param new_ingredient: The `new_ingredient` parameter is an object representing the ingredient
        that you want to add to the substance. It should have a `type` attribute that matches the `type`
        attribute of the substance
        :return: The method `add_ingredient_V2` returns a boolean value. It returns `True` if the
        ingredient was added successfully, and `False` otherwise.
        """

        res = new_ingredient.type == self._type
        if res:
            self._ingredients.append(new_ingredient)
            self.add_characteristics_V2(new_ingredient)
        return res

    # ___________________________

    def add_ingredient(self, new_ingredient):
        if USE_V1:
            res = self.add_ingredient_V1(new_ingredient)
        else:
            res = self.add_ingredient_V2(new_ingredient)
        return res


class Base(Substance):
    def __init__(self):
        super().__init__(NEUTRAL, BASE, BASE_ACTIVE_COMPATIBILITY_MATRIX, BASE_GRAPH)

        # Effect from the tools
        self._effect = None

    def get_effect(self):
        return self._effect

    def set_effect(self, new_effect):
        if self._effect == None and new_effect in [HEATING, FREEZING, MIXING]:
            self._effect = new_effect

    effect = property(get_effect, set_effect)

    def get_name(self):
        return f"Mixture astrale {self._node.capitalize()}"

    name = property(get_name)

    def __eq__(self, other):
        result = False
        if isinstance(other, Base):
            result = self._ingredients == other.ingredients
        return result


class Active(Substance):
    def __init__(self):
        super().__init__(NEUTRAL, ACTIVE, BASE_ACTIVE_COMPATIBILITY_MATRIX, ACTIVE_GRAPH)

        # Effect from the tools
        self._effect = None

    def get_effect(self):
        return self._effect

    def set_effect(self, new_effect):
        if self._effect == None and new_effect in [FERMENTATION, DISTILLATION, SUBLIMATION]:
            self._effect = new_effect

    effect = property(get_effect, set_effect)

    def get_name(self):
        return f"Mixture élémentaire {self._node.capitalize()}"

    name = property(get_name)

    def __eq__(self, other):
        result = False
        if isinstance(other, Active):
            result = self._ingredients == other.ingredients
        return result


# a finished potion either has a name or is called a "mixture raté"
# a potion that isn't finished is called a "mixture étrange"

class Potion(Item):
    def __init__(self, name: str, base: Base, active: Active, max_stack: int = DEFAULT_POTION_MAX_STACK, path: str = ""):
        super().__init__(name, max_stack, path)
        self._ingredients = []
        self._base = base
        self._active = active
        # Do not access this value except in get_alchemical_property
        # you should be accessing self.alchemical_property
        self._alchemical_property = None

    # _______ GETTER & SETTERS _______
    def get_ingredients(self):
        return self._ingredients

    ingredients = property(get_ingredients)

    def get_base(self):
        return self._base

    base = property(get_base)

    def get_active(self):
        return self._active

    active = property(get_active)

    def get_planet(self):
        return self._base.node

    planet = property(get_planet)

    def get_element(self):
        return self._active.node

    element = property(get_element)

    def get_alchemical_property(self):
        if self._base.effect != None and self._active.effect != None:
            self._alchemical_property = ALCHEMICAL_PROPERTY_MATRIX[
                self._base.effect][self._active.effect]
        return self._alchemical_property

    alchemical_property = property(get_alchemical_property)

    def get_finished(self):
        return self._base.node != None and self._active.node != None and self.alchemical_property != None

    finished = property(get_finished)

    def get_name(self):
        # when we call name, we should have already
        # called update_info()
        return self._name

    name = property(get_name)

    def get_description(self):
        # when we call description, we should have already
        # called update_info()
        return self._description

    description = property(get_description)
    # _______ METHODS _______

    def add_ingredient(self, *ingredients):
        """
        The function adds ingredients to a recipe and updates the recipe's information.
        """
        for new_ingredient in ingredients:
            self._ingredients.append(new_ingredient)
            self._base.add_ingredient(new_ingredient)
            self._active.add_ingredient(new_ingredient)

    def add_effect(self, *effects):
        """
        The function adds effect(s) to the base and active if they don't have one
        """
        for new_effect in effects:
            if self.alchemical_property == None:
                if self._base.effect == None and new_effect in [HEATING, FREEZING, MIXING]:
                    self._base.effect = new_effect
                elif self._active.effect == None and new_effect in [FERMENTATION, DISTILLATION, SUBLIMATION]:
                    self._active.effect = new_effect

    # for now, this code is in potion but it will be else where in the end (in the cauldron for example)
    def update_info(self):
        """
        The function updates the name and description of a potion based on its
        planet, element and alchemical property.
        """
        if not self.finished:
            self._name = "Mixture étrange"
            self._description = "Une mixture qui a un certain potentiel..."
        else:
            tmp = MAIN_POTION_TREE
            for level in [TOP, MIDDLE, BOTTOM]:
                if level == TOP:
                    key = self._base.node
                elif level == MIDDLE:
                    key = self.alchemical_property
                else:
                    key = self._active.node

                if key in tmp.keys():
                    tmp = tmp[key]
                else:
                    tmp = tmp[NEUTRAL]
                    break
                if tmp["level"] == END:
                    break

            potion_info = tmp
            self._name = potion_info["name"]
            self._description = potion_info["description"]

    def __eq__(self, other):
        result = False
        if isinstance(other, Potion):
            result = self._ingredients == other.ingredients
        return result