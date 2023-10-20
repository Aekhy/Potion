from items.item import Item
from items.settings import *
from graphs.settings import * 


class Substance(Item):
    def __init__(self, result: str, type: str, comp_matrix, graph, max_stack: int = DEFAULT_MAX_STACK, path: str =""):
        super().__init__(result, max_stack, path)
        
        self._ingredients = []
        
        # Base or Active
        self._type = type
 
        # Result of the characteristics
        self._node = None
        
        # this variable tells if the substance is failed or not
        self._failed = False

        # Characteristics are COLD, HOT, HUMID ...
        self._characteristics = []

        # This matrix is used to add a new characteristic
        self._compatibility_matrix = comp_matrix
        
        # This graphs tells how to access nodes
        self._graph = graph
        
        

    #_______ GETTER & SETTERS _______
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

    

    #_______ METHODS _______
    def add_characteristics(self, new_ingredient):
        """
        The `add_characteristics` method is used to add the characteristics of a new ingredient
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
                compatibility = self._compatibility_matrix[self._characteristics[-1]][characteristic]
                if compatibility == 0:
                    self._characteristics.pop()
                else:
                    self._characteristics.append(characteristic)
        
    def find_node_from_characteristics(self):
        """
        The `find_node_from_characteristics` method is supposed to find what the characteristics
        are corresponding to and store it in self._node
        """
        self._node = NEUTRAL
        if self._characteristics != []:
            l = len(self._characteristics)
            # We know that we have nodes with only even number of characteristics
            if l % 2 == 0:
                i = 0
                done = False
                while not done and i<l :
                    found_node = False
                    for node in self._graph[self._node]["neighbours"]:
                        if found_node :
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
    
    def add_ingredient(self, new_ingredient):
        """
        The `add_ingredient` method add an ingredient to the substance.
        It returns a boolean : True if we added the ingredient successfully, False otherwise.\n
        It calls `add_characterisitcs` and `find_node_from_characteristics`\n
        """
        res = new_ingredient.type == self._type
        if res:
            self._ingredients.append(new_ingredient)
            self.add_characteristics(new_ingredient)
            self.find_node_from_characteristics()
        return res
        
class Base(Substance):
    def __init__(self):
        super().__init__(NEUTRAL, BASE, BASE_ACTIVE_COMPATIBILITY_MATRIX, BASE_GRAPH)
        
        # Effect from the tools
        self._effect = NOTHING

    def get_effect(self):
        return self._effect
    
    def set_effect(self, new_effect):
        if self._effect == NOTHING and new_effect in [HEATING, FREEZING, MIXING] :
            self._effect = new_effect

    effect = property(get_effect, set_effect)

class Active(Substance):
    def __init__(self):
        super().__init__(NEUTRAL, ACTIVE, BASE_ACTIVE_COMPATIBILITY_MATRIX, ACTIVE_GRAPH)
    
        # Effect from the tools
        self._effect = NOTHING

    def get_effect(self):
        return self._effect
    
    def set_effect(self, new_effect):
        if self._effect == NOTHING and new_effect in [FERMENTATION, DISTILLATION, SUBLIMATION] :
            self._effect = new_effect

    effect = property(get_effect, set_effect)

class Potion(Item):
    def __init__(self, name: str, max_stack: int = DEFAULT_POTION_MAX_STACK, path: str =""):
        super().__init__(name, max_stack, path)
        self._ingredients = []
        self._base = Base()
        self._active = Active()
    
    #_______ GETTER & SETTERS _______
    def get_ingredients(self):
        return self._ingredients
        
    ingredients = property(get_ingredients)

    def get_planet(self):
        return self._base.node
    
    planet = property(get_planet)

    def get_element(self):
        return self._active.node
    
    element = property(get_element)

    def get_alchemical_property(self):
        return ALCHEMICAL_PROPERTY_MATRIX[self._base.effect][self._active.effect]

    alchemical_property = property(get_alchemical_property)

    def get_finished(self):
        return self._base.node != None and self._active.node != None and self.alchemical_property != NOTHING

    finished = property(get_finished)


    def get_name(self):
        if not self.finished:
            res = "Mixture étrange"
        else:
            res = self._name
        return res
    
    name = property(get_name)

    #_______ METHODS _______ 

    def add_ingredient(self, *ingredients):
        for new_ingredient in ingredients:
            self._ingredients.append(new_ingredient)
            self._base.add_ingredient(new_ingredient)
            self._active.add_ingredient(new_ingredient)

    def add_effect(self, *effects):
        for new_effect in effects:
            if self.alchemical_property == NOTHING:
                if self._base.effect == NOTHING and new_effect in [HEATING, FREEZING, MIXING] :
                    self._base.effect = new_effect
                elif self._active.effect == NOTHING and new_effect in [FERMENTATION, DISTILLATION, SUBLIMATION] :
                    self._active.effect = new_effect
