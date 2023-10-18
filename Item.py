import pygame
from settings.ClasseSetting import DEFAULT_MAX_STACK
class Item():
    def __init__(self, name: str, max_stack: int = DEFAULT_MAX_STACK, path=""):
        self.path = ""
        self.name = name
        self.max_stack = max_stack

    def get_name(self):
        return self.name
    
    def get_max_stack(self):
        return self.max_stack
    
    #! si on redefinit __eq__ cela plante avec les sprites. (pas tjr apparement, faire attention)
    # utilisé dans Slot.py dans la methode has room
    def __eq__(self, other):
        result = False
        if isinstance(other, Item):
            result = self.name == other.name
        return result
    