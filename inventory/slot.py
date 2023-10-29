from .case import Case
from utils.texts import *
from .settings import *
from general_settings.private_settings import LAYERS

class Slot():
    def __init__(self, state, group, can_take=True, can_add=True, item=None, quantity=0, x=0, y=0, layer=LAYERS["max"], size=CASE_SIZE_DEFAULT, color=SLOT_COLOR_DEFAULT, item_name_font_size=ITEM_NAME_FONT_SIZE_DEFAULT, item_name_font_color=ITEM_NAME_FONT_COLOR_DEFAULT, quantity_font_size=QUANTITY_FONT_SIZE_DEFAULT, quantity_font_color = QUANTITY_FONT_COLOR_DEFAULT):
        self.state = state
        if can_take:
            self.state.slots["take"].append(self)
        if can_add:
            self.state.slots["add"].append(self)

        self.group = group
        self._item = item
        self._quantity = quantity
        self._size = size
        self._x = x
        self._y = y
        self._layer = layer
        self._color = color
        self._item_name_font_size = item_name_font_size
        self._item_name_font_color = item_name_font_color
        self._quantity_font_size = quantity_font_size
        self._quantity_font_color = quantity_font_color
        self.type = 'Slot'

        self.update_display()

    # ////////// PUBLIC \\\\\\\\\\

    # ***** CONTROLS *****
    @property
    def is_empty(self):
        return self._quantity == 0
    
    @property
    def is_not_full(self):
        return self._quantity<self._item.max_stack # type: ignore
    
    def has_room(self, item):
        return self.is_empty or (self.is_not_full and self._item == item)

    # ***** GETTERS *****
    @property
    def rect(self):
        if(hasattr(self, 'case_sprite')):
            return self.case_sprite.rect
        else:
            return None

    @property
    def size(self):
        return self._size

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def color(self):
        return self._color

    @property
    def item_name_font_size(self):
        return self._item_name_font_size

    @property
    def item_name_font_color(self):
        return self._item_name_font_color

    @property
    def quantity_font_size(self):
        return self._quantity_font_size

    @property
    def quantity_font_color(self):
        return self._quantity_font_color

    @property
    def item(self):
        return self._item

    @property
    def quantity(self):
        return self._quantity
    
    # ***** ENGINE *****
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
        new_quantity = self._quantity + quantity
        max_stack = item.max_stack

        if self.has_room(item):
            if self.is_empty:
                self._item = item
            if new_quantity > max_stack :
                quantity_left = self._quantity + quantity - max_stack
                self._quantity = max_stack
            else:
                item_left = None
                quantity_left = 0
                self._quantity = new_quantity
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
        if not self.is_empty:
            item_taken = self._item
            if quantity < self._quantity:
                quantity_taken = quantity
                self._quantity -= quantity
            else:
                quantity_taken = self._quantity
                self._quantity = 0
                self._item = None
        return item_taken, quantity_taken

    def add_item(self, item, quantity=1):
        item_left, quantity_left = self.add_calculation(item, quantity)
        self.update_item_image_name_quantity_display()
        return item_left,quantity_left
    
    def take_item(self, quantity=1):
        item_taken, quantity_taken = self.take_calculation(quantity)
        self.update_item_image_name_quantity_display()
        return item_taken, quantity_taken

    
    # ////////// PRIVATE \\\\\\\\\\
    # Print order: - case < item_image < item_name and item_quantity
    def make_case_sprite(self):
        self.case_sprite = Case(self.group, self._x, self._y, self._layer, "", self._size, self._color)
        self.case_sprite._layer = self._layer # type: ignore

    def make_quantity_sprite(self):
        self.quantity_sprite = TextOutlined(self._x+self._size,
                                            self._y+self._size,
                                            str(self._quantity),
                                            self._layer + 0.2,
                                            "bottomright",
                                            self._quantity_font_size,
                                            self._quantity_font_color)

    def make_item_name_sprite_custom(self):
        name = self._item.name # type: ignore
        # self.item_name_sprite_custom is not a sprite, it's a class that contains many sprites
        # go see Utils.py
        self.item_name_sprite_custom = TextOutlined(self._x+self._size/2,
                                             self._y+self._size/2,
                                             name,
                                             self._layer + 0.2,
                                             "center",
                                             self._item_name_font_size,
                                             self._item_name_font_color)
        
    def make_item_image_sprite(self):
        # we need proper image from item
        self.item_image_sprite = pygame.sprite.Sprite()
        if self._item.img != "": # type: ignore
            self.item_image_sprite.image = pygame.image.load(self._item.img).convert_alpha() # type: ignore
        else:
            self.item_image_sprite.image = pygame.Surface((20,20))
            self.item_image_sprite.image.fill("yellow")

        self.item_image_sprite.rect = self.item_image_sprite.image.get_rect(center = (self._x+self._size/2,self._y+self._size/2))
        self.item_image_sprite._layer = self._layer + 0.1 # type: ignore

    
    def update_case_sprite(self):
        if hasattr(self, 'case_sprite'):
            self.case_sprite.kill()
        self.make_case_sprite()
        self.case_sprite.add(self.group)

    def update_quantity_sprite(self):
        if hasattr(self, 'quantity_sprite'):
            self.quantity_sprite.kill()
        if not self.is_empty:
            self.make_quantity_sprite()
            self.quantity_sprite.add_to_group(self.group)

    def update_item_name_sprite_custom(self):
        if hasattr(self, 'item_name_sprite_custom'):
            self.item_name_sprite_custom.kill()
        if not self.is_empty:
            self.make_item_name_sprite_custom()
            # self.item_name_sprite_custom is not a sprite, it's a class that contains many sprites
            # it has it's own methode to add itself to a group 
            self.item_name_sprite_custom.add_to_group(self.group)

    def update_item_image_sprite(self):
        if hasattr(self, 'item_image_sprite'):
            self.item_image_sprite.kill()
        if not self.is_empty:
            self.make_item_image_sprite()
            self.group.add(self.item_image_sprite)

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
    
