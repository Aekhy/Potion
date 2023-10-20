from items.item import Item
from items.settings import DEFAULT_INGREDIENT_MAX_STACK
class Ingredient(Item):
    def __init__(self, name: str, type: str, characteristics: list, max_stack: int = DEFAULT_INGREDIENT_MAX_STACK ,path: str ="") -> None:
        super().__init__(name, max_stack, path)
        self._type = type
        self._characteristics = characteristics

    def get_type(self):
        return self._type
        
    type = property(get_type)

    def get_characteristics(self):
        return self._characteristics
        
    characteristics = property(get_characteristics)