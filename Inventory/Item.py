from .config import *

class Item():
    def __init__(self, name: str, max_stack: int = DEFAULT_MAX_STACK, img=""):
        self._img = img
        self._name = name
        self._max_stack = max_stack

    # ***** GETTER *****
    
    @property
    def name(self):
        return self._name
    
    @property
    def max_stack(self):
        return self._max_stack

    @property
    def img(self):
        return self._img

    # ***** TOOLS - BOOL *****

    # To know if two items are equal, we compare their names
    def __eq__(self, other):
        result = False
        if isinstance(other, Item):
            result = self.name == other.name
        return result