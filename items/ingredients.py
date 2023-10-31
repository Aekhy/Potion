from items.item import Item
from items.settings import DEFAULT_INGREDIENT_MAX_STACK, INGREDIENT_DATA
from utils.json_functions import Read
import json

class Ingredient(Item):
    def __init__(self, name: str) -> None:

        ingredient = INGREDIENT_DATA[name]
        
        ms = ingredient["max_stack"]
        if ms <= 0:
            ms = DEFAULT_INGREDIENT_MAX_STACK

        super().__init__(name, ms, ingredient["path"])
        self._type = ingredient["type"]
        self._characteristics = ingredient["characteristics"]

    def get_type(self):
        return self._type
        
    type = property(get_type)

    def get_characteristics(self):
        return self._characteristics
        
    characteristics = property(get_characteristics)


class Debug_Ingredient(Item):
    def __init__(self, name: str, type: str, characteristics: list, max_stack: int = DEFAULT_INGREDIENT_MAX_STACK, path: str ="") -> None:
        super().__init__(name, max_stack, path)
        self._type = type
        self._characteristics = characteristics

    def get_type(self):
        return self._type
        
    type = property(get_type)

    def get_characteristics(self):
        return self._characteristics
        
    characteristics = property(get_characteristics)