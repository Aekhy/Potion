import pygame
from Case import Case
from settings.ClasseSetting import *
from Utils import *
from group import draw_grp

class Slot():
    def __init__(self, item=None, quantity=0, x=0, y=0, size=DEFAULT_SLOT_SIZE, color=DEFAULT_SLOT_COLOR, item_name_font_size=DEFAULT_ITEM_NAME_FONT_SIZE, item_name_font_color=DEFAULT_ITEM_NAME_FONT_COLOR, quantity_font_size=DEFAULT_QUANTITY_FONT_SIZE, quantity_font_color = DEFAULT_QUANTITY_FONT_COLOR):
        #-- Attributs --
        self.item = item
        self.quantity = quantity
        self.size = size
        self.x = x
        self.y = y
        self.color = color
        self.item_name_font_size = item_name_font_size
        self.item_name_font_color = item_name_font_color
        self.quantity_font_size = quantity_font_size
        self.quantity_font_color = quantity_font_color
        
        #-- Graphisme --
        self.update_display()
        

    # GETTER
    def get_rect(self):
        return self.case_sprite.rect
    
    def get_item(self):
        return self.item
    
    def get_quantity(self):
        return self.quantity
    
    # TOOLS - BOOL
    def is_empty(self):
        return self.quantity == 0
    
    def is_not_full(self):
        return self.quantity<self.item.get_max_stack()
    
    def has_room(self, item):
        return self.is_empty() or (self.is_not_full() and self.item == item)
    
    # MOTEUR
    def add_calculation(self, item, quantity=1):
        """
        The function `add_calculation` adds an item to a container, updating the quantity and handling
        stack limits.
        
        :param item: The item parameter represents the item that is being added to the calculation. It
        could be an object or a value that represents the item
        :param quantity: The quantity parameter represents the number of items to be added to the
        calculation. It has a default value of 1, which means if no value is provided when calling the
        function, it will assume a quantity of 1, defaults to 1 (optional)
        :return: the values of `item_left` and `quantity_left`.
        """
        item_left = item
        quantity_left = quantity
        new_quantity = self.quantity + quantity
        max_stack = item.get_max_stack()

        if self.has_room(item):
            if self.is_empty():
                self.item = item
            if new_quantity > max_stack :
                quantity_left = self.quantity + quantity - max_stack
                self.quantity = max_stack
            else:
                item_left = None
                quantity_left = 0
                self.quantity = new_quantity
        return item_left, quantity_left
    
    def take_calculation(self, quantity=1):
        """
        The function takes a quantity as input and returns the item and quantity taken from a container.
        
        :param quantity: The quantity parameter is an optional parameter that specifies the quantity of
        the item to be taken from the calculation. If no quantity is provided, the default value is 1,
        defaults to 1 (optional)
        :return: a tuple containing the item taken and the quantity taken.
        """
        quantity_taken = 0
        item_taken = None
        if not self.is_empty():
            item_taken = self.item
            if quantity < self.quantity:
                quantity_taken = quantity
                self.quantity -= quantity
            else:
                quantity_taken = self.quantity
                self.quantity = 0
                self.item = None
        return item_taken, quantity_taken
    
    # AFFICHAGE - case < item_image < item_name et item_quantity
    def make_case_sprite(self):
        self.case_sprite = Case(self.x, self.y, "", self.size, self.color)
        self.case_sprite._layer = 1

    def make_quantity_sprite(self):
        self.quantity_sprite = TextOutlined(self.x+self.size,
                                            self.y+self.size,
                                            str(self.quantity),
                                            3,
                                            "bottomright",
                                            self.quantity_font_size,
                                            self.quantity_font_color)

    def make_item_name_sprite_custom(self):
        name = self.item.get_name()
        layer = 3
        # self.item_name_sprite_custom is not a sprite, it's a class that contains many sprites
        # go see Utils.py
        self.item_name_sprite_custom = TextOutlined(self.x+self.size/2,
                                             self.y+self.size/2,
                                             name,
                                             layer,
                                             "center",
                                             self.item_name_font_size,
                                             self.item_name_font_color)
        
    def make_item_image_sprite(self):
        # we need proper image from item
        self.item_image_sprite = pygame.sprite.Sprite()
        if self.item.path != "":
            self.item_image_sprite.image = pygame.image.load(self.item.path).convert_alpha()
        else:
            self.item_image_sprite.image = pygame.Surface((20,20))
            self.item_image_sprite.image.fill("yellow")

        self.item_image_sprite.rect = self.item_image_sprite.image.get_rect(center = (self.x+self.size/2,self.y+self.size/2))
        self.item_image_sprite._layer = 2
    
    def update_case_sprite(self):
        if hasattr(self, 'case_sprite'):
            self.case_sprite.kill()
        self.make_case_sprite()
        self.case_sprite.add(draw_grp)

    def update_quantity_sprite(self):
        if hasattr(self, 'quantity_sprite'):
            self.quantity_sprite.kill()
        if not self.is_empty():
            self.make_quantity_sprite()
            self.quantity_sprite.add_to_group(draw_grp)

    def update_item_name_sprite_custom(self):
        if hasattr(self, 'item_name_sprite_custom'):
            self.item_name_sprite_custom.kill()
        if not self.is_empty():
            self.make_item_name_sprite_custom()
            # self.item_name_sprite_custom is not a sprite, it's a class that contains many sprites
            # it has it's own methode to add itself to a group 
            self.item_name_sprite_custom.add_to_group(draw_grp)

    def update_item_image_sprite(self):
        if hasattr(self, 'item_image_sprite'):
            self.item_image_sprite.kill()
        if not self.is_empty():
            self.make_item_image_sprite()
            draw_grp.add(self.item_image_sprite)

    def update_item_image_name_quantity_display(self):
        self.update_quantity_sprite()
        self.update_item_name_sprite_custom()
        self.update_item_image_sprite()
    
    def update_display(self):
        self.update_case_sprite()
        self.update_item_image_name_quantity_display()

    def kill(self):
        if hasattr(self, 'case_sprite'):
            self.case_sprite.kill()
        if hasattr(self, 'quantity_sprite'):
            self.quantity_sprite.kill()
        if hasattr(self, 'item_name_sprite_custom'):
            self.item_name_sprite_custom.kill()
        if hasattr(self, 'item_image_sprite'):
            self.item_image_sprite.kill()

    # OTHERS - CALL MOTEUR AND AFFICHAGE FUNCTIONS
    
    def add_item(self, item, quantity=1):
        item_left, quantity_left = self.add_calculation(item, quantity)
        self.update_item_image_name_quantity_display()
        return item_left,quantity_left
    
    def take_item(self, quantity=1):
        item_taken, quantity_taken = self.take_calculation(quantity)
        self.update_item_image_name_quantity_display()
        return item_taken, quantity_taken

        
    
    
        
    
