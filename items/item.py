import pygame
from items.settings import DEFAULT_MAX_STACK
class Item():
    def __init__(self, name: str, max_stack: int = DEFAULT_MAX_STACK, path=""):
        self._name = name
        self._max_stack = max_stack
        self._path = path
        
    # dangerous, can cause infinite recurssion
    # if not properly handled
    def get_name(self):
        return self._name
    def set_name(self, new_name):
        self._name = new_name

    name = property(get_name, set_name)

    def get_max_stack(self):
        return self._max_stack
    
    name = property(get_max_stack)

    def get_path(self):
        return self._path
    
    path = property(get_path)

    #! si on redefinit __eq__ cela plante avec les sprites. (pas tjr apparement, faire attention)
    # utilisé dans Slot.py dans la methode has room
    def __eq__(self, other):
        result = False
        if isinstance(other, Item):
            result = self.name == other.name
        return result
    