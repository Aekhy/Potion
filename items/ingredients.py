from item import Item
from items.settings import DEFAULT_MAX_STACK
class Ingredient():
    def __init__(self, name: str, type: str, max_stack: int = DEFAULT_MAX_STACK ,path: str ="") -> None:
        super().__init__(name, max_stack, path)
        self._type = type

        def get_type(self):
            return self._type
        
        type = property(get_type)